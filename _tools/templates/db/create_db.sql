CREATE USER bm_${name} WITH PASSWORD 'bm_${name}';
CREATE DATABASE bm_${name};
GRANT ALL PRIVILEGES ON DATABASE bm_${name} TO bm_${name};
