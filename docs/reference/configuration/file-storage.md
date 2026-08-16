# File storage

Dependency-Track uses file storage for intermediate data during background processing,
including uploaded BOMs, vulnerability analysis results, and large notifications.
Files are short-lived and automatically cleaned up after processing.

The storage provider is selected via [`dt.file-storage.provider`](properties.md#dtfile-storageprovider).

Both providers compress stored files using [zstd](https://facebook.github.io/zstd/). The compression level is
configurable per provider (default: 5, range: -7 to 22). Higher levels yield
better compression at the cost of CPU.

## Providers

### Local

The `local` provider stores files on the local filesystem. This is the default.

```ini
dt.file-storage.provider=local
dt.file-storage.local.directory=/data/storage
```

When running multiple instances, all nodes must have access to the same directory.
A shared persistent volume (for example, NFS) works well for this.

Configuration:

- [`dt.file-storage.local.directory`](properties.md#dtfile-storagelocaldirectory)
- [`dt.file-storage.local.compression-level`](properties.md#dtfile-storagelocalcompression-level)

### S3

The `s3` provider stores files in an S3-compatible object store (AWS S3, MinIO, etc.).
Use this when a shared volume is impractical.

The bucket must exist before startup. Dependency-Track will verify its existence
and fail to start if it's not found.

```ini
dt.file-storage.provider=s3
dt.file-storage.s3.endpoint=https://s3.amazonaws.com
dt.file-storage.s3.bucket=dtrack-files
dt.file-storage.s3.access-key=<access-key>
dt.file-storage.s3.secret-key=<secret-key>
dt.file-storage.s3.region=us-east-1
```

#### Authentication

How the `s3` provider authenticates is controlled by `dt.file-storage.s3.credentials-source`,
which defaults to `static`.

**Static credentials** (`credentials-source=static`, the default). Configure
both `dt.file-storage.s3.access-key` and `dt.file-storage.s3.secret-key`. If either of them
is missing, Dependency-Track fails to start.
This mode works with any S3-compatible object store.

**AWS environment credentials** (`credentials-source=aws`). Dependency-Track resolves credentials
from its environment, using the first of these sources that provides them:

1. The `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables
2. The shared AWS configuration file, `~/.aws/credentials` by default
3. IAM Roles for Service Accounts (IRSA) on Amazon EKS
4. Task roles on Amazon ECS
5. Instance profiles on Amazon EC2

```ini
dt.file-storage.provider=s3
dt.file-storage.s3.endpoint=https://s3.us-east-1.amazonaws.com
dt.file-storage.s3.bucket=dtrack-files
dt.file-storage.s3.region=us-east-1
dt.file-storage.s3.credentials-source=aws
```

Dependency-Track resolves credentials when it verifies the bucket during startup.
If no source provides credentials, or if static credentials are configured alongside
`credentials-source=aws`, startup fails.

!!! note
    Amazon EKS Pod Identity is not supported. The S3 client does not read the token file that the
    Pod Identity Agent provides, and it rejects the agent's endpoint because that address is not a
    loopback address. Use IRSA on Amazon EKS.

Configuration:

- [`dt.file-storage.s3.endpoint`](properties.md#dtfile-storages3endpoint)
- [`dt.file-storage.s3.bucket`](properties.md#dtfile-storages3bucket)
- [`dt.file-storage.s3.credentials-source`](properties.md#dtfile-storages3credentials-source)
- [`dt.file-storage.s3.access-key`](properties.md#dtfile-storages3access-key)
- [`dt.file-storage.s3.secret-key`](properties.md#dtfile-storages3secret-key)
- [`dt.file-storage.s3.region`](properties.md#dtfile-storages3region)
- [`dt.file-storage.s3.compression-level`](properties.md#dtfile-storages3compression-level)
- [`dt.file-storage.s3.connect-timeout-ms`](properties.md#dtfile-storages3connect-timeout-ms)
- [`dt.file-storage.s3.read-timeout-ms`](properties.md#dtfile-storages3read-timeout-ms)
- [`dt.file-storage.s3.write-timeout-ms`](properties.md#dtfile-storages3write-timeout-ms)
