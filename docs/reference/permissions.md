# Permissions

For background on how the access control model works (users, teams, ACLs), see
[Access control](../concepts/access-control.md).

## Permissions

Dependency-Track uses a two-level permission model. Coarse-grained permissions
(for example `PORTFOLIO_MANAGEMENT`) grant full access to a capability. Fine-grained
permissions (for example `PORTFOLIO_MANAGEMENT_CREATE`) allow restricting access to
specific operations. A coarse-grained permission implies all of its fine-grained
variants.

### Portfolio

For procedures, see [Organizing projects into hierarchies](../guides/user/organizing-projects.md)
and [Managing project versions](../guides/user/managing-project-versions.md).

| Permission                        | Description                                                            |
|:----------------------------------|:-----------------------------------------------------------------------|
| `BOM_UPLOAD`                      | Upload CycloneDX Software Bills of Materials.                          |
| `PROJECT_CREATION_UPLOAD`         | Auto-create a project on BOM upload if it does not exist.              |
| `VIEW_PORTFOLIO`                  | Read projects, components, licenses, the dependency graph, and metrics.|
| `PORTFOLIO_ACCESS_CONTROL_BYPASS` | Bypass portfolio access control, granting access to all projects.      |
| `PORTFOLIO_MANAGEMENT`            | Create, update, and delete projects and portfolio data.                |
| `PORTFOLIO_MANAGEMENT_CREATE`     | Create projects and portfolio data.                                    |
| `PORTFOLIO_MANAGEMENT_READ`       | Read portfolio data.                                                   |
| `PORTFOLIO_MANAGEMENT_UPDATE`     | Update projects and portfolio data.                                    |
| `PORTFOLIO_MANAGEMENT_DELETE`     | Delete projects and portfolio data.                                    |

### Vulnerability analysis

| Permission                        | Description                                                                      |
|:----------------------------------|:---------------------------------------------------------------------------------|
| `VIEW_VULNERABILITY`              | View vulnerabilities that affect projects.                                       |
| `VULNERABILITY_ANALYSIS`          | Make analysis decisions on vulnerabilities and manage VEX data.                   |
| `VULNERABILITY_ANALYSIS_CREATE`   | Upload VEX documents to a project.                                               |
| `VULNERABILITY_ANALYSIS_READ`     | Read VEX documents for a project.                                                |
| `VULNERABILITY_ANALYSIS_UPDATE`   | Make analysis decisions on vulnerabilities and upload VEX documents.              |

### Vulnerability management

| Permission                          | Description                                             |
|:------------------------------------|:--------------------------------------------------------|
| `VULNERABILITY_MANAGEMENT`          | Full management of internal vulnerabilities.  |
| `VULNERABILITY_MANAGEMENT_CREATE`   | Create internal vulnerabilities.              |
| `VULNERABILITY_MANAGEMENT_READ`     | Read internal vulnerabilities.                |
| `VULNERABILITY_MANAGEMENT_UPDATE`   | Update internal vulnerabilities and tags.     |
| `VULNERABILITY_MANAGEMENT_DELETE`   | Delete internal vulnerabilities.              |

### Policy management

| Permission                    | Description                                                      |
|:------------------------------|:-----------------------------------------------------------------|
| `POLICY_MANAGEMENT`           | Create, update, and delete policies, services, and license groups.|
| `POLICY_MANAGEMENT_CREATE`    | Create policies.                                                  |
| `POLICY_MANAGEMENT_READ`      | Read policies.                                                    |
| `POLICY_MANAGEMENT_UPDATE`    | Update policies.                                                  |
| `POLICY_MANAGEMENT_DELETE`    | Delete policies.                                                  |
| `POLICY_VIOLATION_ANALYSIS`   | Make analysis decisions on policy violations.                     |
| `VIEW_POLICY_VIOLATION`       | View policy violations across the portfolio.                      |

### Access management

| Permission                    | Description                                       |
|:------------------------------|:--------------------------------------------------|
| `ACCESS_MANAGEMENT`           | Manage users, teams, permissions, and API keys.   |
| `ACCESS_MANAGEMENT_CREATE`    | Create users, teams, and API keys.                |
| `ACCESS_MANAGEMENT_READ`      | Read users, teams, and API keys.                  |
| `ACCESS_MANAGEMENT_UPDATE`    | Update users, teams, and API keys.                |
| `ACCESS_MANAGEMENT_DELETE`    | Delete users, teams, and API keys.                |

### System configuration

| Permission                       | Description                                                                          |
|:---------------------------------|:-------------------------------------------------------------------------------------|
| `SYSTEM_CONFIGURATION`           | Full access to system configuration (notifications, repositories, email settings).   |
| `SYSTEM_CONFIGURATION_CREATE`    | Create system configuration entries.                                                 |
| `SYSTEM_CONFIGURATION_READ`      | Read system configuration.                                                           |
| `SYSTEM_CONFIGURATION_UPDATE`    | Update system configuration.                                                         |
| `SYSTEM_CONFIGURATION_DELETE`    | Delete system configuration entries.                                                 |

### Secret management

| Permission                    | Description                       |
|:------------------------------|:----------------------------------|
| `SECRET_MANAGEMENT`           | Full secret management access.    |
| `SECRET_MANAGEMENT_CREATE`    | Create secrets.                   |
| `SECRET_MANAGEMENT_UPDATE`    | Update secrets.                   |
| `SECRET_MANAGEMENT_DELETE`    | Delete secrets.                   |

### Tags

| Permission            | Description                              |
|:----------------------|:-----------------------------------------|
| `TAG_MANAGEMENT`      | Update and delete tags.                  |
| `TAG_MANAGEMENT_DELETE`| Delete tags.                            |

## Default teams

Dependency-Track creates the following default teams on first startup:

| Team            | Purpose                                                                                                                     |
|:----------------|:----------------------------------------------------------------------------------------------------------------------------|
| Administrators  | Full access. Used for initial setup and ongoing administration. Members receive all permissions.                             |
| Portfolio Managers | Intended for users who manage projects and portfolios without needing administrative access.                              |
| Automation      | Intended for CI/CD pipelines and automated tools. Typically holds `BOM_UPLOAD` and `PROJECT_CREATION_UPLOAD`.              |
