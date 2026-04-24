# Configuring secret management

Dependency-Track supports pluggable secret storage providers.
This guide covers provider selection, encryption key management,
and caching configuration.

For creating, updating, and deleting secrets in the app,
see [Managing secrets](../user/managing-secrets.md).

## Providers

The secret management mechanism is designed to support different providers.

Currently only the [database](#database) and [environment variable](#environment-variables)
providers are available. Support for external services such as [AWS secrets manager],
[Azure Key Vault], and [HashiCorp Vault] / [OpenBao] is planned.
Implementation of these options is driven by user demand,
so please file an enhancement request if you need any of them.

### Database

The default provider, which stores secrets in the `SECRET` database table.

Secrets are encrypted using [AES-GCM-256].
The provider implements [envelope encryption] to enable [key rotation](#kek-rotation).
All crypto operations are facilitated by [Google Tink].

#### Configuration

The provider may be configured using the following properties:

* [`dt.secret-management.provider`](../../reference/configuration/properties.md#dtsecret-managementprovider)
* [`dt.secret-management.database.datasource.name`](../../reference/configuration/properties.md#dtsecret-managementdatabasedatasourcename)
* [`dt.secret-management.database.kek`](../../reference/configuration/properties.md#dtsecret-managementdatabasekek)
* [`dt.secret-management.database.kek-keyset.path`](../../reference/configuration/properties.md#dtsecret-managementdatabasekek-keysetpath)
* [`dt.secret-management.database.kek-keyset.create-if-missing`](../../reference/configuration/properties.md#dtsecret-managementdatabasekek-keysetcreate-if-missing)

!!! note
    Also refer to the [data source configuration](../../reference/configuration/datasources.md) documentation.

#### Key management

Encryption of secrets involves two types of keys:

* The key encryption key (KEK)
* Data encryption keys (DEKs)

When creating a secret, Dependency-Track generates a new DEK,
and encrypts the secret value with it. It then encrypts the DEK
with the KEK. Both the encrypted DEK and the encrypted secret value
are then stored in the database.

!!! info
    The encrypted DEK is [tagged](https://developers.google.com/tink/design/keysets#keyids)
    with the ID of the KEK that encrypted it.

When reading a secret, the encrypted DEK and encrypted secret value
are read from the database. The DEK is then decrypted with the KEK,
which then allows the secret value to be decrypted using the DEK.

Dependency-Track uses [Google Tink]'s concept of [keysets]
to enable rotation of KEKs. A KEK keyset is created automatically
on startup. Or, a [manually created keyset](#creating-kek-keysets)
may be provided.

The KEK keyset uses [Google Tink]'s JSON serialization,
and is not encrypted itself. For production deployments,
**mount the KEK keyset at runtime** using
[Kubernetes secrets] or similar mechanisms, and ensure that
the keyset file is only readable by the app user.
Refer to [Creating KEK keysets](#creating-kek-keysets) for an example.

!!! note
    [Google Tink] [supports](https://developers.google.com/tink/key-management-overview#create_kek)
    a small selection of key management systems (KMS), which may be used to manage the KEK keyset.
    Dependency-Track does not yet use this capability. If this is important to you,
    please raise an enhancement request.

#### Config-based KEK

As an alternative to the keyset file, the KEK can be provided directly as a base64-encoded
AES-256 key (32 bytes) via the [`dt.secret-management.database.kek`](../../reference/configuration/properties.md#dtsecret-managementdatabasekek)
property. When set, this takes precedence over the keyset file configuration.

This is useful for multi-instance deployments where sharing a keyset file across nodes
is inconvenient, for example when the KEK is stored in a secret manager that exposes
values as environment variables rather than files.

!!! warning
    The config-based KEK does **not** support [KEK rotation](#kek-rotation). If you expect
    to rotate the KEK, use the [file-based keyset approach](#creating-kek-keysets) instead.

#### Creating KEK keysets

To create a new KEK keyset, the following prerequisites are required:

* A working [Google Tinkey] installation

Create a new keyset using the `AES256_GCM` preset:

```shell linenums="1"
tinkey create-keyset \
  --key-template AES256_GCM \
  --out secret-management-kek.json \
  --out-format json
```

List keys in the new keyset to verify that a valid key was generated:

```shell linenums="1"
tinkey list-keyset \
  --in secret-management-kek.json \
  --in-format json
```

??? info "Example Output"
    ```
    primary_key_id: 1115312215
    key_info {
      type_url: "type.googleapis.com/google.crypto.tink.AesGcmKey"
      status: ENABLED
      key_id: 1115312215
      output_prefix_type: TINK
    }
    ```

Make Dependency-Track use the keyset by:

1. Mounting the file into the API server container
2. Configuring [`kek-keyset.path`](../../reference/configuration/properties.md#dtsecret-managementdatabasekek-keysetpath)
   to point to the location where the file has been mounted
3. Disabling the [`kek-keyset.create-if-missing`](../../reference/configuration/properties.md#dtsecret-managementdatabasekek-keysetcreate-if-missing) option

??? example "Kubernetes Secret Example"
    ```yaml linenums="1"
    apiVersion: v1
    kind: Secret
    metadata:
      name: secret-management-kek
    type: Opaque
    stringData:
      keyset.json: |
        {
          "primaryKeyId": 1115312215,
          "key": [
            {
              "keyData": {
                "typeUrl": "type.googleapis.com/google.crypto.tink.AesGcmKey",
                "value": "GhD...",
                "keyMaterialType": "SYMMETRIC"
              },
              "status": "ENABLED",
              "keyId": 1115312215,
              "outputPrefixType": "TINK"
            }
          ]
        }
    ---
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: dependency-track-apiserver
    spec:
      template:
        spec:
          containers:
          - name: apiserver
            # ...
            env:
            - name: DT_SECRET_MANAGEMENT_PROVIDER
              value: "database"
            - name: DT_SECRET_MANAGEMENT_DATABASE_KEK_KEYSET_PATH
              value: "/run/secrets/secret-management-kek/keyset.json"
            - name: DT_SECRET_MANAGEMENT_DATABASE_KEK_KEYSET_CREATE_IF_MISSING
              value: "false"
            volumeMounts:
            - name: kek-keyset
              mountPath: /run/secrets/secret-management-kek
              readOnly: true
          volumes:
          - name: kek-keyset
            secret:
              secretName: secret-management-kek
              defaultMode: 0400
    ```

#### KEK rotation

To perform KEK rotation, the following prerequisites are required:

* A working [Google Tinkey] installation
* Access to the KEK keyset

First, list the keys currently contained in the keyset:

```shell linenums="1"
tinkey list-keyset \
  --in secret-management-kek.json \
  --in-format json
```

??? info "Example Output"
    ```
    primary_key_id: 1115312215
    key_info {
      type_url: "type.googleapis.com/google.crypto.tink.AesGcmKey"
      status: ENABLED
      key_id: 1115312215
      output_prefix_type: TINK
    }
    ```

Add a new key using the `AES256_GCM` template:

```shell linenums="1"
tinkey add-key \
  --key-template AES256_GCM \
  --in secret-management-kek.json \
  --in-format json \
  --out secret-management-kek-new.json \
  --out-format json
```

List keys in the new keyset file, verifying that it now contains multiple keys:

```shell linenums="1"
tinkey list-keyset \
  --in secret-management-kek-new.json \
  --in-format json
```

??? info "Example Output"
    ```
    primary_key_id: 1115312215
    key_info {
      type_url: "type.googleapis.com/google.crypto.tink.AesGcmKey"
      status: ENABLED
      key_id: 1115312215
      output_prefix_type: TINK
    }
    key_info {
      type_url: "type.googleapis.com/google.crypto.tink.AesGcmKey"
      status: ENABLED
      key_id: 3812494172
      output_prefix_type: TINK
    }
    ```

Note how both keys are `ENABLED`, but the old key's ID is still referenced
via `primary_key_id`. Only the primary key encrypts new data, but
other `ENABLED` keys remain available for decryption.

Roll out the new keyset to your Dependency-Track instances. This ensures that
all instances can decrypt DEKs using the new KEK when you make it
the primary key later. Until then, DEKs continue to be encrypted using the old KEK.

!!! warning
    The KEK keyset is only loaded on startup. Ensure that your DT instances
    are restarted and the new KEK keyset file is mounted.

Once the new KEK key is successfully rolled out, you can promote it to be primary key:

```shell linenums="1"
tinkey promote-key \
  --in secret-management-kek-new.json \
  --in-format json \
  --key-id 3812494172 \
  --out secret-management-kek-new-promoted.json \
  --out-format json
```

List the keys again to verify the promotion was successful:

```shell linenums="1"
tinkey list-keyset \
  --in secret-management-kek-new-promoted.json \
  --in-format json
```

??? info "Example Output"
    ```
    primary_key_id: 3812494172
    key_info {
      type_url: "type.googleapis.com/google.crypto.tink.AesGcmKey"
      status: ENABLED
      key_id: 1115312215
      output_prefix_type: TINK
    }
    key_info {
      type_url: "type.googleapis.com/google.crypto.tink.AesGcmKey"
      status: ENABLED
      key_id: 3812494172
      output_prefix_type: TINK
    }
    ```

After making sure that `primary_key_id` now refers to the new key, roll out
this new keyset to your Dependency-Track deployments.

From now on, whenever a new secret is created or an existing secret's value changes,
the DEK is encrypted with the new KEK.

!!! warning
    `tinkey` lets you turn off, destroy, and delete keys from a keyset.
    Before you perform any of those actions, be aware that it can prevent
    encrypted secrets in the database from being decrypted.
    Dependency-Track does not currently offer a mechanism to re-crypt existing
    secrets. If this is important to you, please raise an enhancement request.

### Environment variables

A simple provider that reads secrets from environment variables.
This can be convenient for test deployments, when secrets rarely change,
or when service availability is not critical.

!!! warning
    This provider is **read-only**. Secrets come from the environment
    **once** on startup. You **cannot** *add*, *update*,
    or *remove* secrets at runtime. Changing secret values requires a restart
    of the Dependency-Track instance.

Environment variables must be prefixed with `DT_SECRET_` for the
provider to recognize them. Casing of the prefix does not matter, but the casing *after* the
prefix is preserved as-is. For example:

```ini linenums="1"
# Picked up as secret "GITHUB_TOKEN":
DT_SECRET_GITHUB_TOKEN=foo

# Picked up as secret "github_token":
dt_secret_github_token=foo

# NOT recognized as secret due to missing prefix:
GITHUB_TOKEN=foo
```

The provider logs the name of secrets it discovered on startup.
It also emits a warning log message when it found no secrets at all.

#### Configuration

The provider may be configured using the following properties:

* [`dt.secret-management.provider`](../../reference/configuration/properties.md#dtsecret-managementprovider)

??? info "Example Configuration"
    ```ini linenums="1"
    dt.secret-management.provider=env
    ```

## Caching

To reduce provider load and improve performance, secret values can be cached
in memory. This is configured via:

* [`dt.secret-management.cache.enabled`](../../reference/configuration/properties.md#dtsecret-managementcacheenabled)
* [`dt.secret-management.cache.expire-after-write-ms`](../../reference/configuration/properties.md#dtsecret-managementcacheexpire-after-write-ms)
* [`dt.secret-management.cache.max-size`](../../reference/configuration/properties.md#dtsecret-managementcachemax-size)

!!! info
    Caching is applied transparently regardless of which provider is configured.
    When enabled, decrypted secret values are cached for the configured duration.

!!! warning
    Cached secrets are invalidated when they get updated or deleted.
    This only applies to the node that performed the update or deletion.
    Other nodes in the cluster rely on the time-based invalidation.
    Take this into consideration when enabling the cache and configuring
    the `expire-after-write-ms` option.

[AES-GCM-256]: https://en.wikipedia.org/wiki/Galois/Counter_Mode
[AWS secrets manager]: https://aws.amazon.com/secrets-manager/
[Azure Key Vault]: https://azure.microsoft.com/en-us/products/key-vault
[Google Tink]: https://developers.google.com/tink/what-is
[Google Tinkey]: https://developers.google.com/tink/tinkey-overview
[HashiCorp Vault]: https://www.hashicorp.com/en/products/vault
[Kubernetes secrets]: https://kubernetes.io/docs/concepts/configuration/secret/
[OpenBao]: https://openbao.org/
[envelope encryption]: https://en.wikipedia.org/wiki/Hybrid_cryptosystem#Envelope_encryption
[keysets]: https://developers.google.com/tink/design/keysets
