set windows-shell := ["pwsh.exe", "-NoLogo", "-Command"]

container_name := "bm-postgresql-db"
volume_name := "bookmarks-db-data"

[private]
default:
  @just --list --justfile {{justfile()}}

# Create new project
@new TYPE NAME PORT='3000': && (db_create NAME)
  python3 ./_tools/scripts/init_new_project.py {{TYPE}} {{NAME}} -p {{PORT}}

# Remove project
[unix, confirm('This will remove the project. Are you sure?')]
@remove TYPE NAME: (db_drop NAME)
  if [ -d "./{{ TYPE }}s/{{NAME}}" ]; then rm -rf "./{{ TYPE }}s/{{NAME}}"; fi

# Remove project
[windows, confirm('This will remove the project. Are you sure?')]
@remove TYPE NAME: (db_drop NAME)
  if (Test-Path "./{{ TYPE }}s/{{NAME}}") { Remove-Item -Recurse -Force -Path "./{{ TYPE }}s/{{NAME}}" }

# Create postgres docker container
@db_up:
  python3 ./_tools/scripts/create_postgres.py

# Stop postgres docker container
@db_stop:
  docker container stop {{ container_name }}

# Start postgres docker container
@db_start:
  docker container start {{ container_name }}

# Remove postgres docker container and volume
[confirm('This will remove both docker container and volume. Are you sure?')]
@db_down:
  docker container rm {{ container_name }} --force
  docker volume rm {{ volume_name }}

# Remove postgres docker container
[confirm('This will remove docker container. Are you sure?')]
@db_rm_c:
  docker container rm {{ container_name }} --force

# Remove docker volume
[confirm('This will remove docker volume. Are you sure?')]
@db_rm_v:
  docker volume rm {{ volume_name }}

# Prepare database
@db_create NAME:
  python3 ./_tools/scripts/run_sql_script.py -n {{NAME}} -s "create_db.sql"

# Drop database
[confirm('This will remove database and user inside postgres. Are you sure?')]
@db_drop NAME:
  python3 ./_tools/scripts/run_sql_script.py -n {{ NAME }} -s "drop_db.sql"
