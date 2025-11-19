/*I'm importing store patrons table I'm going to add an "inventory" and "sales" table. I then made a trigger so when a sale is made it correctly updates the stock of the respective inventory item. I will also use a trigger to activate only when the amount purchased exceeds the current stock in the inventory table. I feel these triggers would be neccessary in a database setup like I have here as the outofstock trigger prevents an item going into the negatives of stock and the inventoryupdate trigger is convienient and cuts out updating the stock manually. I used the below resources when I looked up "how to make a conditional trigger in SQLite" 

https://www.geeksforgeeks.org/sqlite/sqlite-triggers/ I used this to figure how to make a conditional trigger

Looked for more information on WHEN
https://www.sqlitetutorial.net/sqlite-trigger/
"If you use a condition in the WHEN clause, the trigger is only invoked when the condition is true. In case you omit the WHEN clause, the trigger is executed for all rows."

From my understanding WHEN just wants a true or false.
 */
DROP TABLE IF EXISTS sales;

DROP TABLE IF EXISTS inventory;

DROP TABLE IF EXISTS storePatrons;

DROP TRIGGER IF EXISTS outOfStock;

DROP TRIGGER IF EXISTS inventoryUpdate;

--FIRST
CREATE TABLE --Table of store patrons
    storePatrons (
        customerid INTEGER PRIMARY KEY, -- id primary keys
        email TEXT UNIQUE, -- forces unique emails
        name TEXT NOT NULL, -- names can not be null
        age INTEGER, --no age check
        favoriteSnack TEXT DEFAULT 'Lays' --default for someones snack choice
    );

CREATE TABLE --Table of store patrons
    inventory (
        itemid INTEGER PRIMARY KEY,
        itemName TEXT NOT NULL,
        stock INTEGER NOT NULL
    );

CREATE TABLE --Table of store patrons
    sales (
        saleid INTEGER PRIMARY KEY,
        quantitySold INTEGER NOT NULL,
        saleTime TEXT,
        itemid INTEGER NOT NULL,
        customersEmail TEXT NOT NULL,
        FOREIGN KEY (itemid) REFERENCES inventory (itemid), -- in order to update the item's current stock
        FOREIGN KEY (customersEmail) REFERENCES storePatrons (email) --track customer's purchase
    );

INSERT INTO
    inventory (itemname, stock)
VALUES
    ('Doritos', 30),
    ('M&Ms', 50),
    ('Lays', 35),
    ('Sun Chips', 20);

INSERT INTO
    storePatrons (email, name, age, favoriteSnack)
VALUES
    ('test@gmail', 'John Smith', 23, 'Doritos'),
    ('test2@gmail', 'Coleene Smith', 45, 'M&Ms'),
    ('test3@gmail', 'Jimbo', 67, 'Sun Chips');

INSERT INTO
    storePatrons (email, name, age)
VALUES
    ('test6@gmail', 'Jimmy Smith', 14);

SELECT
    *
FROM
    storePatrons;

SELECT
    *
FROM
    inventory;

--Next
--I made a trigger here that will update the stock of the item sold in a transaction
CREATE TRIGGER inventoryUpdate AFTER INSERT ON sales BEGIN
UPDATE inventory
SET
    stock = stock - NEW.quantitySold
WHERE
    itemid = NEW.itemid;

END;

/*
This trigger uses a WHEN to make sure the new stock being entered isn't less than 0. Preventing selling more than we have. If the NEW stock goes under 0 it will rollback the changes to both tables.
 */
CREATE TRIGGER outOfStock BEFORE
UPDATE ON inventory WHEN NEW.stock < 0 BEGIN
SELECT
    RAISE (ROLLBACK, 'INVENTORY INSUFFICIENT');

END;

--John bought 5 dorritos coleene bought 2 m&ms
BEGIN TRANSACTION;

INSERT INTO
    sales (quantitySold, saleTime, itemid, customersEmail)
VALUES
    (5, DATETIME ('now', 'localtime'), 1, 'test@gmail'),
    (
        2,
        DATETIME ('now', 'localtime'),
        2,
        'test2@gmail'
    );

END TRANSACTION;

--John smith tries to buy 500 dorritos
BEGIN TRANSACTION;

INSERT INTO
    sales (quantitySold, saleTime, itemid, customersEmail)
VALUES
    (
        500,
        DATETIME ('now', 'localtime'),
        1,
        'test@gmail'
    );

END TRANSACTION;

--Extra transaction to insert and show the different times from datetime
BEGIN TRANSACTION;

INSERT INTO
    sales (quantitySold, saleTime, itemid, customersEmail)
VALUES
    (
        10,
        DATETIME ('now', 'localtime'),
        4,
        'test3@gmail'
    );

END TRANSACTION;

SELECT
    *
FROM
    sales;

SELECT
    *
FROM
    inventory;