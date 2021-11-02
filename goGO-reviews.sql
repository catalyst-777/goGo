--
-- PostgreSQL database dump
--

-- Dumped from database version 13.4
-- Dumped by pg_dump version 13.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: review_info; Type: TABLE; Schema: public; Owner: courtneydoss
--

CREATE TABLE public.review_info (
    review_id integer NOT NULL,
    cleanliness integer NOT NULL,
    accessibile boolean,
    lgbt_friendly boolean,
    bathroom_id character varying NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.review_info OWNER TO courtneydoss;

--
-- Name: review_info_review_id_seq; Type: SEQUENCE; Schema: public; Owner: courtneydoss
--

CREATE SEQUENCE public.review_info_review_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.review_info_review_id_seq OWNER TO courtneydoss;

--
-- Name: review_info_review_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: courtneydoss
--

ALTER SEQUENCE public.review_info_review_id_seq OWNED BY public.review_info.review_id;


--
-- Name: user_info; Type: TABLE; Schema: public; Owner: courtneydoss
--

CREATE TABLE public.user_info (
    user_id integer NOT NULL,
    fname character varying(30) NOT NULL,
    lname character varying(30) NOT NULL,
    email character varying(100) NOT NULL,
    password character varying(100) NOT NULL
);


ALTER TABLE public.user_info OWNER TO courtneydoss;

--
-- Name: user_info_user_id_seq; Type: SEQUENCE; Schema: public; Owner: courtneydoss
--

CREATE SEQUENCE public.user_info_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_info_user_id_seq OWNER TO courtneydoss;

--
-- Name: user_info_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: courtneydoss
--

ALTER SEQUENCE public.user_info_user_id_seq OWNED BY public.user_info.user_id;


--
-- Name: review_info review_id; Type: DEFAULT; Schema: public; Owner: courtneydoss
--

ALTER TABLE ONLY public.review_info ALTER COLUMN review_id SET DEFAULT nextval('public.review_info_review_id_seq'::regclass);


--
-- Name: user_info user_id; Type: DEFAULT; Schema: public; Owner: courtneydoss
--

ALTER TABLE ONLY public.user_info ALTER COLUMN user_id SET DEFAULT nextval('public.user_info_user_id_seq'::regclass);


--
-- Data for Name: review_info; Type: TABLE DATA; Schema: public; Owner: courtneydoss
--

COPY public.review_info (review_id, cleanliness, accessibile, lgbt_friendly, bathroom_id, user_id) FROM stdin;
\.


--
-- Data for Name: user_info; Type: TABLE DATA; Schema: public; Owner: courtneydoss
--

COPY public.user_info (user_id, fname, lname, email, password) FROM stdin;
1	Courtney	Doss	777.catalyst@gmail.com	cosmo
2	Bobby	Hassan	test@gmail.com	bobby
\.


--
-- Name: review_info_review_id_seq; Type: SEQUENCE SET; Schema: public; Owner: courtneydoss
--

SELECT pg_catalog.setval('public.review_info_review_id_seq', 1, false);


--
-- Name: user_info_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: courtneydoss
--

SELECT pg_catalog.setval('public.user_info_user_id_seq', 2, true);


--
-- Name: review_info review_info_pkey; Type: CONSTRAINT; Schema: public; Owner: courtneydoss
--

ALTER TABLE ONLY public.review_info
    ADD CONSTRAINT review_info_pkey PRIMARY KEY (review_id);


--
-- Name: user_info user_info_email_key; Type: CONSTRAINT; Schema: public; Owner: courtneydoss
--

ALTER TABLE ONLY public.user_info
    ADD CONSTRAINT user_info_email_key UNIQUE (email);


--
-- Name: user_info user_info_pkey; Type: CONSTRAINT; Schema: public; Owner: courtneydoss
--

ALTER TABLE ONLY public.user_info
    ADD CONSTRAINT user_info_pkey PRIMARY KEY (user_id);


--
-- Name: review_info review_info_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: courtneydoss
--

ALTER TABLE ONLY public.review_info
    ADD CONSTRAINT review_info_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.user_info(user_id);


--
-- PostgreSQL database dump complete
--

