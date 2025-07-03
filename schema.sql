--
-- PostgreSQL database dump
--

-- Dumped from database version 17.1
-- Dumped by pg_dump version 17.2 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: color_type; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.color_type AS ENUM (
    'Interior',
    'Exterior'
);


--
-- Name: condition_type; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.condition_type AS ENUM (
    'New',
    'Used',
    'Unknown'
);


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: audit_trails; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.audit_trails (
    id integer NOT NULL,
    vehicle_id integer,
    user_id integer,
    action character varying(50),
    action_timestamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    ip_address character varying(45)
);


--
-- Name: audit_trails_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.audit_trails_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: audit_trails_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.audit_trails_id_seq OWNED BY public.audit_trails.id;


--
-- Name: base_vehicles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.base_vehicles (
    id integer NOT NULL,
    make_id integer NOT NULL,
    model_id integer NOT NULL,
    trim_id integer NOT NULL,
    manufacture_year_id integer NOT NULL,
    exterior_color_id integer,
    interior_color_id integer,
    body_type_id integer,
    door_id integer,
    seat_id integer,
    engine_id integer,
    transmission_id integer,
    drive_train_id integer,
    fuel_type_id integer,
    fuel_tank_capacity_gal numeric(4,2),
    epa_metrics_id integer,
    torque_id integer
);


--
-- Name: base_vehicles_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.base_vehicles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: base_vehicles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.base_vehicles_id_seq OWNED BY public.base_vehicles.id;


--
-- Name: body_types; Type: TABLE; Schema: public; Owner: -
--

DROP SEQUENCE IF EXISTS public.body_types_id_seq CASCADE;

CREATE SEQUENCE IF NOT EXISTS public.body_types_id_seq;

CREATE TABLE IF NOT EXISTS public.body_types (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);


--
-- Name: colors; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.colors (
    id integer NOT NULL,
    name character varying(50) DEFAULT 'Unknown'::character varying,
    hex_code character varying(7) DEFAULT '#000000'::character varying
);


--
-- Name: colors_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.colors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: colors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.colors_id_seq OWNED BY public.colors.id;


--
-- Name: conditions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.conditions (
    id integer NOT NULL,
    type public.condition_type DEFAULT 'Unknown'::public.condition_type
);


--
-- Name: conditions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.conditions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: conditions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.conditions_id_seq OWNED BY public.conditions.id;


--
-- Name: doors; Type: TABLE; Schema: public; Owner: -
--

DROP SEQUENCE IF EXISTS public.doors_id_seq CASCADE;

CREATE SEQUENCE IF NOT EXISTS public.doors_id_seq;

CREATE TABLE IF NOT EXISTS public.doors (
    id SERIAL PRIMARY KEY,
    number_of_doors INT NOT NULL UNIQUE
);


--
-- Name: drive_trains; Type: TABLE; Schema: public; Owner: -
--

DROP SEQUENCE IF EXISTS public.drive_trains_id_seq CASCADE;

CREATE SEQUENCE IF NOT EXISTS public.drive_trains_id_seq;

CREATE TABLE IF NOT EXISTS public.drive_trains (
    id SERIAL PRIMARY KEY,
    type TEXT NOT NULL UNIQUE
);


--
-- Name: engine_types; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.engine_types (
    id integer NOT NULL,
    name character varying(50) DEFAULT 'Unknown'::character varying
);


--
-- Name: engine_types_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.engine_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: engine_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.engine_types_id_seq OWNED BY public.engine_types.id;


--
-- Name: engines; Type: TABLE; Schema: public; Owner: -
--

DROP SEQUENCE IF EXISTS public.engines_id_seq CASCADE;

CREATE SEQUENCE IF NOT EXISTS public.engines_id_seq;

CREATE TABLE IF NOT EXISTS public.engines (
    id SERIAL PRIMARY KEY,
    engine_type_id INT NOT NULL,
    cylinders INT,
    engine_size_l FLOAT,
    horsepower INT
);


