import argparse
import os
import sys
from time import sleep
from utilities import call_command, call_command_and_capture

CONTAINER_NAME="bm-postgresql-db"

parser = argparse.ArgumentParser(description='Script to create a database for a specified backend.')
parser.add_argument("-n", "--name", dest="name", type=str, help="Name of the backend")
parser.add_argument("-s", "--script", dest="script", type=str, help="Name of the SQL script")

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()

root_path = os.path.join(os.path.dirname(__file__), '../../')
backend_path = os.path.join(root_path, 'backends', args.name)

if not os.path.exists(backend_path):
    print(f"'{args.name}' backend does not exist. Skipping...")
    sys.exit(0)

sql_file = os.path.abspath(os.path.join(backend_path, '_db', args.script))
if args.script == "create_db.sql":
    print(f"Creating database using '{sql_file}'")
if args.script == "drop_db.sql":
    print(f"Dropping database using '{sql_file}'")

call_command(f"docker cp {sql_file} {CONTAINER_NAME}:/{args.script}")
sleep(5)
rc, _, err = call_command_and_capture(f"docker exec {CONTAINER_NAME} /bin/sh -c 'psql -h localhost -U postgres -a -f /{args.script}'")

if rc == 0:
    if args.script == "create_db.sql":
        print("Database created")
    if args.script == "drop_db.sql":
        print("Database dropped")
else:
    if args.script == "create_db.sql":
        print("Error creating database. Exiting...")
    if args.script == "drop_db.sql":
        print("Error dropping database. Exiting...")
    print(err)
    sys.exit(1)
