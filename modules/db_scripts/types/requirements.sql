DROP TYPE IF EXISTS public.requirements;

CREATE TYPE public.requirements AS
(
	minimum text,
	recommended text
);

ALTER TYPE public.requirements
    OWNER TO postgres;
