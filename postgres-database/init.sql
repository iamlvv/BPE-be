-- Table: public.bpe_user

-- DROP TABLE IF EXISTS public.bpe_user;

CREATE TABLE IF NOT EXISTS public.bpe_user
(
    id       serial,
    password character varying(100) COLLATE pg_catalog."default",
    email    character varying(25) COLLATE pg_catalog."default" NOT NULL,
    name     character varying(25) COLLATE pg_catalog."default" NOT NULL,
    phone    character(10) COLLATE pg_catalog."default",
    avatar   character varying(50) COLLATE pg_catalog."default",
    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT users_email_key UNIQUE (email),
    CONSTRAINT users_phone_key UNIQUE (phone)
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
    name      character varying(25) COLLATE pg_catalog."default" NOT NULL,
    is_delete boolean,
    create_at timestamp without time zone,
    user_id   integer                                            NOT NULL,
    CONSTRAINT project_pkey PRIMARY KEY (id),
    CONSTRAINT project_name_key UNIQUE (name)
)
    TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.project
    OWNER to postgres;

-- Table: public.bpmn_file

-- DROP TABLE IF EXISTS public.bpmn_file;

CREATE TABLE IF NOT EXISTS public.bpmn_file
(
    xml_file_link character varying(255) COLLATE pg_catalog."default" NOT NULL UNIQUE,
    project_id    integer                                             NOT NULL,
    version       varchar(10),
    last_saved    timestamp without time zone,
    CONSTRAINT bpmn_file_pkey PRIMARY KEY (xml_file_link, project_id),
    CONSTRAINT bpmn_file_version_key UNIQUE (version)
)
    TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.bpmn_file
    OWNER to postgres;

-- Table: public.cost

-- DROP TABLE IF EXISTS public.cost;


CREATE TABLE IF NOT EXISTS public.evaluated_result
(
    xml_file_link character varying(255) COLLATE pg_catalog."default" NOT NULL,
    project_id    integer                                             NOT NULL,
    result        jsonb,
    CONSTRAINT evaluated_result_pkey PRIMARY KEY (xml_file_link, project_id),
    CONSTRAINT evaluated_result_xml_file_link_key UNIQUE (xml_file_link)
)
    TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.evaluated_result
    OWNER to postgres;

-- Table: public.history_image

-- DROP TABLE IF EXISTS public.history_image;

CREATE TABLE IF NOT EXISTS public.history_image
(
    xml_file_link character varying(255) COLLATE pg_catalog."default" NOT NULL,
    project_id    integer                                             NOT NULL,
    save_at       timestamp without time zone                         NOT NULL,
    image_link    character varying(255) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT history_image_pkey PRIMARY KEY (xml_file_link, project_id, save_at, image_link),
    CONSTRAINT history_image_project_id_key UNIQUE (project_id),
    CONSTRAINT history_image_xml_file_link_key UNIQUE (xml_file_link)
)
    TABLESPACE pg_default;

-- Add constraint

ALTER TABLE IF EXISTS public.history_image
    OWNER to postgres;

ALTER TABLE IF EXISTS public.project
    ADD CONSTRAINT project_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.bpe_user (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION;

ALTER TABLE IF EXISTS public.bpmn_file
    ADD CONSTRAINT bpmn_file_project_id_fkey FOREIGN KEY (project_id)
        REFERENCES public.project (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION;

ALTER TABLE IF EXISTS public.evaluated_result
    ADD CONSTRAINT evaluated_result_project_id_fkey FOREIGN KEY (project_id)
        REFERENCES public.project (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION;

ALTER TABLE IF EXISTS public.evaluated_result
    ADD CONSTRAINT evaluated_result_xml_file_link_fkey FOREIGN KEY (xml_file_link)
        REFERENCES public.bpmn_file (xml_file_link) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.history_image
    ADD CONSTRAINT history_image_project_id_fkey FOREIGN KEY (project_id)
        REFERENCES public.project (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION;

ALTER TABLE IF EXISTS public.history_image
    ADD CONSTRAINT history_image_xml_file_link_fkey FOREIGN KEY (xml_file_link)
        REFERENCES public.bpmn_file (xml_file_link) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION;
