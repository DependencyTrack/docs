# Quick start

In this tutorial, we will get Dependency-Track running locally using Docker Compose
and log in to the frontend for the first time.

## What we need

- [Docker](https://docs.docker.com/get-docker/) or [Podman](https://podman.io/)
- [Compose v2](https://docs.docker.com/compose/install/)

## Starting Dependency-Track

We download the Compose file and start the stack:

=== ":fontawesome-brands-linux: Linux / :fontawesome-brands-apple: macOS"

    ```shell
    curl -O https://raw.githubusercontent.com/DependencyTrack/docs/main/docs/tutorials/docker-compose.quickstart.yml
    docker compose -f docker-compose.quickstart.yml up
    ```

=== ":fontawesome-brands-windows: Windows (PowerShell)"

    ```powershell
    Invoke-WebRequest -Uri "https://raw.githubusercontent.com/DependencyTrack/docs/main/docs/tutorials/docker-compose.quickstart.yml" -OutFile "docker-compose.quickstart.yml"
    docker compose -f docker-compose.quickstart.yml up
    ```

This will pull the required images, initialize the database, and start all services.

??? note "Compose file contents"
    ```yaml
    --8<-- "docs/tutorials/docker-compose.quickstart.yml"
    ```

## Logging in

Once the stack is up, we open the frontend at **<http://localhost:8081>** and log in
with the default credentials:

| Username | Password |
|----------|----------|
| `admin`  | `admin`  |

!!! note
    Dependency-Track will ask us to change the password upon first login.

## What's next

- [Creating a component policy](creating-a-component-policy.md): Catch components that violate your standards
- [Setting up notifications](setting-up-notifications.md): Route events to Slack, email, or a webhook
- [Deploying to production](../guides/administration/deploying-to-production.md): Move from this quickstart to a real deployment
