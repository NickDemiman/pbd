-- Type: release_date

-- DROP TYPE IF EXISTS public.release_date;

CREATE TYPE public.release_date AS
(
	coming_soon boolean,
	date date
);

ALTER TYPE public.release_date
    OWNER TO postgres;
