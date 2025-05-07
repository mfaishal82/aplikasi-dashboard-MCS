-- Supabase database dump
-- Schema only (no data)
-- Generated on 2025-05-07T04:57:16.701Z

-- Disable foreign key constraints during import (uncomment to use)
-- SET session_replication_role = 'replica';

-- Start transaction
BEGIN;

-- Table: siswa
DROP TABLE IF EXISTS siswa CASCADE;

CREATE TABLE siswa (
  id bigint NOT NULL,
  nama text NOT NULL,
  kelas_id bigint NOT NULL,
  halaqoh_id bigint NOT NULL,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  gender text NOT NULL
);

ALTER TABLE siswa ADD PRIMARY KEY (id);

-- Table: halaqoh
DROP TABLE IF EXISTS halaqoh CASCADE;

CREATE TABLE halaqoh (
  id bigint NOT NULL,
  nama text NOT NULL,
  gender text NOT NULL,
  pengajar_id bigint NOT NULL,
  mulai_tahun_ajaran smallint NOT NULL,
  akhir_tahun_ajaran smallint NOT NULL
);

ALTER TABLE halaqoh ADD PRIMARY KEY (id);

-- Table: pengajar_pelajaran
DROP TABLE IF EXISTS pengajar_pelajaran CASCADE;

CREATE TABLE pengajar_pelajaran (
  pengajar_pelajaran_id bigint NOT NULL,
  pengajar_id bigint NOT NULL,
  pelajaran_id bigint NOT NULL,
  kelas_id bigint NOT NULL,
  pengajar_nama text,
  pelajaran_nama text,
  kelas_nama text,
  mulai_tahun_ajaran smallint,
  akhir_tahun_ajaran smallint
);

ALTER TABLE pengajar_pelajaran ADD PRIMARY KEY (pengajar_pelajaran_id);

-- Table: kelas
DROP TABLE IF EXISTS kelas CASCADE;

CREATE TABLE kelas (
  id bigint NOT NULL,
  nama text NOT NULL,
  gender text NOT NULL,
  walikelas_id bigint NOT NULL,
  mulai_tahun_ajaran smallint NOT NULL,
  akhir_tahun_ajaran smallint NOT NULL
);

ALTER TABLE kelas ADD PRIMARY KEY (id);

-- Table: pelajaran
DROP TABLE IF EXISTS pelajaran CASCADE;

CREATE TABLE pelajaran (
  id bigint NOT NULL,
  nama text NOT NULL
);

ALTER TABLE pelajaran ADD PRIMARY KEY (id);

-- Table: pengajar
DROP TABLE IF EXISTS pengajar CASCADE;

CREATE TABLE pengajar (
  id bigint NOT NULL,
  nama text NOT NULL,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  gender text NOT NULL DEFAULT ''::text,
  birthday date
);

ALTER TABLE pengajar ADD PRIMARY KEY (id);

-- Table: quranidn
DROP TABLE IF EXISTS quranidn CASCADE;

CREATE TABLE quranidn (
  id integer NOT NULL,
  surah_id integer NOT NULL,
  verse_id integer NOT NULL,
  verse_text text NOT NULL,
  indo_text text NOT NULL,
  read_text text,
  page integer,
  surah_name varchar(100),
  is_sajadah boolean NOT NULL DEFAULT false,
  juz_id integer
);

ALTER TABLE quranidn ADD PRIMARY KEY (id);

-- Table: setoran
DROP TABLE IF EXISTS setoran CASCADE;

CREATE TABLE setoran (
  id integer NOT NULL,
  siswa_id integer NOT NULL,
  pengajar_id integer NOT NULL,
  jenis varchar(10) NOT NULL,
  halaman_awal integer NOT NULL,
  halaman_akhir integer NOT NULL,
  waktu_setoran timestamp with time zone NOT NULL DEFAULT now(),
  surah_mulai integer,
  verse_mulai integer,
  surah_akhir integer,
  verse_akhir integer
);

ALTER TABLE setoran ADD PRIMARY KEY (id);

-- Sequences for table: setoran
-- Create sequence if it doesn't exist
CREATE SEQUENCE IF NOT EXISTS public.setoran_id_seq
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 2147483647
  START 1
  NO CYCLE;

-- Set sequence value
SELECT pg_catalog.setval('public.setoran_id_seq', 103108, true);

-- Set sequence ownership
ALTER SEQUENCE public.setoran_id_seq OWNED BY setoran.id;

-- Foreign key constraints (added at the end to avoid dependency issues)
-- Foreign key constraints for table: siswa
ALTER TABLE siswa ADD CONSTRAINT siswa_kelas_id_fkey FOREIGN KEY (kelas_id) REFERENCES kelas (id);
ALTER TABLE siswa ADD CONSTRAINT siswa_halaqoh_id_fkey FOREIGN KEY (halaqoh_id) REFERENCES halaqoh (id);

-- Foreign key constraints for table: halaqoh
ALTER TABLE halaqoh ADD CONSTRAINT fk_pembimbing FOREIGN KEY (pengajar_id) REFERENCES pengajar (id);

-- Foreign key constraints for table: pengajar_pelajaran
ALTER TABLE pengajar_pelajaran ADD CONSTRAINT pengajar_pelajaran_pelajaran_id_fkey FOREIGN KEY (pelajaran_id) REFERENCES pelajaran (id);
ALTER TABLE pengajar_pelajaran ADD CONSTRAINT pengajar_pelajaran_pengajar_id_fkey FOREIGN KEY (pengajar_id) REFERENCES pengajar (id);
ALTER TABLE pengajar_pelajaran ADD CONSTRAINT pengajar_pelajaran_kelas_id_fkey FOREIGN KEY (kelas_id) REFERENCES kelas (id);

-- Foreign key constraints for table: kelas
ALTER TABLE kelas ADD CONSTRAINT fk_walikelas FOREIGN KEY (walikelas_id) REFERENCES pengajar (id);

-- Commit transaction
COMMIT;

-- Re-enable foreign key constraints (uncomment if you disabled them above)
-- SET session_replication_role = 'origin';

