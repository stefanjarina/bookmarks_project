#!/usr/bin/env python3
import argparse
from pathlib import Path
import string
import sys
from utilities import create_path, copy_file, template_file

# CONSTANTS

BASE_PATH = Path(__file__).resolve().parent.parent  # path back to tools folder
CHOICES = ["backend", "frontend", "fullstack", "baas"]
PATHS = {
    "frontend": BASE_PATH.parent.joinpath("frontends"),
    "backend": BASE_PATH.parent.joinpath("backends"),
    "fullstack": BASE_PATH.joinpath("fullstack"),
    "baas": BASE_PATH.joinpath("baas"),
    "templates": BASE_PATH.joinpath("templates"),
}

# ARGUMENT PARSING

parser = argparse.ArgumentParser()
parser.add_argument(
    "type", help="type of project", choices=CHOICES)
parser.add_argument(
    "name", help="name of the project framework")
parser.add_argument("-p", "--port", dest="port", type=int,
                    default=3000, help="port for docker compose (default: 3000)")

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()

# RESOLVE PATH
try:
    path = Path(PATHS[args.type]).resolve()
    fullpath = path.joinpath(args.name)
except KeyError as e:
    print(f"{e} not supported choose either {CHOICES.join(', ')}")
    sys.exit(1)

create_path(fullpath)

# COPY BASE GITIGNORE
copy_file(PATHS["templates"].joinpath("git_specific", "gitignore"), fullpath, ".gitignore")

# COPY BASE DOCKERIGNORE
copy_file(PATHS["templates"].joinpath("docker", ".dockerignore"), fullpath, ".dockerignore")


if args.type == "frontend" or args.type == "fullstack":
    # COPY PRETTIER CONFIG
    copy_file(PATHS["templates"].joinpath("other", "prettierrc"), fullpath, ".prettierrc")


if args.type == "backend":
    dbPath = fullpath.joinpath("_db")
    create_path(dbPath)
    
    # TEMPLATE OUT create_db.sql
    template_file(PATHS["templates"].joinpath(*["db", "create_db.sql"]), dbPath, "create_db.sql", name=args.name)
    
    # TEMPLATE OUT drop_db.sql
    template_file(PATHS["templates"].joinpath(*["db", "drop_db.sql"]), dbPath, "drop_db.sql", name=args.name)

# TEMPLATE OUT README.md
template_file(PATHS["templates"].joinpath(*["git_specific", "README.md"]), fullpath, "README.md",
            additional_text=", please update it to match the framework and language",
            name=args.name, type=f"{args.type}s")

# TEMPLATE OUT DOCKER-COMPOSE
template_file(PATHS["templates"].joinpath(*["docker", "docker-compose.yml"]), fullpath, "docker-compose.yml", 
            additional_text=", please update exposed ports according to your specific needs", 
            name=args.name, port=args.port)
