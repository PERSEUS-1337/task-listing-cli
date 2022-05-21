if [ -f .env ]
then
  export $(egrep -v '^#' .env | xargs)
  mysql -u $DB_USER -p$DB_PASSWORD < setup/database_setup.sql
fi
