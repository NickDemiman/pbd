CREATE OR REPLACE FUNCTION public.get_db_size_mb(
	name character varying)
    RETURNS text
    LANGUAGE 'sql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
select pg_database_size(name)/1024
$BODY$;

ALTER FUNCTION public.get_db_size_mb(character varying)
    OWNER TO postgres;
