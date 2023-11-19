-- Type: package_group

-- DROP TYPE IF EXISTS public.package_group;

CREATE TYPE public.package_group AS
(
	name character varying,
	title character varying,
	description character varying,
	selection_text character varying,
	save_text character varying,
	display_type integer,
	is_recurring_subscription character varying,
	subs bit(1)
);

ALTER TYPE public.package_group
    OWNER TO postgres;
