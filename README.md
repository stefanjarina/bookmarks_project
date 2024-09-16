# The Bookmarks Project

Showcase of simple Bookmarking application.

Written in several back-end frameworks and languages as well as in several modern front-end frameworks.

## Types of projects

- **frontend**: frameworks such as svelte, vue, react, blazor etc...
- **backend**: frameworks such as aspnet, gin, rails, phoenix, etc...
- **fullstack**: frameworks such as sveltekit, next, nuxt, astro, solidstart, etc...
- **baas**: config files for BaaS (e.g. supabase, appwrite)

## Required software for tooling (not frameworks themselves)

- [just](https://just.systems/) (make alternative to easily run scripts. You can always run them manually though)
- [python 3.10+](https://www.python.org/)
- [PowerShell 7+](https://github.com/PowerShell/PowerShell)
- [Docker](https://www.docker.com/products/docker-desktop/)

## JUST tasks

- create database

```bash
just db_up
```

- scaffold new project

```bash
# Create new project
just new frontend svelte
# Create new project with different port for docker compose
just new frontend svelte -p 3456
just new backend go
```

- remove project

```bash
just remove backend go
# Above is destructive action, confirmation will be needed, you can also pass --yes after just command
```

- prepare database and user

```bash
# below is automatically called by 'just new' task
# this only works for backends
just db_create go
```

- drop database

```bash
# below is automatically called by 'just remove' task
# this only works for backends
just db_drop go
# Above is destructive action, confirmation will be needed, you can also pass --yes after just command
```

- remove docker stuff

```bash
just db_down # removes both container and volume
just db_rm_c # removes only container
just db_rm_v # removes only volume
# Above are all destructive actions, confirmation will be needed, you can also pass --yes after just command
```

- list of available tasks

```bash
$ just
Available recipes:
    db_create NAME            # Prepare database
    db_down                   # Remove postgres docker container and volume
    db_drop NAME              # Drop database
    db_rm_c                   # Remove postgres docker container
    db_rm_v                   # Remove docker volume
    db_start                  # Start postgres docker container
    db_stop                   # Stop postgres docker container
    db_up                     # Create postgres docker container
    new TYPE NAME PORT='3000' # Create new project
    remove TYPE NAME          # Remove project
```

## Database

### Docker

If not using BaaS platform, then latest PostgreSQL is created and started in docker with default user and password

### Databases

For backend projects database with 'bm_%NAME%' is created with database, user names and password being the same
