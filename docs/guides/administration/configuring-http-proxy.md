# Configuring an HTTP proxy

The Dependency-Track API server makes outbound HTTP and HTTPS calls to mirror vulnerability data sources, fetch
package metadata from repositories, perform OIDC discovery, deliver webhooks, and reach other integrations. In
environments where outbound traffic must traverse a corporate proxy, configure the API server to route those calls
through it.

Proxy configuration applies to the API server only. The frontend is a static single-page app served to the
user's browser; any requests it appears to make actually originate from the browser itself.

!!! note
    The API server supports only plain HTTP proxies, with optional Basic or NTLM authentication.
    HTTPS-fronted proxies and SOCKS proxies do not work.

## Configuration sources

The API server reads proxy settings from two sources, in this order:

1. App properties (`dt.http.proxy.*`, `dt.no.proxy`).
2. The standard `HTTPS_PROXY`, `HTTP_PROXY`, and `NO_PROXY` environment variables.

If `dt.http.proxy.address` has a value, app properties win and the API server ignores the environment variables.
Otherwise, the API server falls back to the environment.

## Configuring via app properties

Set the following properties (see [Application configuration](../../reference/configuration/application.md#environment-variable-mapping)
for how property names map to environment variables):

- [`dt.http.proxy.address`](../../reference/configuration/properties.md#dthttpproxyaddress): proxy hostname or IP address.
- [`dt.http.proxy.port`](../../reference/configuration/properties.md#dthttpproxyport): proxy port. Required when
  `dt.http.proxy.address` has a value.
- [`dt.http.proxy.username`](../../reference/configuration/properties.md#dthttpproxyusername): optional, for
  authenticated proxies.
- [`dt.http.proxy.password`](../../reference/configuration/properties.md#dthttpproxypassword): optional, for
  authenticated proxies.
- [`dt.no.proxy`](../../reference/configuration/properties.md#dtnoproxy): comma-separated bypass list.

Example:

```properties linenums="1"
dt.http.proxy.address=proxy.example.com
dt.http.proxy.port=8080
dt.no.proxy=localhost,127.0.0.1,example.com
```

## Configuring via standard environment variables

When app properties are unset, the API server reads `HTTPS_PROXY` first and falls back to `HTTP_PROXY`. Variable
names match case-insensitively, so the lowercase forms (`https_proxy`, `http_proxy`, `no_proxy`) work too.

Each value takes the form `http://[user[:password]@]host[:port]`. The API server URL-decodes the credentials, so
reserved characters in the username or password require percent-encoding.

```text
HTTPS_PROXY=http://proxy.example.com:8080
NO_PROXY=localhost,127.0.0.1,example.com
```

The API server uses the same proxy for both HTTP and HTTPS upstream calls. URIs with any other scheme (such as
`ldap://`) always bypass the proxy.

## Bypass list

Both `dt.no.proxy` and `NO_PROXY` accept a comma-separated list of entries. Each entry takes the form of either a
hostname or IP address, optionally with `:port`. CIDR ranges, IP-address ranges, leading-dot notation, and protocol
schemes are not supported.

The matching rules are:

- A single `*` entry disables the proxy for all destinations.
- Comparison is case-insensitive.
- An entry matches the request host exactly, or any subdomain of it. For example, `example.com` matches both
  `example.com` and `api.example.com`.
- If an entry includes a port (`host:port`), the host must match (exact or subdomain) and the port must match exactly.
- Only `http` and `https` URIs go through the proxy; other schemes always bypass it.

For example, given `dt.no.proxy=example.com,localhost:5432`:

- `https://api.example.com/` bypasses the proxy (subdomain match).
- `https://localhost:5432/` bypasses the proxy (host and port match).
- `https://localhost:5433/` goes through the proxy (port mismatch).

## Authenticated proxies

For Basic-authenticated proxies, set `dt.http.proxy.username` and `dt.http.proxy.password`. Avoid placing the password
in plain text; see [Loading values from files](../../reference/configuration/application.md#loading-values-from-files).

For NTLM-authenticated proxies, supply the username in `domain\username` form. The API server splits on the first
backslash into separate domain and username fields. When using the URL form (`HTTPS_PROXY`), percent-encode the
backslash as `%5C`:

```text
HTTPS_PROXY=http://CORP%5Cdt-service:s3cret@proxy.example.com:8080
```

## Trusting an intercepting proxy's certificate

If the proxy terminates and re-issues TLS connections, the API server must trust the proxy's certificate authority.
See [Configuring internal CA trust](configuring-internal-ca.md).
