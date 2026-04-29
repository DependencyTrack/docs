# Configuring LDAP

Dependency-Track can authenticate users against an LDAP directory such as Microsoft
Active Directory, ApacheDS, or any other LDAP-compatible server. Once enabled, users
log in with their directory credentials rather than a locally managed password.

## Prerequisites

- A service account in the LDAP directory with read access to users and groups.
- Network connectivity from the Dependency-Track API server to the LDAP server.
- For LDAPS (recommended in production), a valid TLS certificate on the LDAP server.
  If an internal CA issued the certificate, see [Configuring internal CA trust](configuring-internal-ca.md).

## Configuration

Configure all LDAP settings via [app properties](../../reference/configuration/properties.md).
The examples below use property names; see [Application configuration](../../reference/configuration/application.md#environment-variable-mapping)
for how property names map to environment variables.

### Minimal configuration

Enable LDAP and configure the server connection:

```properties linenums="1"
dt.ldap.enabled=true
dt.ldap.server.url=ldap://ldap.example.com:389
dt.ldap.basedn=dc=example,dc=com
dt.ldap.security.auth=simple
dt.ldap.bind.username=cn=dt-service,dc=example,dc=com
dt.ldap.bind.password=changeme
dt.ldap.auth.username.format=uid={0},ou=users,dc=example,dc=com
dt.ldap.attribute.name=cn
dt.ldap.attribute.mail=mail
```

!!! tip
    Dependency-Track substitutes the `{0}` placeholder in `dt.ldap.auth.username.format`
    with the username entered at login.

### User provisioning

When enabled, Dependency-Track creates accounts automatically the first time an LDAP
user logs in. Otherwise, an administrator must create each account before its user can
log in.

```properties
dt.ldap.user.provisioning=true
```

### Team synchronisation

When enabled, Dependency-Track keeps team membership in sync with LDAP group membership.
Map teams to LDAP groups under **Administration > Access Management > Teams**.

```properties
dt.ldap.team.synchronization=true
dt.ldap.groups.filter=(&(objectClass=groupOfUniqueNames))
dt.ldap.user.groups.filter=(&(objectClass=groupOfUniqueNames)(uniqueMember={USER_DN}))
dt.ldap.groups.search.filter=(&(objectClass=groupOfUniqueNames)(cn=*{SEARCH_TERM}*))
dt.ldap.users.search.filter=(&(objectClass=inetOrgPerson)(cn=*{SEARCH_TERM}*))
```

!!! tip
    Dependency-Track substitutes `{USER_DN}` with the authenticated user's distinguished
    name, and `{SEARCH_TERM}` with search input from the UI.

---

## Tested configurations

The configurations below work with specific directory implementations. Adapt values
such as base DNs, bind credentials, and attribute names to match your environment.

### Microsoft Active Directory

Active Directory uses a global catalog port (3268/3269) for forest-wide searches.
Users typically authenticate with their User Principal Name (`user@domain.com`).

```properties linenums="1"
dt.ldap.enabled=true
dt.ldap.server.url=ldap://ldap.example.com:3268
dt.ldap.basedn=dc=example,dc=com
dt.ldap.security.auth=simple
dt.ldap.bind.username=CN=DT Service Account,DC=example,DC=com
dt.ldap.bind.password=changeme
dt.ldap.auth.username.format={0}@example.com
dt.ldap.attribute.name=userPrincipalName
dt.ldap.attribute.mail=mail
dt.ldap.groups.filter=(&(objectClass=group)(objectCategory=Group))
dt.ldap.user.groups.filter=(&(objectClass=group)(objectCategory=Group)(member:1.2.840.113556.1.4.1941:={USER_DN}))
dt.ldap.groups.search.filter=(&(objectClass=group)(objectCategory=Group)(cn=*{SEARCH_TERM}*))
dt.ldap.users.search.filter=(&(objectClass=user)(objectCategory=Person)(cn=*{SEARCH_TERM}*))
```

!!! tip
    The `member:1.2.840.113556.1.4.1941:=` OID in the user groups filter enables
    recursive group membership lookup (LDAP_MATCHING_RULE_IN_CHAIN), so
    Dependency-Track resolves nested group memberships correctly.

For LDAPS (recommended in production), change the port to `3269` and update the URL:

```properties
dt.ldap.server.url=ldaps://ldap.example.com:3269
```

### ApacheDS

```properties linenums="1"
dt.ldap.enabled=true
dt.ldap.server.url=ldap://ldap.example.com:389
dt.ldap.basedn=dc=example,dc=com
dt.ldap.security.auth=simple
dt.ldap.bind.username=uid=admin,ou=system
dt.ldap.bind.password=changeme
dt.ldap.auth.username.format=uid={0},ou=users,dc=example,dc=com
dt.ldap.attribute.name=cn
dt.ldap.attribute.mail=mail
dt.ldap.groups.filter=(&(objectClass=groupOfUniqueNames))
dt.ldap.user.groups.filter=(&(objectClass=groupOfUniqueNames)(uniqueMember={USER_DN}))
dt.ldap.groups.search.filter=(&(objectClass=groupOfUniqueNames)(cn=*{SEARCH_TERM}*))
dt.ldap.users.search.filter=(&(objectClass=inetOrgPerson)(cn=*{SEARCH_TERM}*))
```

### Fedora 389 Directory Server

```properties linenums="1"
dt.ldap.enabled=true
dt.ldap.server.url=ldap://ldap.example.com:389
dt.ldap.basedn=dc=example,dc=com
dt.ldap.security.auth=simple
dt.ldap.bind.username=cn=Directory Manager
dt.ldap.bind.password=changeme
dt.ldap.auth.username.format=uid={0},ou=people,dc=example,dc=com
dt.ldap.attribute.name=uid
dt.ldap.attribute.mail=mail
dt.ldap.groups.filter=(&(objectClass=groupOfUniqueNames))
dt.ldap.user.groups.filter=(&(objectClass=groupOfUniqueNames)(uniqueMember={USER_DN}))
dt.ldap.groups.search.filter=(&(objectClass=groupOfUniqueNames)(cn=*{SEARCH_TERM}*))
dt.ldap.users.search.filter=(&(objectClass=inetOrgPerson)(uid=*{SEARCH_TERM}*))
```

### NetIQ / Novell eDirectory

eDirectory typically uses LDAPS on port 636 and an organisation-based DN structure.

```properties linenums="1"
dt.ldap.enabled=true
dt.ldap.server.url=ldaps://ldap.example.com:636
dt.ldap.basedn=o=example
dt.ldap.security.auth=simple
dt.ldap.bind.username=cn=admin,o=example
dt.ldap.bind.password=changeme
dt.ldap.auth.username.format=uid={0},ou=users,o=example
dt.ldap.attribute.name=uid
dt.ldap.attribute.mail=mail
dt.ldap.groups.filter=(&(objectClass=groupOfUniqueNames))
dt.ldap.user.groups.filter=(&(objectClass=groupOfUniqueNames)(uniqueMember={USER_DN}))
dt.ldap.groups.search.filter=(&(objectClass=groupOfUniqueNames)(cn=*{SEARCH_TERM}*))
dt.ldap.users.search.filter=(&(objectClass=inetOrgPerson)(uid=*{SEARCH_TERM}*))
```

---

## All LDAP properties

For a full list of LDAP-related configuration properties and their types, defaults, and
environment variable equivalents, see the
[configuration reference](../../reference/configuration/properties.md#ldap).

## See also

- [Permissions](../../reference/permissions.md): mapping LDAP groups to Dependency-Track teams
- [Configuring OpenID Connect](configuring-oidc.md): alternative to LDAP using OpenID Connect
- [Configuring internal CA trust](configuring-internal-ca.md): trust internal TLS certificates for LDAPS
