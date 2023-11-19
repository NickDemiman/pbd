-- Type: platforms

-- DROP TYPE IF EXISTS public.platforms;

CREATE TYPE public.platforms AS
(
	windows boolean,
	mac boolean,
	linux boolean
);

ALTER TYPE public.platforms
    OWNER TO postgres;
