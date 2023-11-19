DROP TABLE IF EXISTS public."App_Tag";

CREATE TABLE IF NOT EXISTS public."App_Tag"
(
    id serial NOT NULL ,
    appid integer NOT NULL,
    tagid integer NOT NULL,
    CONSTRAINT "App_Tag_pkey" PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."App_Tag"
    OWNER to postgres;