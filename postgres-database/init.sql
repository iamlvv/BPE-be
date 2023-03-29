-- Table: public.bpe_user

-- DROP TABLE IF EXISTS public.bpe_user;

CREATE TABLE IF NOT EXISTS public.bpe_user
(
    id integer NOT NULL DEFAULT 'nextval('users_id_seq'::regclass)',
    password character varying(8) COLLATE pg_catalog."default",
    email character varying(25) COLLATE pg_catalog."default" NOT NULL,
    name character varying(25) COLLATE pg_catalog."default" NOT NULL,
    phone character(10) COLLATE pg_catalog."default",
    avatar character varying(50) COLLATE pg_catalog."default",
    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT users_email_key UNIQUE (email),
    CONSTRAINT users_name_key UNIQUE (name),
    CONSTRAINT users_phone_key UNIQUE (phone)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.bpe_user
    OWNER to postgres;

CREATE TABLE IF NOT EXISTS public.project
(
    id integer NOT NULL DEFAULT 'nextval('project_project_id_seq'::regclass)',
    document character varying COLLATE pg_catalog."default",
    name character varying(25) COLLATE pg_catalog."default" NOT NULL,
    is_delete boolean,
    create_at timestamp without time zone,
    user_id integer NOT NULL DEFAULT 'nextval('project_user_id_seq'::regclass)',
    CONSTRAINT project_pkey PRIMARY KEY (id),
    CONSTRAINT project_name_key UNIQUE (name),
    CONSTRAINT project_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.bpe_user (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.project
    OWNER to postgres;

-- Table: public.bpmn_file

-- DROP TABLE IF EXISTS public.bpmn_file;

CREATE TABLE IF NOT EXISTS public.bpmn_file
(
    xml_file_link character varying(255) COLLATE pg_catalog."default" NOT NULL DEFAULT 'nextval('bpmn_file_xml_file_link_seq'::regclass)',
    project_id integer NOT NULL DEFAULT 'nextval('bpmn_file_project_id_seq'::regclass)',
    version integer NOT NULL,
    last_saved timestamp without time zone,
    CONSTRAINT bpmn_file_pkey PRIMARY KEY (xml_file_link, project_id),
    CONSTRAINT bpmn_file_project_id_key UNIQUE (project_id),
    CONSTRAINT bpmn_file_version_key UNIQUE (version),
    CONSTRAINT bpmn_file_xml_file_link_key UNIQUE (xml_file_link),
    CONSTRAINT bpmn_file_project_id_fkey FOREIGN KEY (project_id)
        REFERENCES public.project (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.bpmn_file
    OWNER to postgres;

-- Table: public.cost

-- DROP TABLE IF EXISTS public.cost;

CREATE TABLE IF NOT EXISTS public.cost
(
    project_id integer NOT NULL DEFAULT 'nextval('cost_project_id_seq'::regclass)',
    xml_file_link character varying(255) COLLATE pg_catalog."default" NOT NULL,
    lane_name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    unit_cost double precision NOT NULL,
    CONSTRAINT cost_project_id_fkey FOREIGN KEY (project_id)
        REFERENCES public.project (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT cost_xml_file_link_fkey FOREIGN KEY (xml_file_link)
        REFERENCES public.bpmn_file (xml_file_link) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.cost
    OWNER to postgres;

-- Table: public.evaluated_result

-- DROP TABLE IF EXISTS public.evaluated_result;

CREATE TABLE IF NOT EXISTS public.evaluated_result
(
    xml_file_link character varying(255) COLLATE pg_catalog."default" NOT NULL DEFAULT 'nextval('evaluated_result_xml_file_link_seq'::regclass)',
    project_id integer NOT NULL DEFAULT 'nextval('evaluated_result_project_id_seq'::regclass)',
    total_task integer NOT NULL,
    optional_task integer NOT NULL,
    flexibility double precision NOT NULL,
    number_of_handled_task integer NOT NULL,
    exception_handling double precision NOT NULL,
    quality double precision NOT NULL,
    cycle_time double precision NOT NULL,
    number_of_unhandled_task integer NOT NULL,
    total_cost double precision,
    CONSTRAINT evaluated_result_pkey PRIMARY KEY (xml_file_link, project_id),
    CONSTRAINT evaluated_result_project_id_fkey FOREIGN KEY (project_id)
        REFERENCES public.project (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT evaluated_result_xml_file_link_fkey FOREIGN KEY (xml_file_link)
        REFERENCES public.bpmn_file (xml_file_link) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.evaluated_result
    OWNER to postgres;

-- Table: public.history_image

-- DROP TABLE IF EXISTS public.history_image;

CREATE TABLE IF NOT EXISTS public.history_image
(
    xml_file_link character varying(255) COLLATE pg_catalog."default" NOT NULL DEFAULT 'nextval('history_image_xml_file_link_seq'::regclass)',
    project_id integer NOT NULL DEFAULT 'nextval('history_image_project_id_seq'::regclass)',
    save_at timestamp without time zone NOT NULL,
    image_link character varying(255) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT history_image_pkey PRIMARY KEY (xml_file_link, project_id, save_at, image_link),
    CONSTRAINT history_image_project_id_key UNIQUE (project_id),
    CONSTRAINT history_image_xml_file_link_key UNIQUE (xml_file_link),
    CONSTRAINT history_image_project_id_fkey FOREIGN KEY (project_id)
        REFERENCES public.project (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT history_image_xml_file_link_fkey FOREIGN KEY (xml_file_link)
        REFERENCES public.bpmn_file (xml_file_link) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.history_image
    OWNER to postgres;

-- Table: public.project

-- DROP TABLE IF EXISTS public.project;


-- Table: public.transparency

-- DROP TABLE IF EXISTS public.transparency;

CREATE TABLE IF NOT EXISTS public.transparency
(
    project_id integer NOT NULL DEFAULT 'nextval('transparency_project_id_seq'::regclass)',
    xml_file_link character varying(255) COLLATE pg_catalog."default" NOT NULL,
    view_name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    transparency double precision NOT NULL,
    number_of_explicit_task integer NOT NULL,
    CONSTRAINT transparency_project_id_fkey FOREIGN KEY (project_id)
        REFERENCES public.project (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT transparency_xml_file_link_fkey FOREIGN KEY (xml_file_link)
        REFERENCES public.bpmn_file (xml_file_link) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.transparency
    OWNER to postgres;