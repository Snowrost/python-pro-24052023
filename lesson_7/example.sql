CREATE TABLE groups(
	id UUID NOT NULL PRIMARY KEY,
	name varchar(30) NOT NULL,
	start_date timestamp
);

CREATE TABLE students(
	id UUID NOT NULL PRIMARY KEY,
	first_name varchar(50) NOT NULL,
	last_name varchar(150) NOT NULL,
	address varchar(200),
	group_id UUID references groups(id)
);

INSERT INTO groups VALUES('40db2a8e-f513-4458-8661-623911f48aa9',
'Python Pro 25.05.2023',
'2023-05-25');

SELECT * FROM groups;

INSERT INTO students VALUES('e4069274-d2f2-430a-b31f-5ffe40d5ebe3',
'Ivan',
'Niekipielov',
'somewhere',
'40db2a8e-f513-4458-8661-623911f48aa9');

INSERT INTO students VALUES('81bc93ab-fe00-4c84-b242-fac5a41c9172',
'John',
'Dou',
'somewhere else',
'40db2a8e-f513-4458-8661-623911f48aa9');

INSERT INTO students VALUES('c71502ae-cbb8-4309-831c-6a1323ad1bf9',
'Iosef',
'G',
'somewhere far far away',
'40db2a8e-f513-4458-8661-623911f48aa9');

SELECT * FROM students;

SELECT * FROM students WHERE first_name in ('John', 'Ivan')
AND address = 'somewhere';

SELECT * FROM students WHERE first_name = 'John'
OR first_name= 'Ivan';

SELECT first_name, * FROM students;

UPDATE students SET address='London' WHERE id='e4069274-d2f2-430a-b31f-5ffe40d5ebe3';

DELETE FROM students WHERE first_name='Iosef';

explain analyse SELECT * FROM students WHERE first_name='Ivan';

CREATE INDEX students_first_name_idx ON students(first_name);


