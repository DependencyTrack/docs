# About access control

Dependency-Track uses a role-based access control model built around **permissions**,
**teams**, and **users**. Teams hold permissions, and users inherit the
permissions of every team they belong to.

## Users

Three types of users exist:

| Type          | Description                                                                                       |
|:--------------|:--------------------------------------------------------------------------------------------------|
| Managed User  | A local account created and managed within Dependency-Track.                                      |
| LDAP User     | Authenticated via an external LDAP directory. See [Configuring LDAP](../guides/administration/configuring-ldap.md). |
| OIDC User     | Authenticated via an OpenID Connect identity provider. See [Configuring OIDC](../guides/administration/configuring-oidc.md). |

All user types share the same permission model. The authentication mechanism determines
how the system verifies a user's identity, not what they can access.

### LDAP authentication flow

With LDAP, Dependency-Track authenticates users by performing a service-account
bind to locate the user's directory entry, then attempting a bind with the user's
own credentials to verify their password. On success, the system grants access.
With user provisioning turned on, Dependency-Track creates the account
automatically on first login.

### OIDC authentication flow

With OIDC, the frontend redirects the user to the identity provider's authorization
endpoint. After the user authenticates, the IdP returns an ID token to the frontend,
which forwards it to the API server for validation. The API server verifies the token
against the IdP's discovery endpoint and extracts the username from the configured
claim. With user provisioning turned on, Dependency-Track creates accounts on
first login.

## Teams

A team is a named collection of users and API keys. Teams hold permissions directly;
individual users do not. This makes it straightforward to manage access for groups of
people (for example, *Security Engineers*, *Developers*, *CI/CD Pipelines*) or automated systems.

A user can belong to more than one team and inherits the union of all permissions from
every team they are a member of.

API keys belong to a team and carry the same permissions as that team. They authenticate
automated access (CI/CD pipelines, integrations) without associating requests with a
specific human user.

## Portfolio access control

By default, all teams with `VIEW_PORTFOLIO` can see every project. Access Control Lists
(ACLs) restrict portfolio visibility so that a team can only see the projects explicitly
assigned to it.

Enable ACLs in **Administration > Access Management > Portfolio Access Control**.
Once active, every project must be explicitly assigned to at least one team for it to
be visible to non-administrator users.

ACLs are most useful in multi-tenant scenarios where different teams should not see
each other's projects. For single-team or open environments, ACLs add management
overhead without security benefit.

## Further reading

* [Permissions reference](../reference/permissions.md) for the full permissions table
  and default teams.
