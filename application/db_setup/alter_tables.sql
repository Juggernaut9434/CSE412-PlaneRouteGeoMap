ALTER TABLE IF EXISTS public.route
    ADD COLUMN route_id serial NOT NULL;
ALTER TABLE IF EXISTS public.route
    ADD PRIMARY KEY (route_id);

ALTER TABLE IF EXISTS public.plane
    ADD COLUMN plane_id serial NOT NULL;
ALTER TABLE IF EXISTS public.plane
    ADD PRIMARY KEY (plane_id);

CREATE OR REPLACE VIEW "routes_coor"
    AS
    SELECT airline,
        src.iata "src_iata", src.latitude "src_lat", src.longitude "src_long",
        dest.iata "dest_iata", dest.latitude "dest_lat", dest.longitude "dest_long",
        src.city "src_city", dest.city "dest_city",
        src.country "src_country", dest.country "dest_country"
    FROM route r
    INNER JOIN airport as src ON src.iata = r.src_airport
    INNER JOIN airport as dest ON dest.iata = r.dest_airport;

CREATE INDEX IF NOT EXISTS "airport_iata"
    ON airport
    USING hash (airport_id);