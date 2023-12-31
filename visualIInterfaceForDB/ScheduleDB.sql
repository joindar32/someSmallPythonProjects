PGDMP     ,                     {            schedule    15.2    15.2                0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    40960    schedule    DATABASE     |   CREATE DATABASE schedule WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE schedule;
                postgres    false            �            1259    40971    subject    TABLE     ^   CREATE TABLE public.subject (
    id integer NOT NULL,
    name character varying NOT NULL
);
    DROP TABLE public.subject;
       public         heap    postgres    false            �            1259    40970    subject_id_seq    SEQUENCE     �   CREATE SEQUENCE public.subject_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE public.subject_id_seq;
       public          postgres    false    215                       0    0    subject_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE public.subject_id_seq OWNED BY public.subject.id;
          public          postgres    false    214            �            1259    40980    teacher    TABLE     �   CREATE TABLE public.teacher (
    teacher_id integer NOT NULL,
    full_name character varying NOT NULL,
    subject integer
);
    DROP TABLE public.teacher;
       public         heap    postgres    false            �            1259    40979    teacher_teacher_id_seq    SEQUENCE     �   CREATE SEQUENCE public.teacher_teacher_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.teacher_teacher_id_seq;
       public          postgres    false    217                       0    0    teacher_teacher_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.teacher_teacher_id_seq OWNED BY public.teacher.teacher_id;
          public          postgres    false    216            �            1259    41008 	   timetable    TABLE     �   CREATE TABLE public.timetable (
    id_lesson integer NOT NULL,
    day character varying NOT NULL,
    week integer NOT NULL,
    subject integer,
    room_numb character varying NOT NULL,
    start_time character varying NOT NULL
);
    DROP TABLE public.timetable;
       public         heap    postgres    false            �            1259    41007    timetable_id_lesson_seq    SEQUENCE     �   CREATE SEQUENCE public.timetable_id_lesson_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.timetable_id_lesson_seq;
       public          postgres    false    219                       0    0    timetable_id_lesson_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.timetable_id_lesson_seq OWNED BY public.timetable.id_lesson;
          public          postgres    false    218            o           2604    40974 
   subject id    DEFAULT     h   ALTER TABLE ONLY public.subject ALTER COLUMN id SET DEFAULT nextval('public.subject_id_seq'::regclass);
 9   ALTER TABLE public.subject ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    215    214    215            p           2604    40983    teacher teacher_id    DEFAULT     x   ALTER TABLE ONLY public.teacher ALTER COLUMN teacher_id SET DEFAULT nextval('public.teacher_teacher_id_seq'::regclass);
 A   ALTER TABLE public.teacher ALTER COLUMN teacher_id DROP DEFAULT;
       public          postgres    false    217    216    217            q           2604    41011    timetable id_lesson    DEFAULT     z   ALTER TABLE ONLY public.timetable ALTER COLUMN id_lesson SET DEFAULT nextval('public.timetable_id_lesson_seq'::regclass);
 B   ALTER TABLE public.timetable ALTER COLUMN id_lesson DROP DEFAULT;
       public          postgres    false    218    219    219            	          0    40971    subject 
   TABLE DATA           +   COPY public.subject (id, name) FROM stdin;
    public          postgres    false    215                    0    40980    teacher 
   TABLE DATA           A   COPY public.teacher (teacher_id, full_name, subject) FROM stdin;
    public          postgres    false    217                    0    41008 	   timetable 
   TABLE DATA           Y   COPY public.timetable (id_lesson, day, week, subject, room_numb, start_time) FROM stdin;
    public          postgres    false    219   �                  0    0    subject_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.subject_id_seq', 9, true);
          public          postgres    false    214                       0    0    teacher_teacher_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.teacher_teacher_id_seq', 9, true);
          public          postgres    false    216                       0    0    timetable_id_lesson_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.timetable_id_lesson_seq', 25, true);
          public          postgres    false    218            s           2606    40978    subject subject_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.subject
    ADD CONSTRAINT subject_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.subject DROP CONSTRAINT subject_pkey;
       public            postgres    false    215            u           2606    40987    teacher teacher_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.teacher
    ADD CONSTRAINT teacher_pkey PRIMARY KEY (teacher_id);
 >   ALTER TABLE ONLY public.teacher DROP CONSTRAINT teacher_pkey;
       public            postgres    false    217            w           2606    41015    timetable timetable_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY public.timetable
    ADD CONSTRAINT timetable_pkey PRIMARY KEY (id_lesson);
 B   ALTER TABLE ONLY public.timetable DROP CONSTRAINT timetable_pkey;
       public            postgres    false    219            x           2606    40988    teacher teacher_subject_fkey    FK CONSTRAINT     }   ALTER TABLE ONLY public.teacher
    ADD CONSTRAINT teacher_subject_fkey FOREIGN KEY (subject) REFERENCES public.subject(id);
 F   ALTER TABLE ONLY public.teacher DROP CONSTRAINT teacher_subject_fkey;
       public          postgres    false    3187    217    215            y           2606    41016     timetable timetable_subject_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.timetable
    ADD CONSTRAINT timetable_subject_fkey FOREIGN KEY (subject) REFERENCES public.subject(id);
 J   ALTER TABLE ONLY public.timetable DROP CONSTRAINT timetable_subject_fkey;
       public          postgres    false    3187    219    215            	   �   x�UP9n�0����ȝ����p�H��*�a7~�,Y��f�!�")x���p�K4��
����6G�7Q�;��i��s���ˈ��C�r������&è걷R��)I�W�\9��	g�>�L�Ư*��L�p 0���8�U��>�Q�&�C�6��0��B��A喙�$���+��y8��|�9ly�ϵ�S6I���*ypX���sD�O�B`G��;�Py��/�z�D         �   x�=�K
�@D�ݧ�4��e<LTč���������Wxs#g��ꦫ�U%���}J���h)Wcg�hO�¥����P8�Ff�Ӿ�S���2co�ׁp�o��΋��d�M:�!�ʗ��C	��yn�-����[���#������0+�X��c���~ �z�           x�u�AN�@Eמ�����$��p��+$$�,+�P��Z��n;HM�(J����#d�v��m���]���/�&�˞��J��p��IPYۏʪ�ڧmlGGĠd����\5������Qs�,�JG�G��OQ"e�U�E�:����' �n�}���y3����}5iy����
Zޓv\�E��W�?\�ն�����w��Uhy���F�m�����v @[��偧Q���kT��F��˨��߂�I�G� q�\��I��:��5$     