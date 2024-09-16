# Bookmarks {framework} ({language})

- {technology1}
- {technology2}
- {technology3}

## Docker

### Prepare database

It is adviced to use just scripts to create and setup database, but you can do it manually as well.

#### With script

```bash
# from root of this repository run
just db_up
just db_create
```

#### Manually

- Create network for containers

```bash
docker network create bookmarks
```

- Create Database container for PostgreSQL

```bash
docker run -d --net bookmarks -e "POSTGRES_PASSWORD=postgres" -v bookmarks-db-data:/var/lib/postgresql/data --name bm-postgresql-db -p 5432:5432 postgres:latest
```

- Copy SQL script to container

```bash
docker cp ./_db/* bm-postgresql-db:/
```

- Execute SQL script to create user and database

```bash
docker exec bm-postgresql-db /bin/sh -c 'psql -h localhost -U postgres -a -f /create_db.sql > /tmp/user_create.log 2>&1'
```

### Build image

```bash
# from root of this repository run
cd ${type}s/${name}
docker-compose up --build
```

### Build/Run APPLICATION with Docker-Compose

```bash
docker-compose up
docker-compose up --build  # to rebuild
```
