import sys
from utilities import call_command, call_command_and_capture

CONTAINER_NAME="bm-postgresql-db"
VOLUME_NAME="bookmarks-db-data"
NETWORK_NAME="bookmarks"
POSTGRES_PASSWORD="postgres"
POSTGRES_VERSION="latest"
POSTGRES_PORT="5432"
POSTGRES_PASSWORD="postgres"

def get_postgres():
    """Function to get the status of the PostgreSQL container"""
    return call_command_and_capture("docker container ls -a -f 'name=bm-postgresql-db' --format '{{.Status}}'")

_, network_status, _ = call_command_and_capture("docker network ls --filter 'name=^bookmarks$' --format '{{.Name}}'")

if not network_status:
    print("Network 'bookmarks' does not exist yet. Creating...")
    call_command("docker network create bookmarks")

_, status, _ = get_postgres()

if status:
    print("Container is already running. Skipping container creation...")
else:
    command = (f"docker run -d --net {NETWORK_NAME} -h db -e POSTGRES_PASSWORD={POSTGRES_PASSWORD} "
               f"-v {VOLUME_NAME}:/var/lib/postgresql/data --name {CONTAINER_NAME} "
               f"-p {POSTGRES_PORT}:5432 postgres:{POSTGRES_VERSION}")
    rc, _, _ = call_command_and_capture(command)
    if rc == 0:
        print("Container created")
    else:
        print("Error creating container. Exiting...")
        sys.exit(1)
