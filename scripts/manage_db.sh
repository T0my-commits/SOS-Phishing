source .env

# variables
OLD_DOCKER_NAME="CHANGEME"
OLD_DATABASE_NAME="CHANGEME"
NEW_DOCKER_NAME="CHANGEME"

# export postgre DB from docker
sudo docker exec -t sos_phishing-db-1 pg_dump -U $POSTGRES_USER -d $OLD_DATABASE_NAME > backup.sql

# get backup file on host machine
docker cp backend-db-1:/backup.sql ./backup.sql

# import backup into database
sudo docker exec -i backend-db-1 psql -U $POSTGRES_USER -d $POSTGRES_DB < ./backup.sql
