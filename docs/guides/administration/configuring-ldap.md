# Configuring LDAP

Dependency-Track can authenticate users against an LDAP directory such as Microsoft
Active Directory, ApacheDS, or any other LDAP-compatible server. Once enabled, users
log in with their directory credentials rather than a locally managed password.

## How LDAP authentication works

1. The user enters their credentials on the Dependency-Track login page.
2. Dependency-Track binds to the LDAP server using the configured service account.
3. The user's entry is located in the directory using the configured username format.
4. A bind attempt is made with the user's credentials to verify their password.
5. If successful, the user is granted access. If [user provisioning](#user-provisioning)
   is enabled, their account is created automatically on first login.

## Prerequisites

- A service account in the LDAP directory with read access to users and groups.
- Network connectivity from the Dependency-Track API server to the LDAP server.
- If using LDAPS (recommended for production), a valid TLS certificate on the LDAP server.
  If the certificate is signed by an internal CA, see [Configuring Internal CA](configuring-internal-ca.md).

## Configuration

All LDAP settings are configured via [app properties](../../reference/configuration/properties.md).
The most practical way to supply them in a container deployment is via environment variables.

### Minimal configuration

At least, enable LDAP and configure the server connection:

```ini linenums="1"
DT_LDAP_ENABLED=true
DT_LDAP_SERVER_URL=ldap://ldap.example.com:389
DT_LDAP_BASEDN=dc=example,dc=com
DT_LDAP_SECURITY_AUTH=simple
DT_LDAP_BIND_USERNAME=cn=dt-service,dc=example,dc=com
DT_LDAP_BIND_PASSWORD=changeme
DT_LDAP_AUTH_USERNAME_FORMAT=uid={0},ou=users,dc=example,dc=com
DT_LDAP_ATTRIBUTE_NAME=cn
DT_LDAP_ATTRIBUTE_MAIL=mail
```

The `{0}` placeholder in `DT_LDAP_AUTH_USERNAME_FORMAT` is substituted with the
username entered at login.

### User provisioning

When enabled, accounts are created automatically the first time an LDAP user logs in.
Without provisioning, accounts must be created manually before users can log in.

```ini
DT_LDAP_USER_PROVISIONING=true
```

### Team synchronisation

When enabled, team membership in Dependency-Track is kept in sync with LDAP group
membership. Teams must be mapped to LDAP groups in **Administration → Access Management → Teams**.

```ini
DT_LDAP_TEAM_SYNCHRONIZATION=true
DT_LDAP_GROUPS_FILTER=(&(objectClass=groupOfUniqueNames))
DT_LDAP_USER_GROUPS_FILTER=(&(objectClass=groupOfUniqueNames)(uniqueMember={USER_DN}))
DT_LDAP_GROUPS_SEARCH_FILTER=(&(objectClass=groupOfUniqueNames)(cn=*{SEARCH_TERM}*))
DT_LDAP_USERS_SEARCH_FILTER=(&(objectClass=inetOrgPerson)(cn=*{SEARCH_TERM}*))
```

The `{USER_DN}` placeholder is substituted with the authenticated user's distinguished
name. The `{SEARCH_TERM}` placeholder is substituted with search input from the UI.

---

## Tested Configurations

The following configurations have been tested with specific directory implementations.
Adapt values such as base DNs, bind credentials, and attribute names to match your
environment.

### Microsoft Active Directory

Active Directory uses a global catalog port (3268/3269) for forest-wide searches.
Users typically authenticate with their User Principal Name (`user@domain.com`).

```ini linenums="1"
DT_LDAP_ENABLED=true
DT_LDAP_SERVER_URL=ldap://ldap.example.com:3268
DT_LDAP_BASEDN=dc=example,dc=com
DT_LDAP_SECURITY_AUTH=simple
DT_LDAP_BIND_USERNAME=CN=DT Service Account,DC=example,DC=com
DT_LDAP_BIND_PASSWORD=changeme
DT_LDAP_AUTH_USERNAME_FORMAT={0}@example.com
DT_LDAP_ATTRIBUTE_NAME=userPrincipalName
DT_LDAP_ATTRIBUTE_MAIL=mail
DT_LDAP_GROUPS_FILTER=(&(objectClass=group)(objectCategory=Group))
DT_LDAP_USER_GROUPS_FILTER=(&(objectClass=group)(objectCategory=Group)(member:1.2.840.113556.1.4.1941:={USER_DN}))
DT_LDAP_GROUPS_SEARCH_FILTER=(&(objectClass=group)(objectCategory=Group)(cn=*{SEARCH_TERM}*))
DT_LDAP_USERS_SEARCH_FILTER=(&(objectClass=user)(objectCategory=Person)(cn=*{SEARCH_TERM}*))
```

!!! tip
    The `member:1.2.840.113556.1.4.1941:=` OID in the user groups filter enables
    recursive group membership lookup (LDAP_MATCHING_RULE_IN_CHAIN). This ensures
    nested group memberships are resolved correctly.

For LDAPS (recommended in production), change the port to `3269` and update the URL:

```ini
DT_LDAP_SERVER_URL=ldaps://ldap.example.com:3269
```

### ApacheDS

```ini linenums="1"
DT_LDAP_ENABLED=true
DT_LDAP_SERVER_URL=ldap://ldap.example.com:389
DT_LDAP_BASEDN=dc=example,dc=com
DT_LDAP_SECURITY_AUTH=simple
DT_LDAP_BIND_USERNAME=uid=admin,ou=system
DT_LDAP_BIND_PASSWORD=changeme
DT_LDAP_AUTH_USERNAME_FORMAT=uid={0},ou=users,dc=example,dc=com
DT_LDAP_ATTRIBUTE_NAME=cn
DT_LDAP_ATTRIBUTE_MAIL=mail
DT_LDAP_GROUPS_FILTER=(&(objectClass=groupOfUniqueNames))
DT_LDAP_USER_GROUPS_FILTER=(&(objectClass=groupOfUniqueNames)(uniqueMember={USER_DN}))
DT_LDAP_GROUPS_SEARCH_FILTER=(&(objectClass=groupOfUniqueNames)(cn=*{SEARCH_TERM}*))
DT_LDAP_USERS_SEARCH_FILTER=(&(objectClass=inetOrgPerson)(cn=*{SEARCH_TERM}*))
```

### Fedora 389 Directory Server

```ini linenums="1"
DT_LDAP_ENABLED=true
DT_LDAP_SERVER_URL=ldap://ldap.example.com:389
DT_LDAP_BASEDN=dc=example,dc=com
DT_LDAP_SECURITY_AUTH=simple
DT_LDAP_BIND_USERNAME=cn=Directory Manager
DT_LDAP_BIND_PASSWORD=changeme
DT_LDAP_AUTH_USERNAME_FORMAT=uid={0},ou=people,dc=example,dc=com
DT_LDAP_ATTRIBUTE_NAME=uid
DT_LDAP_ATTRIBUTE_MAIL=mail
DT_LDAP_GROUPS_FILTER=(&(objectClass=groupOfUniqueNames))
DT_LDAP_USER_GROUPS_FILTER=(&(objectClass=groupOfUniqueNames)(uniqueMember={USER_DN}))
DT_LDAP_GROUPS_SEARCH_FILTER=(&(objectClass=groupOfUniqueNames)(cn=*{SEARCH_TERM}*))
DT_LDAP_USERS_SEARCH_FILTER=(&(objectClass=inetOrgPerson)(uid=*{SEARCH_TERM}*))
```

### NetIQ / Novell eDirectory

eDirectory typically uses LDAPS on port 636 and an organisation-based DN structure.

```ini linenums="1"
DT_LDAP_ENABLED=true
DT_LDAP_SERVER_URL=ldaps://ldap.example.com:636
DT_LDAP_BASEDN=o=example
DT_LDAP_SECURITY_AUTH=simple
DT_LDAP_BIND_USERNAME=cn=admin,o=example
DT_LDAP_BIND_PASSWORD=changeme
DT_LDAP_AUTH_USERNAME_FORMAT=uid={0},ou=users,o=example
DT_LDAP_ATTRIBUTE_NAME=uid
DT_LDAP_ATTRIBUTE_MAIL=mail
DT_LDAP_GROUPS_FILTER=(&(objectClass=groupOfUniqueNames))
DT_LDAP_USER_GROUPS_FILTER=(&(objectClass=groupOfUniqueNames)(uniqueMember={USER_DN}))
DT_LDAP_GROUPS_SEARCH_FILTER=(&(objectClass=groupOfUniqueNames)(cn=*{SEARCH_TERM}*))
DT_LDAP_USERS_SEARCH_FILTER=(&(objectClass=inetOrgPerson)(uid=*{SEARCH_TERM}*))
```

---

## All LDAP properties

For a full list of LDAP-related configuration properties and their types, defaults, and
environment variable equivalents, see the
[configuration reference](../../reference/configuration/properties.md#dtldapenabled).

## See also

- [Permissions](../../reference/permissions.md): mapping LDAP groups to Dependency-Track teams
- [Configuring OIDC](configuring-oidc.md): alternative to LDAP using OpenID Connect
- [Configuring Internal CA](configuring-internal-ca.md): trust internal TLS certificates for LDAPS
