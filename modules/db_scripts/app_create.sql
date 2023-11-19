DROP TABLE IF EXISTS public."App";

CREATE TABLE IF NOT EXISTS public."App"
(
    steam_appid bigint NOT NULL,
    name character varying COLLATE pg_catalog."default",
    type character varying COLLATE pg_catalog."default",
    required_age integer,
    is_free boolean,
    controller_support character varying COLLATE pg_catalog."default",
    detailed_description text COLLATE pg_catalog."default",
    about_the_game text COLLATE pg_catalog."default",
    short_description text COLLATE pg_catalog."default",
    supported_languages text COLLATE pg_catalog."default",
    header_image character varying COLLATE pg_catalog."default",
    website character varying COLLATE pg_catalog."default",
    pc_requirements requirements,
    mac_requirements requirements,
    linux_requirements requirements,
    legal_notice text COLLATE pg_catalog."default",
    developers character varying[] COLLATE pg_catalog."default",
    publishers character varying[] COLLATE pg_catalog."default",
    price_overview price_overview,
    packages bigint[],
    package_groups package_group[],
    platforms platforms,
    screenshots screenshot[],
    achievements achievements,
    release_date release_date,
    support_info support_info,
    background character varying COLLATE pg_catalog."default",
    background_raw character varying COLLATE pg_catalog."default",
    content_descriptors "char"[]
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."App"
    OWNER to postgres;