DROP DATABASE IF EXISTS task_listing;
CREATE DATABASE task_listing;
USE task_listing;

CREATE TABLE category(
    category_id INT(10),
    name VARCHAR(50) NOT NULL,
    description VARCHAR(100),
    CONSTRAINT category_category_id_pk PRIMARY KEY (category_id)
);

CREATE TABLE task(
    task_id INT(10),
    category_id INT(10),
    title VARCHAR(50) NOT NULL,
    content VARCHAR(100),
    deadline DATE,
    is_done BOOLEAN DEFAULT FALSE,
    CONSTRAINT task_task_id_pk PRIMARY KEY (task_id),
    CONSTRAINT task_category_id_fk FOREIGN KEY(category_id) REFERENCES category(category_id)
);

INSERT INTO category VALUES
    (0, "CMSC 127", "File Processing and Database Systems"),
    (1, "CMSC 131", "Introduction to Computer Organization and Machine Level Programming"),
    (2, "Misc", "Free Time");

INSERT INTO task(task_id, category_id, title, content, deadline) VALUES(0, 0, "Milestone 3 SQL Queries", "Create an SQL file containing all your table definitions", "2022-05-16");
INSERT INTO task(task_id, category_id, title, deadline) VALUES
    (1, 0, "Exercise 9 TCL/DCL", "2022-05-23"),
    (2, 0, "Exercise 10 Postgres", "2022-05-30"),
    (3, 1, "Exercise 10 I/O System Services", "2022-05-25"),
    (4, 1, "Study Week 11 Types of CPU", "2022-06-01"),
    (5, NULL, "Study Break", "2023-01-01"),
    (6, 2, "Play the piano", NULL);