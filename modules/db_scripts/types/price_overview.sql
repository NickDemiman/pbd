-- Type: price_overview

-- DROP TYPE IF EXISTS public.price_overview;

CREATE TYPE public.price_overview AS
(
	currency character varying,
	initial integer,
	final integer,
	discount_percent smallint,
	initial_formatted character varying,
	final_formatted character varying
);

ALTER TYPE public.price_overview
    OWNER TO postgres;
