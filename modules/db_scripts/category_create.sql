DROP TABLE IF EXISTS public."Category";

CREATE TABLE IF NOT EXISTS public."Category"
(
    categoryid integer NOT NULL,
    type integer NOT NULL,
    internal_name character varying COLLATE pg_catalog."default" NOT NULL,
    display_name character varying COLLATE pg_catalog."default" NOT NULL,
    image_url character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Category_pkey" PRIMARY KEY (categoryid)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Category"
    OWNER to postgres;