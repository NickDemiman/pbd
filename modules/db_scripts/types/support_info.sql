-- Type: support_info

-- DROP TYPE IF EXISTS public.support_info;

CREATE TYPE public.support_info AS
(
	url character varying,
	email character varying
);

ALTER TYPE public.support_info
    OWNER TO postgres;
