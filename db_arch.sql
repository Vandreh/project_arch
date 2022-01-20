CREATE DATABASE db_arch;

DROP TABLE IF EXISTS notas;
DROP TABLE IF EXISTS users;

CREATE TABLE users(
   id_user SERIAL PRIMARY KEY,
   nome_user varchar(80) NOT NULL UNIQUE,
   "password" varchar NOT NULL, 
   "status" varchar(30) NOT NULL
);

CREATE TABLE notas(
   id_nota SERIAL PRIMARY KEY,
   aluno_id BIGINT NOT NULL,
   n1 INT,
   n2 INT,
   n3 INT,
   n4 INT,
   CONSTRAINT fk_aluno
      FOREIGN KEY(aluno_id) 
	   REFERENCES users(id_user)
);
