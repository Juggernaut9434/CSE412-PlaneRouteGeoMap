ALTER TABLE IF EXISTS public.route
    ADD COLUMN route_id serial NOT NULL;
ALTER TABLE IF EXISTS public.route
    ADD PRIMARY KEY (route_id);

ALTER TABLE IF EXISTS public.plane
    ADD COLUMN plane_id serial NOT NULL;
ALTER TABLE IF EXISTS public.plane
    ADD PRIMARY KEY (plane_id);