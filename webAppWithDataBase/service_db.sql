PGDMP     2    2                {         
   service_db    15.2    15.2     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    24576 
   service_db    DATABASE     ~   CREATE DATABASE service_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE service_db;
                postgres    false                        2615    24577    service    SCHEMA        CREATE SCHEMA service;
    DROP SCHEMA service;
                postgres    false            �            1259    24579    users    TABLE     �   CREATE TABLE service.users (
    id integer NOT NULL,
    full_name character varying NOT NULL,
    login character varying NOT NULL,
    password character varying NOT NULL
);
    DROP TABLE service.users;
       service         heap    postgres    false    6            �            1259    24578    users_id_seq    SEQUENCE     �   CREATE SEQUENCE service.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE service.users_id_seq;
       service          postgres    false    216    6            �           0    0    users_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE service.users_id_seq OWNED BY service.users.id;
          service          postgres    false    215            f           2604    24582    users id    DEFAULT     f   ALTER TABLE ONLY service.users ALTER COLUMN id SET DEFAULT nextval('service.users_id_seq'::regclass);
 8   ALTER TABLE service.users ALTER COLUMN id DROP DEFAULT;
       service          postgres    false    216    215    216            �          0    24579    users 
   TABLE DATA           @   COPY service.users (id, full_name, login, password) FROM stdin;
    service          postgres    false    216   )
       �           0    0    users_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('service.users_id_seq', 26, true);
          service          postgres    false    215            �   �   x���Aj�0����)z���$��]�4���Z�KNP���2��A�Q]����A��/�'���2�Ǐ��5�x�7�����!���0��ÓP����$�0�&騬a�Q��С�G���\�1�v5[4yW���G�w.�J��M�A��mz�*j�[kf6͋ܲ�-��R*.��Rj���Zj>���h������Q�v8P:�����7��C�     