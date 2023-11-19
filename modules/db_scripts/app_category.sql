DROP TABLE IF EXISTS public."App_Category";

CREATE TABLE IF NOT EXISTS public."App_Category"
(
    id serial NOT NULL,
    appid integer NOT NULL,
    categoryid integer NOT NULL,
    CONSTRAINT "App_Category_pkey" PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."App_Category"
    OWNER to postgres;