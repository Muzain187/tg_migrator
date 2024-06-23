
# tg_migrator

`tg_migrator` is a migration tool for managing schema changes in graph databases, specifically designed to work with Tigergraph. Inspired by Alembic, `tg_migrator` offers a familiar interface for those who have worked with database migration tools in the SQL world but tailored for the unique requirements of graph databases.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Creating Migrations](#creating-migrations)
  - [Applying Migrations](#applying-migrations)
  - [Rolling Back Migrations](#rolling-back-migrations)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Introduction

`tg_migrator` helps you to version control your Tigergraph schema changes. Whether you're working on a single project or across multiple environments, `tg_migrator` ensures that your graph schema changes are tracked and reproducible.

## Features

- **Schema Versioning**: Track changes to your graph schema over time.
- **Rollback Support**: Easily revert changes if something goes wrong.
- **Environment Agnostic**: Manage migrations in development, testing, and production environments.
- **CLI Interface**: Command-line tools to simplify migration tasks.

## Installation

Install `tg_migrator` using pip:
```bash
cd dist
# choose tg_migrator version wheel file updated one
pip install tg_migrator-0.1.2-py3-none-any.whl
```

```bash
pip install tg_migrator
```

## Quick Start

To quickly get started with `tg_migrator`, follow these steps:

1. **Initialize Migration Directory**:
    ```bash
    tg_migrator init
    ```

2. **Create a New Migration**:
    ```bash
    tg_migrator create_version -m "Create vertex abc"
    ```

3. **Apply Migrations**:
    ```bash
    tg_migrator upgrade all
    ```

## Usage
## Version Management
tg_migrator uses a graph-based approach to manage migration versions:

Vertex: Each migration is represented as a tg_migrator vertex.
Edges:
next_version: Points to the next migration version.
previous_version: Points to the previous migration version.
active: Each migration vertex holds a status indicating whether it has been applied or not.
# Example Schema
![version_tree](https://github.com/Muzain187/tg_migrator/assets/60264379/4146ce12-be0b-4e3a-b38c-e78fc9a144f4)

![schema](https://github.com/Muzain187/tg_migrator/assets/60264379/ab528124-dc73-463e-963f-e293bc555ae8)




### Creating Migrations

Create a new migration file with a descriptive message:

```bash
tg_migrator create -m "Add new vertex type User"
```

This will generate a new migration script in your versions directory.

### Applying Migrations

To apply all pending migrations, run:

```bash
tg_migrator upgrade all
```

This will bring your database schema up to date with the latest changes.

### Rolling Back Migrations

To roll back the most recent migration, specify a specific version to downgrade to:


```bash
tg_migrator downgrade <version>
```

## Configuration

Configuration options can be specified in a configuration file or via environment variables. Here is an example configuration file:

```ini
[tg_migrator]
host_name = http://localhost:9000
secret = secret
tg_cloud = False
graph_name = graph_name
```



## License

This project is licensed under the MIT License. See the [LICENSE](License.txt) file for details.

## Author
Created by Mohammad Ashraf. You can reach me at [muzain.ashraf@gmail.com].

