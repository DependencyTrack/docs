# Uploading BOMs

Dependency-Track builds a project's component inventory from the BOMs you upload.
Each upload starts vulnerability analysis and policy evaluation for the project.
Upload from the UI for a one-off, or from your pipeline so the inventory follows every build.

Uploading requires the `BOM_UPLOAD` [permission](../../reference/permissions.md).
Creating the project on first upload also requires `PROJECT_CREATION_UPLOAD`, `PORTFOLIO_MANAGEMENT`,
or `PORTFOLIO_MANAGEMENT_CREATE`. For pipelines, give these permissions to a
[service account](../../concepts/access-control.md#service-accounts) rather than to a person.

For the BOM formats Dependency-Track accepts, see [File formats](../../reference/file-formats.md).

## Upload from the UI

1. Open the project.
2. Select **Upload BOM**.
3. Select **Browse**, choose the BOM file, then select **Upload**.

<!-- vale Google.Headings = NO -->
## Upload via REST API
<!-- vale Google.Headings = YES -->

Send the BOM as a multipart request to `/api/v1/bom`:

=== "Bash"

    ```bash
    curl -sSf -X POST "https://dependency-track.example.com/api/v1/bom" \
      -H "X-Api-Key: ${DT_API_KEY}" \
      -F "projectName=my-app" \
      -F "projectVersion=1.2.3" \
      -F "autoCreate=true" \
      -F "bom=@bom.json"
    ```

=== "PowerShell"

    ```powershell
    Invoke-RestMethod -Method Post -Uri "https://dependency-track.example.com/api/v1/bom" `
      -Headers @{ "X-Api-Key" = $env:DT_API_KEY } `
      -Form @{
        projectName    = "my-app"
        projectVersion = "1.2.3"
        autoCreate     = "true"
        bom            = Get-Item "bom.json"
      }
    ```

Identify the target project with `project` (its UUID), **or** with `projectName` and `projectVersion`.
With `autoCreate=true`, Dependency-Track creates the project if it doesn't exist.
When it creates one, it also applies these optional fields:

* `parentUUID`, or `parentName` and `parentVersion`, to place the project in a [hierarchy](organizing-projects.md).
* `projectTags`, a comma-separated list of tags.
* `isLatest=true`, to mark the version as the [latest](managing-project-versions.md#mark-a-version-as-latest).

Send `isActive` only when you intend to change the project's active state.
It applies to existing projects too.

To save bandwidth on large BOMs, compress the file with either `gzip` or `zstd` and declare its type.
With curl, use for example `-F "bom=@bom.json.gz;type=application/gzip"`.
For `zstd`, use `application/zstd`.

A BOM that fails schema validation returns `400 Bad Request`.
For every field and response, see the `UploadBom` operation in the [REST API v1 reference](../../reference/api/v1.md).

To authenticate without a stored API key, exchange a platform token for a session as described in
[Configuring workload identity federation](../administration/configuring-workload-identity-federation.md#exchange-the-token-in-the-workload),
then send `Authorization: Bearer ${ACCESS_TOKEN}` instead of `X-Api-Key`.

## Wait for processing to finish

The upload returns as soon as Dependency-Track stores the BOM.
Processing continues in the background. The response carries a token that tracks it:

```json
{
  "token": "6a8d3bd2-3f7d-4b9c-9a54-7c1f0e1c2b4e",
  "projectUuid": "dadec8ad-7053-4e8c-8044-7b6ef698e08d"
}
```

If a later step needs the results, for example to fail the build on policy violations,
poll `/api/v1/event/token/{token}` until processing ends:

```json
{
  "processing": true,
  "status": "RUNNING"
}
```

`status` is `PENDING`, `RUNNING`, `COMPLETED`, or `FAILED`. The token covers the BOM import and the
vulnerability analysis and policy evaluation that follow, so `COMPLETED` means the project's
findings and policy violations reflect the uploaded BOM. For a token Dependency-Track doesn't
know, the response carries `"processing": false` and no `status`.

=== "Bash"

    ```bash
    TOKEN=$(curl -sSf -X POST "https://dependency-track.example.com/api/v1/bom" \
      -H "X-Api-Key: ${DT_API_KEY}" \
      -F "projectName=my-app" \
      -F "projectVersion=1.2.3" \
      -F "autoCreate=true" \
      -F "bom=@bom.json" \
      | jq -r .token)

    while true; do
      STATUS=$(curl -sSf -H "X-Api-Key: ${DT_API_KEY}" \
        "https://dependency-track.example.com/api/v1/event/token/${TOKEN}" \
        | jq -r '.status // "UNKNOWN"')
      case "${STATUS}" in
        COMPLETED) break ;;
        FAILED | UNKNOWN) echo "BOM processing ended with status ${STATUS}" >&2; exit 1 ;;
      esac
      sleep 5
    done
    ```

=== "PowerShell"

    ```powershell
    $headers = @{ "X-Api-Key" = $env:DT_API_KEY }
    $upload = Invoke-RestMethod -Method Post -Uri "https://dependency-track.example.com/api/v1/bom" `
      -Headers $headers `
      -Form @{
        projectName    = "my-app"
        projectVersion = "1.2.3"
        autoCreate     = "true"
        bom            = Get-Item "bom.json"
      }

    while ($true) {
      $status = (Invoke-RestMethod -Headers $headers `
        -Uri "https://dependency-track.example.com/api/v1/event/token/$($upload.token)").status ?? "UNKNOWN"
      if ($status -eq "COMPLETED") { break }
      if ($status -in "FAILED", "UNKNOWN") { throw "BOM processing ended with status $status" }
      Start-Sleep -Seconds 5
    }
    ```

Bound the loop with your CI system's job timeout.

<!-- vale Google.Headings = NO -->
## Upload from GitHub Actions
<!-- vale Google.Headings = YES -->

The [`gh-upload-sbom`](https://github.com/DependencyTrack/gh-upload-sbom) action wraps the upload request:

```yaml
- name: Upload BOM
  id: upload
  uses: DependencyTrack/gh-upload-sbom@v4
  with:
    server-hostname: dependency-track.example.com
    api-key: ${{ secrets.DEPENDENCYTRACK_APIKEY }}
    project-name: my-app
    project-version: ${{ github.ref_name }}
    bom-filename: bom.json
    auto-create: true
```

To authenticate without an API key secret, replace `api-key` with `workload-identity-provider`,
`service-account`, and `oidc-audience`, and grant the job `id-token: write`. See the action's
[workload identity federation](https://github.com/DependencyTrack/gh-upload-sbom#workload-identity-federation)
section, and [GitHub Actions](../administration/configuring-workload-identity-federation.md#github-actions)
for the Dependency-Track side.

The action doesn't wait for processing. It exposes the upload token as `steps.upload.outputs.token`,
so a later step can run the polling loop from [Wait for processing to finish](#wait-for-processing-to-finish)
with `TOKEN` set to that output.

<!-- vale Google.Headings = NO -->
## Upload from Jenkins
<!-- vale Google.Headings = YES -->

The [Dependency-Track Jenkins plugin](https://plugins.jenkins.io/dependency-track/) uploads BOMs as
a build step. See its documentation for setup. For other CI systems, call the REST API as shown in
[Upload via REST API](#upload-via-rest-api).
