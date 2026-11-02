# Configuring SAML

!!! note "Available in 5.3.0 and later"

    Earlier versions support single sign-on through OIDC only.

Dependency-Track supports single sign-on (SSO) via [SAML 2.0](https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf).
When enabled, users authenticate through an external identity provider (IdP)
rather than with a locally managed password. Use SAML when your IdP doesn't
offer OIDC, or when your organization standardizes on SAML for web apps.

!!! note "Frontend configuration required"
    SAML requires configuration on both the **API server** and the **frontend**.
    The API server runs the SAML flow, while the frontend shows the login button.

## Authentication flow

Dependency-Track acts as the SAML service provider (SP). Unlike OIDC, the API
server, not the frontend, talks to the IdP:

1. The user selects the SAML login button. The frontend sends the browser to the
   API server, which redirects it to the IdP with an authentication request.
2. After the user authenticates, the IdP posts a signed SAML response from the
   browser to the API server's assertion consumer service (ACS) at `/api/v2/saml/acs`.
3. The API server verifies the response, then provisions the user and
   synchronizes teams if configured.
4. The API server redirects the browser to the frontend with a one-time code. The
   frontend exchanges the code for a session token.

The one-time code expires after one minute and only works in the browser that
started the login. For the design rationale and the full list of checks the API
server applies to SAML responses, see [ADR 044](https://github.com/DependencyTrack/dependency-track/blob/main/docs/adr/044-saml-authentication.md).

## Prerequisites

- A SAML 2.0 IdP that supports the HTTP-Redirect binding for authentication
  requests and the HTTP-POST binding for responses.
- The IdP must sign the response, the assertion, or both, with RSA-SHA256 or
  stronger and exclusive XML canonicalization. Dependency-Track rejects SHA-1
  signatures and encrypted assertions.
- The IdP's SAML metadata, either as a URL that the API server can reach or as a
  file that you mount into the API server container.
- The API server's `/api/v2/saml/acs` endpoint must be reachable from users' browsers.
- The clocks of the API server and the IdP must be in sync. Dependency-Track
  tolerates a clock skew of up to 60 seconds.

## API server configuration

Configure all SAML settings via [app properties](../../reference/configuration/properties.md).
The examples on this page use property names. See [Application configuration](../../reference/configuration/application.md#environment-variable-mapping)
for how property names map to environment variables.

```properties linenums="1"
dt.frontend-url=https://dtrack.example.com
dt.saml.enabled=true
dt.saml.sp.entity-id=https://dtrack.example.com
dt.saml.sp.acs-url=https://dtrack-api.example.com/api/v2/saml/acs
dt.saml.idp.metadata-url=https://idp.example.com/saml/metadata
```

| Property                   | Purpose                                                                                                     |
|:---------------------------|:------------------------------------------------------------------------------------------------------------|
| `dt.frontend-url`          | Public URL of the frontend. The API server redirects browsers to its `/login/saml` route after the login.   |
| `dt.saml.sp.entity-id`     | Identifier of Dependency-Track at the IdP. Must match the entity ID that you register at the IdP.           |
| `dt.saml.sp.acs-url`       | Public URL of the API server's `/api/v2/saml/acs` endpoint, as browsers see it. Must match the reply URL at the IdP. |
| `dt.saml.idp.metadata-url` | URL of the IdP's SAML metadata. Use `dt.saml.idp.metadata-file` instead to read the metadata from a file.   |

Set exactly one of `dt.saml.idp.metadata-url` and `dt.saml.idp.metadata-file`.
The API server reads the IdP's entity ID, SSO URL, and signing certificates from
the metadata and refreshes it every hour. If a refresh fails, the API server
keeps using the last metadata it loaded.

If the configuration is incomplete, for example when `dt.frontend-url` is
missing, the API server logs an error and keeps SAML login unavailable.

### Registering Dependency-Track at the IdP

The API server publishes its SP metadata at `/api/v2/saml/metadata`. Many IdPs
can import this file or URL directly:

```shell
curl -o dependency-track-sp.xml https://dtrack-api.example.com/api/v2/saml/metadata
```

If your IdP has no metadata import, enter the values by hand:

| IdP setting                         | Value                                               |
|:------------------------------------|:----------------------------------------------------|
| Entity ID, identifier, or audience  | The value of `dt.saml.sp.entity-id`                 |
| ACS URL, reply URL, or callback URL | The value of `dt.saml.sp.acs-url`                   |
| Binding                             | HTTP-POST                                           |
| Signing                             | Sign the assertion, the response, or both           |
| Encryption                          | Off                                                 |

### Username and email

By default, Dependency-Track uses the `NameID` of the assertion's subject as the
username. To read the username from an attribute instead, set the attribute name:

```properties
dt.saml.username-attribute=http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name
```

The attribute must have exactly one value. Dependency-Track refuses the login
when a username starts with the `svc:` prefix that
[service accounts](../../concepts/access-control.md#service-accounts) use, or when a
managed, LDAP, or OIDC user already has the same username.

To store the user's email address, set the attribute that contains it.
Dependency-Track updates the address on every login:

```properties
dt.saml.email-attribute=http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress
```

### User provisioning

When enabled, Dependency-Track creates user accounts automatically on first login:

```properties
dt.saml.user-provisioning=true
```

Otherwise, an administrator must create each account before its user can log in.
Create SAML users under **Administration > Access Management > SAML Users**.
A user without an account sees a message that the account isn't registered.

To add newly provisioned users to a fixed set of teams, list the team names:

```properties
dt.saml.default-teams=Viewers,Auditors
```

Default teams have no effect when team synchronization is enabled.

### Team synchronization

When enabled, Dependency-Track derives team membership from an assertion
attribute that contains the user's groups. Each attribute value counts as one
group name. On every login, Dependency-Track adds the user to all teams mapped
to one of their groups, and removes the user from all other teams.

```properties
dt.saml.team-synchronization=true
dt.saml.groups-attribute=groups
```

To map groups to teams:

1. Go to **Administration > Access Management > SAML Groups**.
2. Select **Create SAML Group** and enter the group name exactly as the IdP sends it.
3. Select the group, then add one or more teams under **Mapped Teams**.

You can also map groups from a team's details under **Administration > Access Management > Teams**.

To skip the manual group creation, enable group provisioning. Dependency-Track
then creates a SAML group for every unknown group name in a user's assertion.
You still map the groups to teams yourself. Dependency-Track never creates teams.

```properties
dt.saml.group-provisioning=true
```

Both team synchronization and group provisioning require `dt.saml.groups-attribute`.

## Frontend configuration

Configure the frontend to show the SAML login button by passing the following
environment variables to the frontend container:

```yaml linenums="1" title="Docker Compose Example"
services:
  frontend:
    image: ghcr.io/dependencytrack/frontend:latest
    environment:
      API_BASE_URL: "https://dtrack-api.example.com"
      SAML_ENABLED: "true"
      SAML_LOGIN_BUTTON_TEXT: "Sign in with SSO"
```

`SAML_LOGIN_BUTTON_TEXT` is optional. When it's empty, the button shows
**Login with SAML**.

The frontend only shows the button when the API server also reports SAML as
enabled. You can configure OIDC and SAML at the same time. The login page then
shows both buttons.

---

## Identity provider examples

The following sections provide configuration notes for common IdPs. In each
case, replace the placeholder values, such as `https://dtrack.example.com` and
the entity IDs, with the values of your environment.

### Keycloak

1. In your realm, create a new **Client** with **Client type** set to `SAML`.
2. Set **Client ID** to the value of `dt.saml.sp.entity-id`.
3. Add the value of `dt.saml.sp.acs-url` to **Valid redirect URIs**, and set it as
   **Assertion Consumer Service POST Binding URL** under **Advanced**.
4. Under **Keys**, turn off **Client signature required**.
5. Under **Settings**, set **Name ID format** to `username` and turn on
   **Force name ID format**. Make sure that **Sign assertions** is on.
6. Under **Client scopes**, open the dedicated scope of the client and add
   these mappers:
    - A **User Property** mapper for the `email` property, with SAML attribute name `email`.
    - A **Group list** mapper with group attribute name `groups`, **Single Group Attribute**
      on, and **Full group path** off, if you want team synchronization.

```properties
dt.saml.sp.entity-id=dependency-track
dt.saml.idp.metadata-url=https://keycloak.example.com/realms/your-realm/protocol/saml/descriptor
dt.saml.email-attribute=email
dt.saml.groups-attribute=groups
```

### Microsoft Entra ID (Azure AD)

1. In the Azure portal, create a new **Enterprise application** of type
   **Non-gallery application**.
2. Under **Single sign-on**, select **SAML**.
3. In **Basic SAML Configuration**, set **Identifier (Entity ID)** to the value of
   `dt.saml.sp.entity-id` and **Reply URL** to the value of `dt.saml.sp.acs-url`.
   You can also upload the SP metadata file instead.
4. In **Attributes & Claims**, add a **group claim** if you want team synchronization.
5. Copy the **App Federation Metadata Url** from the **SAML Certificates** section.

```properties
dt.saml.idp.metadata-url=https://login.microsoftonline.com/<tenant-id>/federationmetadata/2007-06/federationmetadata.xml?appid=<app-id>
dt.saml.email-attribute=http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress
dt.saml.groups-attribute=http://schemas.microsoft.com/ws/2008/06/identity/claims/groups
```

!!! note
    Entra ID sends groups as object IDs (GUIDs) by default, not display names.
    Either create SAML groups with the object IDs, or configure the group claim to
    emit `sAMAccountName` or the cloud-only group display name.

---

## Troubleshooting

When a login fails, the frontend shows **SAML login failed** without details.
The API server logs the reason as a security event, for example
`SAML login refused: Response refused: ...`. Common causes:

| Symptom                                                  | Cause and fix                                                                                                    |
|:---------------------------------------------------------|:-----------------------------------------------------------------------------------------------------------------|
| The login page shows no SAML button.                     | Set `SAML_ENABLED` on the frontend and `dt.saml.enabled` on the API server. `/api/v2/saml/availability` must report `enabled: true`. If it doesn't, check the API server log for configuration errors. |
| The API server responds with `503` when the login starts. | The API server can't load the IdP metadata. Check the metadata URL and the network path, or use a metadata file. |
| The frontend says the account isn't registered.           | User provisioning is off. Create the user under **SAML Users**, or enable `dt.saml.user-provisioning`.          |
| Logins started from the IdP's app portal fail.            | Dependency-Track only accepts logins that it started. Point portal links to the Dependency-Track frontend.     |
| The log reports a signature, audience, or time error.     | Check the IdP's signing algorithm, the entity ID on both sides, and the clock of both servers.                   |
| A user lands in the wrong teams.                          | Check the group names that the IdP sends. Group names must match the SAML group names exactly.                   |

## Limitations

Dependency-Track doesn't support:

- Logins started by the IdP (IdP-initiated SSO).
- Single logout. Logging out of Dependency-Track doesn't end the session at the IdP.
- Encrypted assertions and signed authentication requests.
- More than one IdP.

## All SAML properties

For a full list of SAML-related configuration properties, see the
[configuration reference](../../reference/configuration/properties.md#dtsamlenabled).

## See also

- [Access control](../../concepts/access-control.md): user types, teams, and permissions
- [Configuring OIDC](configuring-oidc.md): alternative to SAML using OpenID Connect
- [Configuring LDAP](configuring-ldap.md): alternative to SAML using LDAP
- [Configuring internal CA trust](configuring-internal-ca.md): trust internal TLS certificates for the IdP metadata URL
