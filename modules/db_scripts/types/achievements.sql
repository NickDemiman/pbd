-- Type: achievements

-- DROP TYPE IF EXISTS public.achievements;

CREATE TYPE public.achievements AS
(
	total integer,
	highlighted achievement[]
);

ALTER TYPE public.achievements
    OWNER TO postgres;
