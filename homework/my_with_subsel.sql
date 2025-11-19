/*I'm importing my bar patrons and store patrons from the join week. I made an extra table called "drinks" and it stores the drinks name and how many times it has been ordered. I then use these tables to make a view of the bar patrons and their favorite drinks and how many times the drink has been ordered. After that I use a few subselects and use them to grab averages of the patrons ages and checking to see who is older than the average. I then use the same query structure for the drinks table. Finally I wanted to try re-writing the drinks average sub select query in CTE. I did struggle figuring out CTE for a while and I hope I did what the assignment wanted with it right. 
 */
--FIRST
CREATE TABLE --Table of store patrons
    storePatrons (
        id INTEGER PRIMARY KEY, -- id primary keys
        email TEXT UNIQUE, -- forces unique emails
        name TEXT NOT NULL, -- names can not be null
        age INTEGER, --no age check
        favoriteSnack TEXT DEFAULT 'Lays' --default for someones snack choice
    );

CREATE TABLE --Table of bar patrons
    barPatrons (
        id INTEGER PRIMARY KEY, --makes id primary keys
        email TEXT UNIQUE, --ensures people can only use an email once
        name TEXT NOT NULL, --doesn't accept NULL as the name must be filled out with anything
        age INTEGER CHECK (age >= 21), --makes sure they are over 21
        favoriteDrink TEXT DEFAULT 'Water', --a bar patron's email must exist in store patrons 
        FOREIGN KEY (email) REFERENCES storePatrons (email)
        -- https://www.w3schools.com/sql/sql_foreignkey.asp
    );

CREATE TABLE --New table for drinks
    drinks (
        id INTEGER PRIMARY KEY,
        drinkName TEXT,
        timesOrdered INTEGER
    );

--NEXT
INSERT INTO
    drinks (drinkName, timesOrdered)
VALUES
    ('Whiskey', 8),
    ('Martini', 4),
    ('Shots', 13),
    ('Wine', 7),
    ('Bourbon', 10);

INSERT INTO
    storePatrons (email, name, age, favoriteSnack)
VALUES
    ('test@gmail', 'John Smith', 23, 'Doritos');

INSERT INTO
    storePatrons (email, name, age, favoriteSnack)
VALUES
    ('test2@gmail', 'Coleene Smith', 45, 'M&Ms');

INSERT INTO
    storePatrons (email, name, age, favoriteSnack)
VALUES
    ('test3@gmail', 'Jimbo', 67, 'Sun Chips');

INSERT INTO
    storePatrons (name, age, favoriteSnack)
VALUES
    ('Bill', 44, 'Snickers');

INSERT INTO
    storePatrons (email, name, age)
VALUES
    ('test6@gmail', 'Jimmy Smith', 14);

-- repeat name and no chosen snack
--Below these must have emails unique to this table AND exist in storePatrons
INSERT INTO
    barPatrons (email, name, age, favoriteDrink)
VALUES
    ('test@gmail', 'John Smith', 23, 'Whiskey');

INSERT INTO
    barPatrons (email, name, age, favoriteDrink)
VALUES
    ('test2@gmail', 'Coleene Smith', 45, 'Wine');

INSERT INTO
    barPatrons (email, name, age, favoriteDrink)
VALUES
    ('test3@gmail', 'Jimbo', 67, 'Bourbon');

SELECT
    *
FROM
    barPatrons;

SELECT
    *
FROM
    storePatrons;

SELECT
    *
FROM
    drinks;

--I create a new VIEW called drinkAndFans making it a query showing peoples favorite drinks, their name, and how many times the drink has been ordered. 
--Next
CREATE VIEW
    drinkAndFans AS
SELECT
    b.name AS patronName,
    b.favoriteDrink,
    d.timesOrdered
FROM
    barPatrons AS b
    JOIN drinks AS d ON b.favoriteDrink = d.drinkName;

SELECT
    *
FROM
    drinkAndFans;

--https://www.w3schools.com/sql/sql_avg.asp
--Selecting the name and age of patrons that are above the average age as well as selecting the average age.
--NEXT
SELECT
    name,
    age,
    (
        SELECT
            AVG(age)
        FROM
            storePatrons
    ) AS averageAge
FROM
    storePatrons
WHERE
    age > (
        SELECT
            AVG(age)
        FROM
            storePatrons
    );

-- This is the same as above but for drinks
--NEXT
SELECT
    drinkName,
    timesOrdered,
    (
        SELECT
            AVG(timesOrdered)
        FROM
            drinks
    ) AS averageOrdered
FROM
    drinks
WHERE
    timesOrdered > (
        SELECT
            AVG(timesOrdered)
        FROM
            drinks
    );

--rewriting the above query in CTE.
-- This was really confusing for me to understand for a while. I think I understand how with works a little better now. I 'save' a SELECT query as averageOrderedDrinks from drinks to use it for the following query and save a little writing in the long run if I had to use it multiple times. and then I select the drinks table and the average and join them with an arbitary always true statement so they join every line, then i use a where to only show drinks above the average.
--NEXT 
WITH
    averageOrderedDrinks AS (
        SELECT
            AVG(timesOrdered) AS averageOrderedDrinks
        FROM
            drinks
    )
SELECT
    d.drinkName,
    d.timesOrdered,
    a.averageOrderedDrinks
FROM
    drinks AS d
    JOIN averageOrderedDrinks AS a ON d.timesOrdered >= 0
WHERE
    d.timesOrdered > a.averageOrderedDrinks;

DROP TABLE IF EXISTS barPatrons;

DROP TABLE IF EXISTS drinks;

DROP TABLE IF EXISTS storePatrons;

DROP VIEW IF EXISTS drinkAndFans