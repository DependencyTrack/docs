# Configuring OpenID Connect

Dependency-Track supports single sign-on via OpenID Connect (OIDC). When enabled,
users authenticate through an external identity provider (IdP) rather than a
locally managed password.

!!! note "Frontend configuration required"
    OIDC requires configuration on both the **API server** and the **frontend**.
    The API server validates tokens; the frontend initiates the OIDC flow. Both
    must be configured with the same issuer and client ID.

## Prerequisites

- An OIDC-compatible identity provider with a configured client (app).
- The client must have the Dependency-Track frontend URL registered as a redirect URI.
- The IdP's discovery endpoint (`/.well-known/openid-configuration`) must be
  reachable from the API server.

## API server configuration

Configure the following properties on the API server:

```ini linenums="1"
DT_OIDC_ENABLED=true
DT_OIDC_ISSUER=https://idp.example.com        # IdP's issuer URL
DT_OIDC_CLIENT_ID=dependency-track            # Client ID registered with the IdP
DT_OIDC_USERNAME_CLAIM=preferred_username     # Claim to use as the DT username
```

### User provisioning

When enabled, user accounts are created automatically on first login:

```ini
DT_OIDC_USER_PROVISIONING=true
```

### Team synchronisation

When enabled, team membership is driven by a claim in the ID token that contains
a list of group names. Teams must be mapped to those group names in
**Administration → Access Management → Teams**.

```ini
DT_OIDC_TEAM_SYNCHRONIZATION=true
DT_OIDC_TEAMS_CLAIM=groups    # Name of the claim containing group names
```

## Frontend Configuration

The frontend must also be configured to start the OIDC flow. Pass the following
environment variables to the frontend container:

```yaml linenums="1"
# Docker Compose example
services:
  frontend:
    image: ghcr.io/dependencytrack/hyades-frontend:latest
    environment:
      API_BASE_URL: "https://dtrack.example.com"
      OIDC_ISSUER: "https://idp.example.com"
      OIDC_CLIENT_ID: "dependency-track"
      OIDC_SCOPE: "openid profile email"
      OIDC_FLOW: "implicit"
```

!!! note
    Some IdPs require the `authorization_code` flow instead of `implicit`. Refer
    to your IdP's documentation and adjust `OIDC_FLOW` accordingly.

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

```ini
DT_OIDC_ISSUER=https://keycloak.example.com/realms/your-realm
DT_OIDC_CLIENT_ID=dependency-track
DT_OIDC_USERNAME_CLAIM=preferred_username
```

### Microsoft Entra ID (Azure AD)

1. Register a new app in the Azure portal.
2. Under **Authentication**, add a **Single-page app** redirect URI:
   `https://dtrack.example.com`.
3. Under **Token configuration**, add an optional claim for `preferred_username` in
   the ID token. Add a **Groups** claim if you want team synchronisation.

```ini
DT_OIDC_ISSUER=https://login.microsoftonline.com/<tenant-id>/v2.0
DT_OIDC_CLIENT_ID=<application-client-id>
DT_OIDC_USERNAME_CLAIM=preferred_username
```

```yaml
OIDC_FLOW: "implicit"
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

```ini
DT_OIDC_ISSUER=https://your-tenant.auth0.com/
DT_OIDC_CLIENT_ID=<auth0-client-id>
DT_OIDC_USERNAME_CLAIM=nickname
```

### GitLab

1. In your GitLab instance or gitlab.com, go to **User Settings → Applications**.
2. Add `https://dtrack.example.com` as a redirect URI.
3. Select the `openid`, `profile`, and `email` scopes.

```ini
DT_OIDC_ISSUER=https://gitlab.com
DT_OIDC_CLIENT_ID=<application-id>
DT_OIDC_USERNAME_CLAIM=nickname
```

For self-hosted GitLab, replace `https://gitlab.com` with your GitLab instance URL.

### Google

1. In the Google Cloud console, create an **OAuth 2.0 Client ID** of type
   **Web app**.
2. Add `https://dtrack.example.com` to **Authorized JavaScript origins** and
   **Authorized redirect URIs**.

```ini
DT_OIDC_ISSUER=https://accounts.google.com
DT_OIDC_CLIENT_ID=<client-id>.apps.googleusercontent.com
DT_OIDC_USERNAME_CLAIM=email
```

!!! note
    Google does not support custom group claims in ID tokens. Team synchronisation
    is not available with Google as the IdP unless you use a proxy IdP layer.

### OneLogin

1. In the OneLogin administration portal, create a new **OpenID Connect** app.
2. Set the **Redirect URI** to `https://dtrack.example.com`.
3. Note the **Client ID** and **Issuer URL** from the app's SSO tab.

```ini
DT_OIDC_ISSUER=https://your-subdomain.onelogin.com/oidc/2
DT_OIDC_CLIENT_ID=<client-id>
DT_OIDC_USERNAME_CLAIM=preferred_username
```

### AWS Cognito

1. Create a **User Pool** in the AWS console.
2. Under **App clients**, create a new client with the **implicit grant** flow enabled.
3. Add `https://dtrack.example.com` to **Callback URLs**.
4. In the **App client settings**, ensure `openid`, `profile`, and `email` scopes
   are selected.

```ini
DT_OIDC_ISSUER=https://cognito-idp.<region>.amazonaws.com/<user-pool-id>
DT_OIDC_CLIENT_ID=<app-client-id>
DT_OIDC_USERNAME_CLAIM=cognito:username
```

---

## All OIDC properties

For a full list of OIDC-related configuration properties, see the
[configuration reference](../../reference/configuration/properties.md#dtoidcenabled).

## See also

- [Permissions](../../reference/permissions.md): mapping IdP groups to Dependency-Track teams
- [Configuring LDAP](configuring-ldap.md): alternative to OIDC using LDAP
- [Configuring Internal CA](configuring-internal-ca.md): trust internal TLS certificates for the IdP
