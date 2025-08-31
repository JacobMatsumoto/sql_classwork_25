/* Directions:
Write a brief paragraph describing the exercise you will design to practice using the basic SQL commands.
You may include this in your .sql file by using SQL Comments: use -- for a single line comment or /*  */ to enclose a multi-line comment.

Create SQL code to implement your idea and test it in SQLite Studio.
Your code should use each of the following SQL statements at least once: SELECT, INSERT, UPDATE, DELETE.
You may use one or more of the example databases provided (e.g. from LinkedIn Exercise files or class demos.)

Create a brief video of your working SQL exercise.
Note: You may use screen-capture video software of your choice: Panopto, Zoom, etc. 

This is a practice file for learning the basics of sql, I have selects to query the data in the tables inserts to add data to the table deletes to remove data and updates to update data. I used the test sql given in the sample sql zip.
 */

SELECT 'Hello world!' AS "First Statement"; -- This makes a query and populates Hello world! with the collum name as First Statement

SELECT * FROM customer; --This shows all customers 

SELECT * FROM customer ORDER BY name; -- This shows all customers ordered by name

INSERT INTO customer (name, address, city, state, zip) VALUES ('James Cole', '223 Street Street', 'Haha City', 'IL', '22499'); --This query adds a new row into customer with the data present in "values". 
SELECT * FROM customer; --This shows all customers 

INSERT INTO customer (address, state, zip) VALUES ('121 New Street', 'NY', 29993); --This query adds a new row into customer but is missing name and city.
SELECT * FROM customer; --This shows all customers 

UPDATE customer SET name = 'Josh Block', city = 'New York' WHERE id = 5; --this updates the record with the id of 5 to now have a name and city where they would normally be NULL.
SELECT * FROM customer; --This shows all customers 

UPDATE customer SET name = 'Bill Smith' WHERE id = 1; --I used this to see if I could change a non NULL data using this.
SELECT * FROM customer; --This shows all customers 

DELETE FROM customer WHERE ID = 4; -- This deletes the row with the associated ID of 6
SELECT * FROM customer; --This shows all customers 