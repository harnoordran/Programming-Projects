-- ***********************
-- Name: Harnoor Kaur Dran
-- Date: 11-10-2023
-- ***********************
SET AUTOCOMMIT ON;

--Q1 Solution
CREATE TABLE L6_MOVIES
(
mid int PRIMARY KEY,
title varchar(35) NOT NULL,
releaseYear int NOT NULL,
director int NOT NULL,
score DECIMAL(3,2) CHECK (score > 0 AND score <5)
);
CREATE TABLE L6_ACTORS
(
aid int PRIMARY KEY,
firstName varchar(20) NOT NULL,
lastName varchar(30) NOT NULL
);
CREATE TABLE L6_CASTINGS
(
movieid int,
actorid int,
PRIMARY KEY (movieid,actorid),
FOREIGN KEY (movieid) REFERENCES L6_MOVIES(mid),
FOREIGN KEY (actorid) REFERENCES L6_ACTORS(aid)
);
CREATE TABLE L6_DIRECTORS
(
directorid INT PRIMARY KEY,
firstname varchar(20) NOT NULL,
lastname varchar(30) NOT NULL
);

--Q2 Solution
ALTER TABLE L6_MOVIES
ADD FOREIGN KEY(director) REFERENCES L6_DIRECTORS(directorid);

--Q3 Solution
ALTER TABLE L6_MOVIES
ADD CONSTRAINT unique_title UNIQUE(title);

--Q4 Solution
INSERT INTO L6_directors(DIRECTORID,FIRSTNAME,LASTNAME) VALUES(1010,'Rob','Minkoff');
INSERT INTO L6_directors(DIRECTORID,FIRSTNAME,LASTNAME) VALUES(1020,'Bill','Condon');
INSERT INTO L6_directors(DIRECTORID,FIRSTNAME,LASTNAME) VALUES(1050,'Josh','Cooley');
INSERT INTO L6_directors(DIRECTORID,FIRSTNAME,LASTNAME) VALUES(2010,'Brad','Bird');
INSERT INTO L6_directors(DIRECTORID,FIRSTNAME,LASTNAME) VALUES(3020,'Lake','Bell');

INSERT INTO L6_movies(mid,title,releaseyear,director,score) VALUES(100,'The Lion King',2019,3020,3.50);
INSERT INTO L6_movies(mid,title,releaseyear,director,score) VALUES(200,'Beauty and the Beast',2017,1050,4.20);
INSERT INTO L6_movies(mid,title,releaseyear,director,score) VALUES(300,'Toy Story 4',2019,1020,4.50);
--Cannot add these values as the constraint says that score must be less than 5
INSERT INTO L6_movies(mid,title,releaseyear,director,score) VALUES(400,'Mission Impossible',2018,2010,5.00);
INSERT INTO L6_movies(mid,title,releaseyear,director,score) VALUES(500,'The Secret Life of Pets',2016,1010,3.90);

--Q5 Solution
DROP TABLE L6_CASTINGS;
DROP TABLE L6_MOVIES;
DROP TABLE L6_ACTORS;
DROP TABLE L6_DIRECTORS;
--Yes , the order might be important in dropping the tables that consist of
--foreign key references as the table that is dependent needs to be deleted 
--before the table being references to avoid errors.


--Q6 Solution
CREATE TABLE employee2 AS SELECT * FROM employees;

--Q7 Solution
ALTER TABLE employee2 ADD username VARCHAR(30);

--Q8 Solution
DELETE FROM employee2;


--Q9 Solution
INSERT INTO employee2 SELECT * FROM employees;

--Q10 Solution
UPDATE employee2 
SET firstname = 'Harnoor',lastname = 'Dran'
WHERE employeenumber = 1002;

--Q11 Solution
UPDATE employee2
SET username = LOWER(SUBSTR(firstname,1,1) || lastname);

--Q12 Solution
DELETE FROM employee2
WHERE officecode = 4;

--Q13 Solution
DROP TABLE employee2;