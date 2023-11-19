-- Type: screenshot

-- DROP TYPE IF EXISTS public.screenshot;

CREATE TYPE public.screenshot AS
(
	id bigint,
	path_thumbnail character varying,
	path_full character varying
);

ALTER TYPE public.screenshot
    OWNER TO postgres;