--
-- Name: epa_metrics; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.epa_metrics (
    id integer NOT NULL,
    epa_combined_mpg numeric(4,1),
    epa_city_mpg numeric(4,1),
    epa_highway_mpg numeric(4,1),
    epa_electric_range_mi numeric(5,1),
    epa_time_to_charge_240v_hr numeric(4,1),
    battery_capacity_kwh numeric(5,1)
);


--
-- Name: epa_metrics_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.epa_metrics_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: epa_metrics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.epa_metrics_id_seq OWNED BY public.epa_metrics.id;


--
-- Name: fuel_types; Type: TABLE; Schema: public; Owner: -
--

DROP SEQUENCE IF EXISTS public.fuel_types_id_seq CASCADE;

CREATE SEQUENCE IF NOT EXISTS public.fuel_types_id_seq;

CREATE TABLE IF NOT EXISTS public.fuel_types (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);


--
-- Name: historical_data; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.historical_data (
    id integer NOT NULL,
    vehicle_id integer NOT NULL,
    listing_year_id integer NOT NULL,
    price numeric(10,2),
    mileage integer,
    msrp numeric(10,2),
    date_captured timestamp without time zone,
    date_archived timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    source_id integer NOT NULL
);


--
-- Name: historical_data_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.historical_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: historical_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.historical_data_id_seq OWNED BY public.historical_data.id;


--
-- Name: listing_years; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.listing_years (
    id integer NOT NULL,
    year smallint
);


--
-- Name: listing_years_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.listing_years_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: listing_years_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.listing_years_id_seq OWNED BY public.listing_years.id;


--
-- Name: live_scraped_data; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.live_scraped_data (
    id integer NOT NULL,
    vehicle_id integer NOT NULL,
    listing_year_id integer NOT NULL,
    price numeric(10,2),
    mileage integer,
    msrp numeric(10,2),
    date_captured timestamp without time zone,
    source_id integer NOT NULL
);


--
-- Name: live_scraped_data_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.live_scraped_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: live_scraped_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.live_scraped_data_id_seq OWNED BY public.live_scraped_data.id;


--
-- Name: locations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.locations (
    id integer NOT NULL,
    state character varying(50),
    city character varying(100),
    county character varying(100),
    zipcode character varying(10),
    region character varying(100)
);


--
-- Name: locations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.locations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: locations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.locations_id_seq OWNED BY public.locations.id;


--
-- Name: makes; Type: TABLE; Schema: public; Owner: -
--

DROP SEQUENCE IF EXISTS public.makes_id_seq CASCADE;

CREATE SEQUENCE IF NOT EXISTS public.makes_id_seq;

