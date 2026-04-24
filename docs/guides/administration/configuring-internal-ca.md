# Configuring internal CA trust

By default, the Java runtime bundled in the Dependency-Track container image trusts
only well-known public certificate authorities. If your environment uses TLS
certificates signed by an internal or private CA, connections to those endpoints
fail with a certificate validation error:

```text
PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException:
unable to find valid certification path to requested object
```

Common scenarios where this occurs:

- **LDAPS**: connecting to an LDAP server using TLS ([Configuring LDAP](configuring-ldap.md))
- **OIDC**: the identity provider uses a privately signed certificate ([Configuring OIDC](configuring-oidc.md))
- **HTTP proxy**: an intercepting TLS proxy sits between Dependency-Track and external services
- **Internal vulnerability sources**: a private vulnerability repository or API server with an internal certificate

The solution is to import your internal CA certificate into the JVM truststore and
mount the modified truststore into the container.

## Step 1: Export the default truststore

Run a temporary container from the API server image and copy out the default truststore:

```shell linenums="1"
docker run --rm \
  --entrypoint cp \
  ghcr.io/dependencytrack/hyades-apiserver:latest \
  /opt/java/openjdk/lib/security/cacerts /tmp/cacerts-modified

docker cp \
  $(docker ps -lq) \
  /tmp/cacerts-modified \
  ./cacerts-modified
```

Or use a single command with `docker create`:

```shell linenums="1"
container_id=$(docker create ghcr.io/dependencytrack/hyades-apiserver:latest)
docker cp "$container_id:/opt/java/openjdk/lib/security/cacerts" ./cacerts-modified
docker rm "$container_id"
```

## Step 2: Import your internal CA certificate

Use the `keytool` utility (included in any JDK) to import your CA certificate.
The default truststore password is `changeit`.

```shell linenums="1"
keytool -import \
  -trustcacerts \
  -keystore ./cacerts-modified \
  -storepass changeit \
  -noprompt \
  -alias internal-ca \
  -file /path/to/your/internal-ca.crt
```

Verify the import succeeded:

```shell linenums="1"
keytool -list -keystore ./cacerts-modified -storepass changeit | grep internal-ca
```

## Step 3: Mount the truststore into the container

Add a volume mount to your Compose file or Kubernetes manifest that replaces the
default truststore with the modified one.

=== "Docker Compose"

    ```yaml linenums="1"
    services:
      apiserver:
        image: ghcr.io/dependencytrack/hyades-apiserver:latest
        volumes:
          - "./cacerts-modified:/opt/java/openjdk/lib/security/cacerts:ro"
    ```

=== "Kubernetes"

    ```yaml linenums="1"
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: dt-truststore
    binaryData:
      cacerts: <base64-encoded contents of cacerts-modified>
    ---
    # In the Deployment spec:
    volumes:
      - name: truststore
        configMap:
          name: dt-truststore
    containers:
      - name: apiserver
        volumeMounts:
          - name: truststore
            mountPath: /opt/java/openjdk/lib/security/cacerts
            subPath: cacerts
            readOnly: true
    ```

    !!! tip
        For large or frequently rotated certificates, consider using a Secret or
        an init container to write the truststore rather than embedding it in a ConfigMap.

## Step 4: Restart the container

Recreate the container to pick up the new volume mount:

```shell
docker compose up -d --force-recreate apiserver
```

On the next startup, Dependency-Track uses the modified truststore and successfully
establishes TLS connections to endpoints signed by your internal CA.

## Troubleshooting

If connections still fail after mounting the truststore, verify that:

- The correct CA certificate was imported (not the server certificate itself).
- The `cacerts-modified` file is the one that was exported from the *current*
  version of the container image. After upgrading, re-export and re-import, since
  the base image's default truststore may change between releases.
- The volume mount path matches the Java home inside the container. To confirm,
  run `docker exec <container> readlink -f $(which java)` and trace up to the
  `lib/security/cacerts` path.
