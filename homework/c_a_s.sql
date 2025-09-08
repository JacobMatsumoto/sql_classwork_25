/* Write a brief paragraph describing a table you will design and what data it will contain.
Explain your reasoning behind any constraints you included in your table design.
You may include this as comments in your SQL code.
Create SQL code to create your table and test it in SQLite Studio.
Your design should use each of the following SQL constraints at least once: PRIMARY KEY, UNIQUE, NOT NULL, DEFAULT, and CHECK.
Create an INDEX for one or more of the fields in your table.
Demonstrate use of the ALTER statement to modify the design of one or more tables.
Demonstrate use of SELECT CASE.
Demonstrate use of SELECT DISTINCT.
Create a brief video of your working SQL exercise.




In this sql program I'll be making a sql table for people going to a bar and signing up, and then using ALTER to add a new section to the table, SELECT CASE to see if someones a senior and SELECT DISTINCT
*/

CREATE TABLE barPatrons (
    id INTEGER PRIMARY KEY, --makes id primary keys
    email TEXT UNIQUE, --ensures people can only use an email once
    name TEXT NOT NULL, --doesn't accept NULL as the name must be filled out with anything
    age INTEGER CHECK(age >= 21) --makes sure they are over 21 
);

CREATE INDEX email_index ON barPatrons(email); --makes an email index

ALTER TABLE barPatrons ADD favoriteDrink TEXT DEFAULT 'Water'; --adds favoriteDrink as a collum

SELECT name, age, --Queries name and age then uses age to see if they're senior citizens
    CASE WHEN age >= 65 THEN 'Senior' ELSE 'Not Senior' END AS discountStatus; FROM barPatrons

SELECT DISTINCT name FROM barPatrons --Only shows distinct/unique names in the bar patron signups.

INSERT INTO barPatrons (email, name, age, favoriteDrink) VALUES ('test@gmail','John Smith', 23, 'Whiskey');
INSERT INTO barPatrons (email, name, age, favoriteDrink) VALUES ('test2@gmail','Coleene Smith', 45, 'Wine');
INSERT INTO barPatrons (email, name, age, favoriteDrink) VALUES ('test3@gmail','Jimbo', 67, 'Bourbon');
INSERT INTO barPatrons (email, name, age,) VALUES ('test6@gmail','John Smith', 34,); -- repeat name and no chosen drink
SELECT * FROM barPatrons

INSERT INTO barPatrons (email, age, favoriteDrink) VALUES ('test5@gmail', 43, 'Whiskey'); --no name
INSERT INTO barPatrons (email, name, age, favoriteDrink) VALUES ('test4@gmail','Billy Thomson', 19, 'Bud Light'); -- under 21
INSERT INTO barPatrons (email, name, age, favoriteDrink) VALUES ('test@gmail','Bill Smith', 44, 'Screw Driver'); -- repeat email
--populating the table.

DROP TABLE barPatrons;