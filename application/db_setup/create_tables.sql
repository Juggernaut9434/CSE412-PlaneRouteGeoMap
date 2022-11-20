CREATE TABLE IF NOT EXISTS public.airline
(
    airline_id integer NOT NULL,
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    alias character varying(50) COLLATE pg_catalog."default",
    iata character(2) COLLATE pg_catalog."default",
    icao character(3) COLLATE pg_catalog."default",
    country character varying(100) COLLATE pg_catalog."default",
    callsign character varying(50) COLLATE pg_catalog."default",
    active character(1) COLLATE pg_catalog."default",
    CONSTRAINT airline_pkey PRIMARY KEY (airline_id)
);

CREATE TABLE IF NOT EXISTS public.airport
(
    airport_id integer NOT NULL,
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    city character varying(100) COLLATE pg_catalog."default" NOT NULL,
    country character varying(50) COLLATE pg_catalog."default" NOT NULL,
    iata character(3) COLLATE pg_catalog."default",
    icao character(4) COLLATE pg_catalog."default",
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    altitude integer NOT NULL,
    timezone numeric(2,0),
    dst character(1) COLLATE pg_catalog."default",
    tz character varying(100) COLLATE pg_catalog."default",
    type character varying(7) COLLATE pg_catalog."default" NOT NULL,
    source character varying(50) COLLATE pg_catalog."default",
    CONSTRAINT airport_pkey PRIMARY KEY (airport_id)
);

CREATE TABLE IF NOT EXISTS public.country
(
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    iso_code character(2) COLLATE pg_catalog."default",
    dafif_code character(2) COLLATE pg_catalog."default"
);

CREATE TABLE IF NOT EXISTS public.plane
(
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    iata character(3) COLLATE pg_catalog."default",
    icao character(4) COLLATE pg_catalog."default"
);

CREATE TABLE IF NOT EXISTS public.route
(
    airline character varying(5) COLLATE pg_catalog."default",
    airline_id integer,
    src_airport character varying(4) COLLATE pg_catalog."default",
    src_airport_id integer,
    dest_airport character varying(4) COLLATE pg_catalog."default",
    dest_airport_id integer,
    codeshare character(1) COLLATE pg_catalog."default",
    stops integer,
    equipment character varying(10)[] COLLATE pg_catalog."default"
);