CREATE TABLE IF NOT EXISTS public.makes (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS public.models (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    make_id INT NOT NULL REFERENCES public.makes(id),
    UNIQUE (make_id, name)
);

CREATE TABLE IF NOT EXISTS public.trims (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    model_id INT NOT NULL REFERENCES public.models(id),
    description TEXT,
    UNIQUE (model_id, name)
);


--
-- Name: manufacturing_years; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.manufacturing_years (
    id integer NOT NULL,
    year smallint NOT NULL
);


--
-- Name: manufacturing_years_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.manufacturing_years_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: manufacturing_years_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.manufacturing_years_id_seq OWNED BY public.manufacturing_years.id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.roles (
    id integer NOT NULL,
    name character varying(50) NOT NULL
);


--
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- Name: seats; Type: TABLE; Schema: public; Owner: -
--

DROP SEQUENCE IF EXISTS public.seats_id_seq CASCADE;

CREATE SEQUENCE IF NOT EXISTS public.seats_id_seq;

CREATE TABLE IF NOT EXISTS public.seats (
    id SERIAL PRIMARY KEY,
    number_of_seats INT NOT NULL UNIQUE
);


--
-- Name: sources; Type: TABLE; Schema: public; Owner: -
--

DROP SEQUENCE IF EXISTS public.sources_id_seq CASCADE;

CREATE SEQUENCE IF NOT EXISTS public.sources_id_seq;

CREATE TABLE IF NOT EXISTS public.sources (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    source_url TEXT
);


--
-- Name: tags; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tags (
    id integer NOT NULL,
    name character varying(50)
);


--
-- Name: tags_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tags_id_seq OWNED BY public.tags.id;


--
-- Name: title_statuses; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.title_statuses (
    id integer NOT NULL,
    status character varying(50)
);


--
-- Name: title_statuses_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.title_statuses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: title_statuses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.title_statuses_id_seq OWNED BY public.title_statuses.id;


--
-- Name: torque; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.torque (
    id integer NOT NULL,
    torque_ft_lbs integer,
    torque_rpm integer
);


--
-- Name: torque_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.torque_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: torque_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.torque_id_seq OWNED BY public.torque.id;


--
-- Name: transmissions; Type: TABLE; Schema: public; Owner: -
--

DROP SEQUENCE IF EXISTS public.transmissions_id_seq CASCADE;

CREATE SEQUENCE IF NOT EXISTS public.transmissions_id_seq;

CREATE TABLE IF NOT EXISTS public.transmissions (
    id SERIAL PRIMARY KEY,
    type TEXT NOT NULL UNIQUE
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    password_hash character varying(255) NOT NULL,
    role_id integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: vehicle_colors; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.vehicle_colors (
    id integer NOT NULL,
    vehicle_id integer NOT NULL,
    color_id integer NOT NULL,
    color_type public.color_type NOT NULL
);


--
-- Name: vehicle_colors_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.vehicle_colors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: vehicle_colors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.vehicle_colors_id_seq OWNED BY public.vehicle_colors.id;


--
-- Name: vehicle_tags; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.vehicle_tags (
    vehicle_id integer NOT NULL,
    tag_id integer NOT NULL
);


--
-- Name: vehicles; Type: TABLE; Schema: public; Owner: -
--

DROP SEQUENCE IF EXISTS public.vehicles_id_seq CASCADE;

CREATE SEQUENCE IF NOT EXISTS public.vehicles_id_seq;

CREATE TABLE IF NOT EXISTS public.vehicles (
    id SERIAL PRIMARY KEY,
    base_vehicle_id INT NOT NULL,
    location_id INT NOT NULL,
    listing_year_id INT NOT NULL,
    vin TEXT NOT NULL UNIQUE,
    price FLOAT,
    msrp FLOAT,
    mileage INT,
    title_status_id INT,
    condition_id INT,
    days_on_market INT,
    date_captured TIMESTAMP,
    date_added TIMESTAMP,
    date_modified TIMESTAMP
);


--
-- Name: audit_trails id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_trails ALTER COLUMN id SET DEFAULT nextval('public.audit_trails_id_seq'::regclass);


--
-- Name: base_vehicles id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.base_vehicles ALTER COLUMN id SET DEFAULT nextval('public.base_vehicles_id_seq'::regclass);


--
-- Name: body_types id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.body_types ALTER COLUMN id SET DEFAULT nextval('public.body_types_id_seq'::regclass);


--
-- Name: colors id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.colors ALTER COLUMN id SET DEFAULT nextval('public.colors_id_seq'::regclass);


--
-- Name: conditions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.conditions ALTER COLUMN id SET DEFAULT nextval('public.conditions_id_seq'::regclass);


--
-- Name: doors id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.doors ALTER COLUMN id SET DEFAULT nextval('public.doors_id_seq'::regclass);


--
-- Name: drive_trains id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.drive_trains ALTER COLUMN id SET DEFAULT nextval('public.drive_trains_id_seq'::regclass);


--
-- Name: engine_types id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.engine_types ALTER COLUMN id SET DEFAULT nextval('public.engine_types_id_seq'::regclass);


--
-- Name: engines id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.engines ALTER COLUMN id SET DEFAULT nextval('public.engines_id_seq'::regclass);


--
-- Name: epa_metrics id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.epa_metrics ALTER COLUMN id SET DEFAULT nextval('public.epa_metrics_id_seq'::regclass);


--
-- Name: fuel_types id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fuel_types ALTER COLUMN id SET DEFAULT nextval('public.fuel_types_id_seq'::regclass);


--
-- Name: historical_data id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.historical_data ALTER COLUMN id SET DEFAULT nextval('public.historical_data_id_seq'::regclass);


--
-- Name: listing_years id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.listing_years ALTER COLUMN id SET DEFAULT nextval('public.listing_years_id_seq'::regclass);


--
-- Name: live_scraped_data id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.live_scraped_data ALTER COLUMN id SET DEFAULT nextval('public.live_scraped_data_id_seq'::regclass);


--
-- Name: locations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.locations ALTER COLUMN id SET DEFAULT nextval('public.locations_id_seq'::regclass);


--
-- Name: makes id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.makes ALTER COLUMN id SET DEFAULT nextval('public.makes_id_seq'::regclass);


--
-- Name: manufacturing_years id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.manufacturing_years ALTER COLUMN id SET DEFAULT nextval('public.manufacturing_years_id_seq'::regclass);


--
-- Name: models id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.models ALTER COLUMN id SET DEFAULT nextval('public.models_id_seq'::regclass);


--
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- Name: seats id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.seats ALTER COLUMN id SET DEFAULT nextval('public.seats_id_seq'::regclass);


--
-- Name: sources id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sources ALTER COLUMN id SET DEFAULT nextval('public.sources_id_seq'::regclass);


--
-- Name: tags id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tags ALTER COLUMN id SET DEFAULT nextval('public.tags_id_seq'::regclass);


--
-- Name: title_statuses id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.title_statuses ALTER COLUMN id SET DEFAULT nextval('public.title_statuses_id_seq'::regclass);


--
-- Name: torque id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.torque ALTER COLUMN id SET DEFAULT nextval('public.torque_id_seq'::regclass);


--
-- Name: transmissions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.transmissions ALTER COLUMN id SET DEFAULT nextval('public.transmissions_id_seq'::regclass);


--
-- Name: trims id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trims ALTER COLUMN id SET DEFAULT nextval('public.trims_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: vehicle_colors id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_colors ALTER COLUMN id SET DEFAULT nextval('public.vehicle_colors_id_seq'::regclass);


--
-- Name: vehicles id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicles ALTER COLUMN id SET DEFAULT nextval('public.vehicles_id_seq'::regclass);


--
-- Name: audit_trails audit_trails_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_trails
    ADD CONSTRAINT audit_trails_pkey PRIMARY KEY (id);


--
-- Name: base_vehicles base_vehicles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.base_vehicles
    ADD CONSTRAINT base_vehicles_pkey PRIMARY KEY (id);


--
-- Name: body_types body_types_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.body_types
    ADD CONSTRAINT body_types_name_key UNIQUE (name);


--
-- Name: body_types body_types_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.body_types
    ADD CONSTRAINT body_types_pkey PRIMARY KEY (id);


--
-- Name: colors colors_hexcode_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.colors
    ADD CONSTRAINT colors_hexcode_key UNIQUE (hex_code);


--
-- Name: colors colors_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.colors
    ADD CONSTRAINT colors_name_key UNIQUE (name);


--
-- Name: colors colors_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.colors
    ADD CONSTRAINT colors_pkey PRIMARY KEY (id);


--
-- Name: conditions conditions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.conditions
    ADD CONSTRAINT conditions_pkey PRIMARY KEY (id);


--
-- Name: conditions conditions_type_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.conditions
    ADD CONSTRAINT conditions_type_key UNIQUE (type);


--
-- Name: doors doors_number_of_doors_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.doors
    ADD CONSTRAINT doors_number_of_doors_key UNIQUE (number_of_doors);


--
-- Name: doors doors_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.doors
    ADD CONSTRAINT doors_pkey PRIMARY KEY (id);


--
-- Name: drive_trains drive_trains_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.drive_trains
    ADD CONSTRAINT drive_trains_pkey PRIMARY KEY (id);


--
-- Name: drive_trains drive_trains_type_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.drive_trains
    ADD CONSTRAINT drive_trains_type_key UNIQUE (type);


--
-- Name: engine_types engine_types_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.engine_types
    ADD CONSTRAINT engine_types_name_key UNIQUE (name);


--
-- Name: engine_types engine_types_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.engine_types
    ADD CONSTRAINT engine_types_pkey PRIMARY KEY (id);


--
-- Name: engines engines_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.engines
    ADD CONSTRAINT engines_pkey PRIMARY KEY (id);


--
-- Name: epa_metrics epa_metrics_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.epa_metrics
    ADD CONSTRAINT epa_metrics_pkey PRIMARY KEY (id);


--
-- Name: fuel_types fuel_types_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fuel_types
    ADD CONSTRAINT fuel_types_name_key UNIQUE (name);


--
-- Name: fuel_types fuel_types_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fuel_types
    ADD CONSTRAINT fuel_types_pkey PRIMARY KEY (id);


--
-- Name: historical_data historical_data_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.historical_data
    ADD CONSTRAINT historical_data_pkey PRIMARY KEY (id);


--
-- Name: listing_years listing_years_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.listing_years
    ADD CONSTRAINT listing_years_pkey PRIMARY KEY (id);


--
-- Name: listing_years listing_years_year_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.listing_years
    ADD CONSTRAINT listing_years_year_key UNIQUE (year);


--
-- Name: live_scraped_data live_scraped_data_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.live_scraped_data
    ADD CONSTRAINT live_scraped_data_pkey PRIMARY KEY (id);


--
-- Name: locations locations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT locations_pkey PRIMARY KEY (id);


--
-- Name: makes makes_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.makes
    ADD CONSTRAINT makes_name_key UNIQUE (name);


--
-- Name: makes makes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.makes
    ADD CONSTRAINT makes_pkey PRIMARY KEY (id);


--
-- Name: manufacturing_years manufacturing_years_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.manufacturing_years
    ADD CONSTRAINT manufacturing_years_pkey PRIMARY KEY (id);


--
-- Name: manufacturing_years manufacturing_years_year_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.manufacturing_years
    ADD CONSTRAINT manufacturing_years_year_key UNIQUE (year);


--
-- Name: models models_make_id_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.models
    ADD CONSTRAINT models_make_id_name_key UNIQUE (make_id, name);


--
-- Name: models models_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.models
    ADD CONSTRAINT models_pkey PRIMARY KEY (id);


--
-- Name: roles roles_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_name_key UNIQUE (name);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: seats seats_number_of_seats_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.seats
    ADD CONSTRAINT seats_number_of_seats_key UNIQUE (number_of_seats);


--
-- Name: seats seats_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.seats
    ADD CONSTRAINT seats_pkey PRIMARY KEY (id);


--
-- Name: sources sources_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sources
    ADD CONSTRAINT sources_name_key UNIQUE (name);


--
-- Name: sources sources_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sources
    ADD CONSTRAINT sources_pkey PRIMARY KEY (id);


--
-- Name: tags tags_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_name_key UNIQUE (name);


--
-- Name: tags tags_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (id);


--
-- Name: title_statuses title_statuses_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.title_statuses
    ADD CONSTRAINT title_statuses_pkey PRIMARY KEY (id);


--
-- Name: title_statuses title_statuses_status_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.title_statuses
    ADD CONSTRAINT title_statuses_status_key UNIQUE (status);


--
-- Name: torque torque_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.torque
    ADD CONSTRAINT torque_pkey PRIMARY KEY (id);


--
-- Name: transmissions transmissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.transmissions
    ADD CONSTRAINT transmissions_pkey PRIMARY KEY (id);


--
-- Name: transmissions transmissions_type_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.transmissions
    ADD CONSTRAINT transmissions_type_key UNIQUE (type);


--
-- Name: trims trims_model_id_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trims
    ADD CONSTRAINT trims_model_id_name_key UNIQUE (model_id, name);


--
-- Name: trims trims_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trims
    ADD CONSTRAINT trims_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: vehicle_colors vehicle_colors_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_colors
    ADD CONSTRAINT vehicle_colors_pkey PRIMARY KEY (id);


--
-- Name: vehicle_tags vehicle_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_tags
    ADD CONSTRAINT vehicle_tags_pkey PRIMARY KEY (vehicle_id, tag_id);


--
-- Name: vehicles vehicles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicles
    ADD CONSTRAINT vehicles_pkey PRIMARY KEY (id);


--
-- Name: vehicles vehicles_vin_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicles
    ADD CONSTRAINT vehicles_vin_key UNIQUE (vin);


--
-- Name: audit_trails audit_trails_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_trails
    ADD CONSTRAINT audit_trails_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: audit_trails audit_trails_vehicle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audit_trails
    ADD CONSTRAINT audit_trails_vehicle_id_fkey FOREIGN KEY (vehicle_id) REFERENCES public.vehicles(id);


--
-- Name: base_vehicles base_vehicles_body_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.base_vehicles
    ADD CONSTRAINT base_vehicles_body_type_id_fkey FOREIGN KEY (body_type_id) REFERENCES public.body_types(id);


--
-- Name: base_vehicles base_vehicles_door_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.base_vehicles
    ADD CONSTRAINT base_vehicles_door_id_fkey FOREIGN KEY (door_id) REFERENCES public.doors(id);


--
-- Name: base_vehicles base_vehicles_drive_train_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.base_vehicles
    ADD CONSTRAINT base_vehicles_drive_train_id_fkey FOREIGN KEY (drive_train_id) REFERENCES public.drive_trains(id);


--
-- Name: base_vehicles base_vehicles_engine_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.base_vehicles
    ADD CONSTRAINT base_vehicles_engine_id_fkey FOREIGN KEY (engine_id) REFERENCES public.engines(id);


--
-- Name: base_vehicles base_vehicles_epa_metrics_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.base_vehicles
    ADD CONSTRAINT base_vehicles_epa_metrics_id_fkey FOREIGN KEY (epa_metrics_id) REFERENCES public.epa_metrics(id);


--
-- Name: base_vehicles base_vehicles_exterior_color_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.base_vehicles
    ADD CONSTRAINT base_vehicles_exterior_color_id_fkey FOREIGN KEY (exterior_color_id) REFERENCES public.colors(id);


--
-- Name: base_vehicles base_vehicles_fuel_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.base_vehicles
    ADD CONSTRAINT base_vehicles_fuel_type_id_fkey FOREIGN KEY (fuel_type_id) REFERENCES public.fuel_types(id);


--
-- Name: base_vehicles base_vehicles_interior_color_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.base_vehicles
    ADD CONSTRAINT base_vehicles_interior_color_id_fkey FOREIGN KEY (interior_color_id) REFERENCES public.colors(id);


--
-- Name: base_vehicles base_vehicles_make_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.base_vehicles
    ADD CONSTRAINT base_vehicles_make_id_fkey FOREIGN KEY (make_id) REFERENCES public.makes(id);


--
-- Name: base_vehicles base_vehicles_manufacture_year_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.base_vehicles
    ADD CONSTRAINT base_vehicles_manufacture_year_id_fkey FOREIGN KEY (manufacture_year_id) REFERENCES public.manufacturing_years(id);


--
-- Name: base_vehicles base_vehicles_model_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.base_vehicles
    ADD CONSTRAINT base_vehicles_model_id_fkey FOREIGN KEY (model_id) REFERENCES public.models(id);


--
-- Name: base_vehicles base_vehicles_seat_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.base_vehicles
    ADD CONSTRAINT base_vehicles_seat_id_fkey FOREIGN KEY (seat_id) REFERENCES public.seats(id);


--
-- Name: base_vehicles base_vehicles_torque_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.base_vehicles
    ADD CONSTRAINT base_vehicles_torque_id_fkey FOREIGN KEY (torque_id) REFERENCES public.torque(id);


--
-- Name: base_vehicles base_vehicles_transmission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.base_vehicles
    ADD CONSTRAINT base_vehicles_transmission_id_fkey FOREIGN KEY (transmission_id) REFERENCES public.transmissions(id);


--
-- Name: base_vehicles base_vehicles_trim_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.base_vehicles
    ADD CONSTRAINT base_vehicles_trim_id_fkey FOREIGN KEY (trim_id) REFERENCES public.trims(id);


--
-- Name: engines engines_engine_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.engines
    ADD CONSTRAINT engines_engine_type_id_fkey FOREIGN KEY (engine_type_id) REFERENCES public.engine_types(id) ON DELETE CASCADE;


--
-- Name: historical_data historical_data_listing_year_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.historical_data
    ADD CONSTRAINT historical_data_listing_year_id_fkey FOREIGN KEY (listing_year_id) REFERENCES public.listing_years(id);


--
-- Name: historical_data historical_data_source_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.historical_data
    ADD CONSTRAINT historical_data_source_id_fkey FOREIGN KEY (source_id) REFERENCES public.sources(id) ON DELETE CASCADE;


--
-- Name: historical_data historical_data_vehicle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.historical_data
    ADD CONSTRAINT historical_data_vehicle_id_fkey FOREIGN KEY (vehicle_id) REFERENCES public.vehicles(id) ON DELETE CASCADE;


--
-- Name: live_scraped_data live_scraped_data_listing_year_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.live_scraped_data
    ADD CONSTRAINT live_scraped_data_listing_year_id_fkey FOREIGN KEY (listing_year_id) REFERENCES public.listing_years(id);


--
-- Name: live_scraped_data live_scraped_data_source_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.live_scraped_data
    ADD CONSTRAINT live_scraped_data_source_id_fkey FOREIGN KEY (source_id) REFERENCES public.sources(id) ON DELETE CASCADE;


--
-- Name: live_scraped_data live_scraped_data_vehicle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.live_scraped_data
    ADD CONSTRAINT live_scraped_data_vehicle_id_fkey FOREIGN KEY (vehicle_id) REFERENCES public.vehicles(id) ON DELETE CASCADE;


--
-- Name: models models_make_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.models
    ADD CONSTRAINT models_make_id_fkey FOREIGN KEY (make_id) REFERENCES public.makes(id) ON DELETE CASCADE;


--
-- Name: trims trims_model_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.trims
    ADD CONSTRAINT trims_model_id_fkey FOREIGN KEY (model_id) REFERENCES public.models(id) ON DELETE CASCADE;


--
-- Name: users users_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id) ON DELETE CASCADE;


--
-- Name: vehicle_colors vehicle_colors_color_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_colors
    ADD CONSTRAINT vehicle_colors_color_id_fkey FOREIGN KEY (color_id) REFERENCES public.colors(id);


--
-- Name: vehicle_colors vehicle_colors_vehicle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_colors
    ADD CONSTRAINT vehicle_colors_vehicle_id_fkey FOREIGN KEY (vehicle_id) REFERENCES public.vehicles(id) ON DELETE CASCADE;


--
-- Name: vehicle_tags vehicle_tags_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_tags
    ADD CONSTRAINT vehicle_tags_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES public.tags(id) ON DELETE CASCADE;


--
-- Name: vehicle_tags vehicle_tags_vehicle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicle_tags
    ADD CONSTRAINT vehicle_tags_vehicle_id_fkey FOREIGN KEY (vehicle_id) REFERENCES public.vehicles(id) ON DELETE CASCADE;


--
-- Name: vehicles vehicles_base_vehicle_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicles
    ADD CONSTRAINT vehicles_base_vehicle_id_fkey FOREIGN KEY (base_vehicle_id) REFERENCES public.trims(id);


--
-- Name: vehicles vehicles_condition_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicles
    ADD CONSTRAINT vehicles_condition_id_fkey FOREIGN KEY (condition_id) REFERENCES public.conditions(id);


--
-- Name: vehicles vehicles_listing_year_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicles
    ADD CONSTRAINT vehicles_listing_year_id_fkey FOREIGN KEY (listing_year_id) REFERENCES public.listing_years(id);


--
-- Name: vehicles vehicles_location_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicles
    ADD CONSTRAINT vehicles_location_id_fkey FOREIGN KEY (location_id) REFERENCES public.locations(id);


--
-- Name: vehicles vehicles_title_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vehicles
    ADD CONSTRAINT vehicles_title_status_id_fkey FOREIGN KEY (title_status_id) REFERENCES public.title_statuses(id);


--
-- PostgreSQL database dump complete
--


