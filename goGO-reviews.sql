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
    bathroom_name character varying,
    date_time date NOT NULL,
    cleanliness integer NOT NULL,
    accessible boolean,
    lgbt_friendly boolean,
    comments text,
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

COPY public.review_info (review_id, bathroom_name, date_time, cleanliness, accessible, lgbt_friendly, comments, bathroom_id, user_id) FROM stdin;
3	Saba's Restaurant	2021-11-04	5	t	t	Restrooms were very clean and people were friendly.	ChIJa7-vBdjpQIYRzzJYuvA2Zyg	3
4	Chevron	2021-02-03	1	t	f	very dirty	ChIJQeEdnxbCQIYR1t19RlpVIyU	3
5	McDonald's	2021-11-11	4	t	t	Super clean!	ChIJqefELgrCQIYRUdAmyEoYW-I	3
8	Swift Food Mart	2021-11-01	1	t	f	You do not want to go here...trust me. 	ChIJvUAVAHDCQIYRVsU9xggoL_8	1
9	Exxon	2021-11-12	3	t	t	Fairly clean for a little gas station.	ChIJ71CMwRHCQIYRJSK2NiFr2Ro	1
10	McDonald's	2021-11-14	5	t	f	CLEAN!!	ChIJqefELgrCQIYRUdAmyEoYW-I	1
12	Chevron	2021-11-02	1	f	f	A lot of people hanging around outside. Wish I could rate this a negative 100. Felt unsafe and restroom was extremely dirty. 	ChIJQeEdnxbCQIYR1t19RlpVIyU	1
13	Chick-fil-A	2021-11-04	5	t	f	Clean. Too bad they aren't LGBT friendly.	${restroomMarker.bathroom_id}	1
14	Hartz Chicken Buffet	2021-11-16	3	t	t	Restrooms were not gender neutral, but they were single use and staff was very lgbt friendly.	ChIJZf4U4mXCQIYRV5A24GaB9Fo	1
15	Manbo food	2021-11-16	1	t	t	Gender neutral restrooms...yayyyyy!	ChIJlZZ8P2XCQIYRVqQxp6Q6-30	1
18	Taqueria La Sabrosita	2021-11-18	4	t	f	Restrooms only for one person at a time. Their hand soap smelled amazing too. 	ChIJKxPibXfCQIYREAKlEJunlOk	1
19	Amigo's Gas	2021-11-07	2	f	f		ChIJp5BTY2_CQIYRQaS9mmk1uFg	1
20	Circle K	2021-11-22	1	t	t	Gender neutral restrooms, but filthy.	ChIJVeryLmzCQIYRgXmUnWnvV-A	1
21	Phillips 66	2021-11-22	4	t	f	Crazy clean!	ChIJa2nL8RHCQIYR08r1deQV9Ds	1
22	Phillips 66	2021-11-22	4	t	f	Crazy clean!	ChIJa2nL8RHCQIYR08r1deQV9Ds	1
23	Swift Food Mart	2021-11-04	1	f	f	Never again.	${restroomMarker.bathroom_id}	1
24	Manbo food	2021-10-04	5	t	t	Very clean, very friendly, and Trans friendly restrooms.	ChIJlZZ8P2XCQIYRVqQxp6Q6-30	1
25	Manbo food	2021-10-04	5	t	t	Very clean, very friendly, and Trans friendly restrooms.	ChIJlZZ8P2XCQIYRVqQxp6Q6-30	1
26	Chick-fil-A	2021-11-23	5	f	f	It's a shame that Chik-fil-a does not support the LGBT community.	${restroomMarker.bathroom_id}	3
28	El Pupusodromo	2021-11-09	4	t	f	Overall pretty great.	${restroomMarker.bathroom_id}	1
29	Astral Catering	2021-11-23	1	f	f	Not a public restroom.	ChIJGxIh0WzCQIYRM80c79ZzHrs	1
30	Chick-fil-A	2021-11-16	5	t	f	Definiely not LGBTQ friendly...	ChIJKTph52DCQIYRBXJ3QbyiBsc	1
32	Tacos	2021-11-23	5	t	t	LGBTQ friendly, handicap accessible, very clean, and TACOS!!	ChIJtxXDNT_DQIYR-tTSgze6ZIY	4
33	El Pupusodromo	2021-11-24	5	f	t	bathroom smells like pinesol, so I KNOW it's clean!	ChIJT5Y80m3CQIYRtFqnNy99ZTA	7
34	Neft Inc	2021-11-22	5	f	f	Very clean restroom, but terrible vibes.	ChIJQ6munxbCQIYRM8vBOwpj-yA	1
\.


--
-- Data for Name: user_info; Type: TABLE DATA; Schema: public; Owner: courtneydoss
--

COPY public.user_info (user_id, fname, lname, email, password) FROM stdin;
1	Courtney	Doss	777.catalyst@gmail.com	cosmo
2	Bobby	Hassan	test@gmail.com	bobby
3	Steve	advisor	steve@gmail.com	test
4	Bullseye	Target	targetmascot@target.com	target
5	Austin	Doss	middlebro@brothers.com	austin
6	Christian 	Bridgeforth	littlebro@brothers.com	chris
7	Asher	Alexander	aaa140777@gmail.com	poop101
\.


--
-- Name: review_info_review_id_seq; Type: SEQUENCE SET; Schema: public; Owner: courtneydoss
--

SELECT pg_catalog.setval('public.review_info_review_id_seq', 34, true);


--
-- Name: user_info_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: courtneydoss
--

SELECT pg_catalog.setval('public.user_info_user_id_seq', 7, true);


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

