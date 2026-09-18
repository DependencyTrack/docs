# Workload identity

!!! note "Available in 5.2.0 and later"

    Earlier versions authenticate automation with team API keys only.

For the model, see [About workload identity federation](../concepts/workload-identity-federation.md).
For the procedure, see [Configuring workload identity federation](../guides/administration/configuring-workload-identity-federation.md).

Field constraints, request bodies, responses, and the permission each operation requires are
in the [REST API v2 reference](api/v2.md), under the operations tagged `Workload Identity Providers`, `OAuth`,
and the workload identity binding operations tagged `Service Accounts`.
This page describes the behavior behind those operations.

## Provider types

| Type     | `iss` claim                      | `sub` claim                                | Key source                          |
|:---------|:---------------------------------|:-------------------------------------------|:------------------------------------|
| `OIDC`   | Must equal the provider's issuer | Any value                                  | Discovery, a key set URL, or inline |
| `SPIFFE` | Ignored                          | Must start with `spiffe://<trust-domain>/` | A bundle endpoint URL, or inline    |

The issuer of a `SPIFFE` provider is a bare trust domain, such as `example.org`.
A key set URL on a `SPIFFE` provider is the trust domain's bundle endpoint,
which must use the `https_web` profile of SPIFFE federation.

## Key fetching

Discovery reads `<issuer>/.well-known/openid-configuration`, requires the document to name the same issuer,
and stores the `jwks_uri` it names. Changing the issuer of an `OIDC` provider that fetches its keys from
a URL re-runs discovery and replaces the stored URL, unless the update names a key source itself.

Dependency-Track caches fetched key sets and rate-limits how often it refreshes them per provider.
When a refresh fails, it keeps using the last fetched key set for up to one hour.

### Outbound fetch constraints

Dependency-Track fetches remote documents when you save a provider,
and during an exchange when a key is missing from the cache. Every fetch obeys the following:

* Only `https` URLs, without user information.
* After resolving the hostname, Dependency-Track refuses loopback, link-local, wildcard,
  and multicast addresses. Private ranges stay allowed. When a configured HTTP proxy handles the destination,
  Dependency-Track skips the address check, because the proxy resolves the name.
* Dependency-Track doesn't follow redirects.
* A response must arrive complete within 10 seconds, and must not exceed 1 MiB.
* Response bodies never appear in API responses or logs.

## Subject matching

A subject is either an exact value or a prefix followed by `*`.
The prefix must be non-empty and must end with `:` or `/`.

| Subject                                 | Matches                                           |
|:----------------------------------------|:--------------------------------------------------|
| `repo:acme-inc/app:ref:refs/heads/main` | That exact `sub` claim.                           |
| `repo:acme-inc/*`                       | Every `sub` starting with `repo:acme-inc/`.       |
| `repo:acme-inc/app*`                    | Rejected. The prefix doesn't end with `:` or `/`. |
| `spiffe://example.org/ci/*`             | Every SPIFFE ID under `spiffe://example.org/ci/`. |
| `spiffe://example.org/ci*`              | Rejected. A SPIFFE prefix must end with `/`.      |

For `SPIFFE` providers, the subject must lie within the provider's trust domain.

To match a prefix that ends mid-segment, use an exact subject prefix plus a condition,
such as `claims.sub.startsWith("repo:acme-inc/app-")`.

## Condition environment

Conditions are [CEL](cel-expressions.md) expressions.
Dependency-Track compiles and type-checks them when you save the binding.
They see one variable:

| Variable | Type               | Contents                                  |
|:---------|:-------------------|:------------------------------------------|
| `claims` | `map(string, dyn)` | The claims of the verified subject token. |

The [CEL strings extension](https://github.com/google/cel-spec/blob/master/doc/extensions/strings.md) is available.
Dependency-Track registers no custom functions here.

An expression must return a boolean. Because claim values are dynamic,
`claims.admin` alone doesn't compile. Write `claims.admin == true` instead.

At exchange time, a condition that raises an error, for example because a claim is absent, doesn't match.
Guard optional claims with `has(claims.name)` where the binding should still match tokens that omit them.
Claim values keep their JSON types, and platforms that encode booleans as strings need string comparisons.

```js
claims.ref == "refs/heads/main"

claims.environment == "production" && claims.environment_protected == "true"

claims.sub.startsWith("repo:acme-inc/app-")
```

## Matching order

Dependency-Track evaluates only the bindings of the service account that the request names,
and only those belonging to the named provider. It tries them from oldest to newest and uses
the first whose subject and condition both match. Duplicate and overlapping bindings do no harm,
because the resulting session is the same either way.

## Subject token requirements

A subject token must be a signed JWT that meets these requirements:

| Property            | Value                                                                                  |
|:--------------------|:---------------------------------------------------------------------------------------|
| Header `typ`        | `JWT`, `JOSE`, `at+jwt`, or absent.                                                    |
| Signature algorithm | `RS256`, `RS384`, `RS512`, `PS256`, `PS384`, `PS512`, `ES256`, `ES384`, or `ES512`.    |
| Required claims     | `exp` and `sub`.                                                                       |
| `aud`               | Must contain the provider's audience.                                                  |
| `iss`               | Must equal the provider's issuer for `OIDC` providers. Ignored for `SPIFFE` providers. |

Dependency-Track refuses symmetric and unsigned tokens. It accepts keys marked for `jwt-svid` use,
as SPIFFE bundles mark them, alongside keys marked for signature use.

## Audit events

The API server logs the following as security events:

* Creating, updating, and deleting providers and bindings.
* Successful exchanges, naming the provider, the service account, the matched binding,
  the token's subject, and its `jti` if it has one.
* Refused exchanges. When the token verified but no binding matched, the log also carries the token's claims.

Subject tokens are never logged.
