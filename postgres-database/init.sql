-- Table: public.bpe_user

-- DROP TABLE IF EXISTS public.bpe_user;

CREATE TABLE IF NOT EXISTS public.bpe_user
(
    id        serial,
    password  character varying(200) COLLATE pg_catalog."default",
    email     character varying COLLATE pg_catalog."default" NOT NULL,
    name      character varying(200) COLLATE pg_catalog."default" NOT NULL,
    phone     character(10) COLLATE pg_catalog."default",
    avatar    character varying COLLATE pg_catalog."default",
    verified  boolean,
    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT users_email_key UNIQUE (email)
)
    TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.bpe_user
    OWNER to postgres;

-- Table: public.project

-- DROP TABLE IF EXISTS public.project;

CREATE TABLE IF NOT EXISTS public.project
(
    id        serial,
    document  character varying COLLATE pg_catalog."default",
    name      character varying(200) COLLATE pg_catalog."default" NOT NULL,
    is_delete boolean,
    create_at timestamp without time zone,
    CONSTRAINT project_pkey PRIMARY KEY (id)
)
    TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.project
    OWNER to postgres;

-- Table: public.work_on

-- DROP TABLE IF EXISTS public.work_on;

CREATE TABLE IF NOT EXISTS public.work_on
(
    id         serial,
    user_id    integer NOT NULL,
    project_id integer NOT NULL,
    role       integer NOT NULL,
    CONSTRAINT work_on_pkey PRIMARY KEY (user_id, project_id)
)
    TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.work_on
    OWNER to postgres;

-- Table: public.bpmn_file

-- DROP TABLE IF EXISTS public.bpmn_file;

CREATE TABLE IF NOT EXISTS public.bpmn_file
(
    id            serial,
    xml_file_link character varying COLLATE pg_catalog."default" NOT NULL UNIQUE,
    project_id    integer                                             NOT NULL,
    version       varchar(10),
    last_saved    timestamp without time zone,
    CONSTRAINT bpmn_file_pkey PRIMARY KEY (xml_file_link, project_id),
    CONSTRAINT bpmn_file_version_key UNIQUE (version)
)
    TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.bpmn_file
    OWNER to postgres;

-- Table: public.comment_on

-- DROP TABLE IF EXISTS public.comment_on;

CREATE TABLE IF NOT EXISTS public.comment_on
(
    id            serial,
    user_id       integer NOT NULL,
    project_id    integer NOT NULL,
    xml_file_link character varying COLLATE pg_catalog."default" NOT NULL,
    content       character varying COLLATE pg_catalog."default" NOT NULL,
    create_at     timestamp without time zone,
    CONSTRAINT    comment_on_pkey PRIMARY KEY (id, user_id, project_id, xml_file_link)
)
    TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.comment_on
    OWNER to postgres;

-- Table: public.evaluated_result

-- DROP TABLE IF EXISTS public.evaluated_result;

CREATE TABLE IF NOT EXISTS public.evaluated_result
(
    id                 serial,
    xml_file_link      character varying COLLATE pg_catalog."default" NOT NULL,
    project_id         integer                                             NOT NULL,
    name               character varying(200) COLLATE pg_catalog."default" NOT NULL UNIQUE,
    result             jsonb,
    description        character varying COLLATE pg_catalog."default",
    project_start_time timestamp without time zone NOT NULL,
    base_time_unit     double precision NOT NULL,
    base_currency_unit character varying(10) COLLATE pg_catalog."default" NOT NULL,
    create_at          timestamp without time zone,
    CONSTRAINT evaluated_result_pkey PRIMARY KEY (xml_file_link, project_id, name)
)
    TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.evaluated_result
    OWNER to postgres;

-- Table: public.history_image

-- DROP TABLE IF EXISTS public.history_image;

CREATE TABLE IF NOT EXISTS public.history_image
(
    id            serial,
    xml_file_link character varying COLLATE pg_catalog."default" NOT NULL,
    project_id    integer                                             NOT NULL,
    save_at       timestamp without time zone                         NOT NULL,
    image_link    character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT history_image_pkey PRIMARY KEY (id, xml_file_link, project_id, save_at)
)
    TABLESPACE pg_default;

-- Add constraint

ALTER TABLE IF EXISTS public.history_image
    OWNER to postgres;

ALTER TABLE IF EXISTS public.bpmn_file
    ADD CONSTRAINT bpmn_file_project_id_fkey FOREIGN KEY (project_id)
        REFERENCES public.project (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION;

ALTER TABLE IF EXISTS public.work_on
    ADD CONSTRAINT work_on_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.bpe_user (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION;

ALTER TABLE IF EXISTS public.work_on
    ADD CONSTRAINT work_on_project_id_fkey FOREIGN KEY (project_id)
        REFERENCES public.project (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION;

ALTER TABLE IF EXISTS public.comment_on
    ADD CONSTRAINT comment_on_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.bpe_user (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION;

ALTER TABLE IF EXISTS public.comment_on
    ADD CONSTRAINT comment_on_project_id_fkey FOREIGN KEY (project_id, xml_file_link)
        REFERENCES public.bpmn_file (project_id, xml_file_link) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION;

ALTER TABLE IF EXISTS public.evaluated_result
    ADD CONSTRAINT evaluated_result_project_id_fkey FOREIGN KEY (project_id, xml_file_link)
        REFERENCES public.bpmn_file (project_id, xml_file_link) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION;

ALTER TABLE IF EXISTS public.history_image
    ADD CONSTRAINT history_image_xml_file_link_fkey FOREIGN KEY (project_id, xml_file_link)
        REFERENCES public.bpmn_file (project_id, xml_file_link) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION;
