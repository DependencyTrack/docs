# Configuring OpenID Connect

Dependency-Track supports SSO via [OpenID Connect](https://openid.net/specs/openid-connect-core-1_0.html)
(OIDC). When enabled, users authenticate through an external identity provider
(IdP) rather than with a locally managed password.

!!! note "Frontend configuration required"
    OIDC requires configuration on both the **API server** and the **frontend**.
    The API server validates tokens; the frontend initiates the OIDC flow.
    Configure both with the same issuer and client ID.

## Prerequisites

- An OIDC-compatible identity provider with a configured client (app).
- The client must have the Dependency-Track frontend URL registered as a redirect URI.
- The IdP's [discovery endpoint](https://openid.net/specs/openid-connect-discovery-1_0.html)
  (`/.well-known/openid-configuration`) must be reachable from the API server.

## API server configuration

Configure all OIDC settings via [app properties](../../reference/configuration/properties.md).
The examples below use property names; see [Application configuration](../../reference/configuration/application.md#environment-variable-mapping)
for how property names map to environment variables.

```properties linenums="1"
dt.oidc.enabled=true
dt.oidc.issuer=https://idp.example.com
dt.oidc.client.id=dependency-track
dt.oidc.username.claim=preferred_username
```

### User provisioning

When enabled, Dependency-Track creates user accounts automatically on first login:

```properties
dt.oidc.user.provisioning=true
```

### Team synchronisation

When enabled, Dependency-Track derives team membership from a claim that
contains a list of group names. The API server reads the claim from the ID
token first, and falls back to the provider's userinfo response if absent.
Either source works, so configure the claim wherever your IdP makes it
easiest to emit. Map teams to those group names under
**Administration > Access Management > Teams**.

```properties
dt.oidc.team.synchronization=true
dt.oidc.teams.claim=groups
```

## Frontend configuration

Configure the frontend to start the OIDC flow by passing the following
environment variables to the frontend container:

```yaml linenums="1" title="Docker Compose Example"
services:
  frontend:
    image: ghcr.io/dependencytrack/hyades-frontend:latest
    environment:
      API_BASE_URL: "https://dtrack.example.com"
      OIDC_ISSUER: "https://idp.example.com"
      OIDC_CLIENT_ID: "dependency-track"
      OIDC_SCOPE: "openid profile email"
```

The frontend defaults to the `code` flow ([authorization code](https://openid.net/specs/openid-connect-core-1_0.html#CodeFlowAuth)
with [PKCE](https://datatracker.ietf.org/doc/html/rfc7636)), which works with
all modern IdPs and is the recommended setting. The [implicit flow](https://openid.net/specs/openid-connect-core-1_0.html#ImplicitFlowAuth)
(`OIDC_FLOW: "implicit"`) is only needed for IdPs that lack a public-client
configuration compatible with PKCE; [RFC 9700](https://datatracker.ietf.org/doc/html/rfc9700#name-implicit-grant)
no longer recommends it, so prefer `code` whenever the IdP supports it.

---

## Identity provider examples

The following sections provide tested configuration notes for common IdPs.
In each case, adapt the placeholder values (`https://dtrack.example.com`, client IDs,
etc.) to match your environment.

### Keycloak

1. Create a new **Client** in your realm with **Client Protocol** set to `openid-connect`.
2. Set **Access Type** to `public`.
3. Add `https://dtrack.example.com/*` to **Valid Redirect URIs**.
4. Under **Mappers**, add a **Group Membership** mapper with token claim name `groups`
   if you want team synchronisation.

```properties
dt.oidc.issuer=https://keycloak.example.com/realms/your-realm
dt.oidc.client.id=dependency-track
dt.oidc.username.claim=preferred_username
```

### Microsoft Entra ID (Azure AD)

1. Register a new app in the Azure portal.
2. Under **Authentication**, add a **Single-page app** redirect URI:
   `https://dtrack.example.com`.
3. Under **Token configuration**, add an optional claim for `preferred_username` in
   the ID token. Add a **Groups** claim if you want team synchronisation.

```properties
dt.oidc.issuer=https://login.microsoftonline.com/<tenant-id>/v2.0
dt.oidc.client.id=<application-client-id>
dt.oidc.username.claim=preferred_username
```

!!! note
    Entra ID returns groups as object IDs (GUIDs) by default, not display names.
    Configure **Groups claim** to emit `sAMAccountName` or `Group Display Name` in
    the token configuration if you want human-readable group names for team sync.

### Auth0

1. Create a new **Single Page Application** in the Auth0 dashboard.
2. Add `https://dtrack.example.com` to **Allowed Callback URLs**, **Allowed Logout URLs**,
   and **Allowed Web Origins**.
3. To include groups/roles, add a custom Action or Rule that injects a `groups` claim
   into the ID token.

```properties
dt.oidc.issuer=https://your-tenant.auth0.com/
dt.oidc.client.id=<auth0-client-id>
dt.oidc.username.claim=nickname
```

### GitLab

1. In your GitLab instance or on `gitlab.com`, go to **User Settings > Applications**.
2. Add `https://dtrack.example.com` as a redirect URI.
3. Select the `openid`, `profile`, and `email` scopes.

```properties
dt.oidc.issuer=https://gitlab.com
dt.oidc.client.id=<application-id>
dt.oidc.username.claim=nickname
```

For self-hosted GitLab, replace `https://gitlab.com` with your GitLab instance URL.

### Google

1. In the GCP console, create an **OAuth 2.0 Client ID** of type **Web app**.
2. Add `https://dtrack.example.com` to **Authorized JavaScript origins** and
   **Authorized redirect URIs**.

```properties
dt.oidc.issuer=https://accounts.google.com
dt.oidc.client.id=<client-id>.apps.googleusercontent.com
dt.oidc.username.claim=email
```

!!! warning
    Google's **Web app** client type requires a `client_secret` at the token
    endpoint even with PKCE, and Google does not offer a public client type
    for SPAs. The default `code` flow on the frontend cannot complete against
    Google without exposing the secret in browser code. As a workaround, set
    `OIDC_FLOW: "implicit"` on the frontend; note that
    [RFC 9700](https://datatracker.ietf.org/doc/html/rfc9700#name-implicit-grant)
    no longer recommends the implicit flow. For a more secure setup, front
    Google with an IdP that supports public clients with PKCE (for example
    Keycloak or Auth0).

!!! note
    Google does not emit custom group claims in either the ID token or the
    userinfo response. Team synchronisation is not available with Google as
    the IdP unless you use a proxy IdP layer.

### OneLogin

1. In the OneLogin administration portal, create a new **OpenID Connect** app.
2. Set the **Redirect URI** to `https://dtrack.example.com`.
3. Note the **Client ID** and **Issuer URL** from the app's SSO tab.

```properties
dt.oidc.issuer=https://your-subdomain.onelogin.com/oidc/2
dt.oidc.client.id=<client-id>
dt.oidc.username.claim=preferred_username
```

### AWS Cognito

1. Create a **User Pool** in the AWS console.
2. Under **App clients**, create a new client with the **authorization code grant**
   flow enabled and **Generate a client secret** turned off (public client + PKCE).
3. Add `https://dtrack.example.com` to **Callback URLs**.
4. In the **App client settings**, select the `openid`, `profile`, and `email`
   scopes.

```properties
dt.oidc.issuer=https://cognito-idp.<region>.amazonaws.com/<user-pool-id>
dt.oidc.client.id=<app-client-id>
dt.oidc.username.claim=cognito:username
```

---

## All OIDC properties

For a full list of OIDC-related configuration properties, see the
[configuration reference](../../reference/configuration/properties.md#dtoidcenabled).

## See also

- [Permissions](../../reference/permissions.md): mapping IdP groups to Dependency-Track teams
- [Configuring LDAP](configuring-ldap.md): alternative to OIDC using LDAP
- [Configuring Internal CA](configuring-internal-ca.md): trust internal TLS certificates for the IdP
