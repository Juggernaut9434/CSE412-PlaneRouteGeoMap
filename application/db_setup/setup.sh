# MAKE SURE YOU ARE IN THE db_setup directory when executing
# MAKE SURE YOU HAVE PERMISSIONS TO WRITE TO A DATABASE

USERNAME=$(whoami)
DATABASE="flight_data"

psql -c "CREATE DATABASE flight_data WITH OWNER=$(whoami)"
psql $DATABASE -a -f ./create_tables.sql

psql $DATABASE -c "\\copy airline FROM 'airlines.dat' DELIMITER ',' CSV HEADER QUOTE '\"' NULL '\\N' ESCAPE ';'"
psql $DATABASE -c "\\copy country FROM 'countries.dat' DELIMITER ',' CSV HEADER QUOTE '\"' NULL '\\N' ESCAPE ';'"
psql $DATABASE -c "\\copy plane FROM 'planes.dat' DELIMITER ',' CSV HEADER QUOTE '\"' NULL '\\N' ESCAPE ';'"
psql $DATABASE -c "\\copy route FROM 'routes.dat' DELIMITER E'\t' CSV HEADER QUOTE '\"' NULL '\\N' ESCAPE ';'"
