# MAKE SURE YOU ARE IN THE db_setup directory when executing
# MAKE SURE YOU HAVE PERMISSIONS TO WRITE TO A DATABASE

USERNAME=$(whoami)
DATABASE="flight_data"

psql -c "CREATE DATABASE flight_data WITH OWNER=$(whoami)"
psql $DATABASE -a -f ./create_tables.sql

psql $DATABASE -c "\\copy airline FROM 'airlines.dat' DELIMITER ',' CSV HEADER QUOTE '\"' NULL '\\N' ESCAPE ';'"
psql $DATABASE -c "\\copy airport FROM 'airports.dat' DELIMITER ',' CSV HEADER QUOTE '\"' NULL '\\N' ESCAPE ';'"
psql $DATABASE -c "\\copy country FROM 'countries.dat' DELIMITER ',' CSV HEADER QUOTE '\"' NULL '\\N' ESCAPE ';'"
psql $DATABASE -c "\\copy plane FROM 'planes.dat' DELIMITER ',' CSV HEADER QUOTE '\"' NULL '\\N' ESCAPE ';'"
psql $DATABASE -c "\\copy route FROM 'routes.dat' DELIMITER E'\t' CSV HEADER QUOTE '\"' NULL '\\N' ESCAPE ';'"

# create indexes and views

psql $DATABASE -c 'CREATE OR REPLACE VIEW "routes_coor" AS 
SELECT airline, src.iata "src_iata", src.latitude "src_lat", src.longitude "src_long", 
dest.iata "dest_iata", dest.latitude "dest_lat", dest.longitude "dest_long",
src.city "src_city", dest.city "dest_city", src.country "src_country", dest.country "dest_country"
FROM route r
INNER JOIN airport as src ON src.iata = r.src_airport
INNER JOIN airport as dest ON dest.iata = r.dest_airport;'

psql $DATABASE -c 'CREATE INDEX IF NOT EXISTS "airport_iata"
ON airport USING hash (airport_id);'
