DROP TABLE IF EXISTS public."Tag";

CREATE TABLE IF NOT EXISTS public."Tag"
(
    tagid integer NOT NULL,
    name character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Tag_pkey" PRIMARY KEY (tagid)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Tag"
    OWNER to postgres;