-- Type: package

-- DROP TYPE IF EXISTS public."package";

CREATE TYPE public."package" AS
(
	packageid bigint,
	percent_savings_text character varying,
	percent_savings smallint,
	option_text text,
	option_description text,
	can_get_free_license character varying,
	is_free_license boolean,
	price_in_cents_with_discount bigint
);

ALTER TYPE public."package"
    OWNER TO postgres;
