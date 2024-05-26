-- This script was generated by the ERD tool in pgAdmin 4.
-- Please log an issue at https://redmine.postgresql.org/projects/pgadmin4/issues/new if you find any bugs, including reproduction steps.
BEGIN;


CREATE TABLE IF NOT EXISTS public.users
(
    user_id bigserial NOT NULL,
    username character varying(64) NOT NULL,
    email character varying(100) NOT NULL,
    password character varying(255) NOT NULL,
    role character varying DEFAULT 'user',
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS public.room
(
    room_id serial NOT NULL,
    room_name character varying(100) NOT NULL,
    floor smallint,
    area character varying,
    PRIMARY KEY (room_id)
);

CREATE TABLE IF NOT EXISTS public.iot_device
(
    device_id serial NOT NULL,
    room_id integer NOT NULL,
    device_type character varying,
    status character varying,
    PRIMARY KEY (device_id)
);

CREATE TABLE IF NOT EXISTS public.energy_usage_data
(
    data_id serial NOT NULL,
    device_id integer NOT NULL,
    "timestamp" timestamp with time zone,
    energy_consumption double precision NOT NULL,
    PRIMARY KEY (data_id)
);


ALTER TABLE IF EXISTS public.iot_device
    ADD FOREIGN KEY (room_id)
    REFERENCES public.room (room_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.energy_usage_data
    ADD FOREIGN KEY (device_id)
    REFERENCES public.iot_device (device_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

END;