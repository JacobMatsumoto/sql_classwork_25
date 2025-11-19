/* 
I'm going to design 2 tables one will be an inventory table holding different products a convenience this table will contain the product's ID, name, price per unit and current stock. The other table will be a sales table. It will have its own ID, a foreign key from product IDs, units sold. I'll use transactions to efficiently and safely write data to my tables and then I'll demonstrate how I could use ROLLBACK to well, rollback changes to a table in a the middle of a transaction. And I'll also demonstrate how I'd utilize SAVEPOINTs to make a state within transactions I can reliably ROLLBACK to. Also, it doesn't seem to of been part of the assignment but a big point of using savepoint, so I included myself using RELEASE in order to save the savepoint after a rollback. I included a link below for the resource I used to learn more about savepoint, rollback and release.
https://www.slingacademy.com/article/practical-examples-of-using-savepoint-in-sqlite/#what-is-a-savepoint? 
 */

DROP TABLE IF EXISTS sales;

DROP TABLE IF EXISTS products;



CREATE TABLE
    products (
        itemID INTEGER PRIMARY KEY,
        itemName TEXT NOT NULL,
        unitPrice REAL NOT NULL,
        stock INTEGER NOT NULL
    );

CREATE TABLE
    sales (
        id INTEGER PRIMARY KEY,
        itemID INTEGER NOT NULL,
        numSold INTEGER NOT NULL,
        FOREIGN KEY (itemID) REFERENCES products (itemID)
    );

BEGIN TRANSACTION;

INSERT INTO
    products (itemName, unitPrice, stock)
VALUES
    ('Layz Chips', 4.99, 30),
    ('Oreo', 6.99, 20),
    ('Jerky', 9.99, 15),
    ('Mints', 1.99, 50),
    ('Magazine', 3.99, 10);

END TRANSACTION;

SELECT
    *
FROM
    products;

SELECT
    *
FROM
    sales;

BEGIN TRANSACTION;

INSERT INTO
    sales (numSold, itemID)
VALUES
    (2, 2), --2 oreo
    (3, 3), -- 3 jerky
    (1, 5);

-- 1 magazine
UPDATE products
SET
    stock = (stock - 2) --updating oreo stock
WHERE
    itemID = 2;

UPDATE products
SET
    stock = (stock - 3) --updating jerky stock
WHERE
    itemID = 3;

UPDATE products
SET
    stock = (stock - 1) --updating magazine stock
WHERE
    itemID = 5;

SAVEPOINT postSale1;

-- creates a savepoint for me to rollback to and subsequently release
INSERT INTO
    sales (numSold, itemID)
VALUES
    (1, 8), -- 1 thing that doesn't exist in our products table, 8 is out of scope.
    (2, 4); -- 2 mints

UPDATE products
SET
    stock = (stock - 1)
WHERE
    itemID = 8;

UPDATE products
SET
    stock = (stock - 2)
WHERE
    itemID = 4;

ROLLBACK TO postSale1;

--rolls back to my savepoint
RELEASE postSale1;

--saves the changes that happen up to the savepoint.
END TRANSACTION;

SELECT
    *
FROM
    products;

SELECT
    *
FROM
    sales;