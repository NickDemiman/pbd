-- Type: achievement

-- DROP TYPE IF EXISTS public.achievement;

CREATE TYPE public.achievement AS
(
	name character varying,
	path character varying
);

ALTER TYPE public.achievement
    OWNER TO postgres;
