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




In this sql program I'll be making a sql table for people going to a bar and signing up, and then using ALTER SELECT CASE and SELECT DISTINCT
*/

CREATE TABLE barPatrons (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE,
    name TEXT NOT NULL,
    age INTEGER CHECK(age >= 21),
    favoriteDrink TEXT DEFAULT 'Water'
);