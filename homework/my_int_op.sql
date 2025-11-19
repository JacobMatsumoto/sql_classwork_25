/*
For this project I made some tables with data to mess around with the new tools provided by the lesson. I used cast to make an INT a REAL / float. I used TYPEOF to get the type of a string, int and real, as well as using the number operands +-%*"/" (the slash needed to be in "" or it broke the docstring).  
*/


--First create the relevant tables
CREATE TABLE
    strings (firstName TEXT NOT NULL, email TEXT NOT NULL);

CREATE TABLE
    integers (
        smallNumber INTEGER NOT NULL,
        bigNumber INTEGER NOT NULL
    );

CREATE TABLE
    floats (
        smallFloat FLOAT NOT NULL,
        bigFloat FLOAT NOT NULL
    );

CREATE TABLE
    mixedData (words TEXT, smallNumber INTEGER, bigFloat2 REAL);

INSERT INTO
    strings (firstName, email)
VALUES
    ('John', 'John@john.com');

INSERT INTO
    strings (firstName, email)
VALUES
    ('Kim', 'Kim@john.com');

INSERT INTO
    integers (smallNumber, bigNumber)
VALUES
    (5, 53);

INSERT INTO
    integers (smallNumber, bigNumber)
VALUES
    (7, 73);

INSERT INTO
    integers (smallNumber, bigNumber)
VALUES
    (12, 35);

INSERT INTO
    floats (smallFloat, bigFloat)
VALUES
    (5.0, 50.0);

INSERT INTO
    floats (smallFloat, bigFloat)
VALUES
    (7.0, 70.3);

INSERT INTO
    floats (smallFloat, bigFloat)
VALUES
    (1.0, 35.3);

INSERT INTO
    mixedData (words, smallNumber, bigFloat2)
VALUES
    ("String!", 9, 20.5);

--next I'll use typeof
SELECT
    TYPEOF (words) AS wordsIs,
    TYPEOF (smallNumber) AS smallNumberIs,
    TYPEOF (bigFloat2) AS bigFloatIs
FROM
    mixedData;

--Should give the type of the 3 main datas we learned about
--
--Next I'll use cast to make ints into reals and reals into ints for opporations 
SELECT
    CAST(smallFloat AS INTEGER)
FROM
    floats;

SELECT
    CAST(i.smallNumber AS FLOAT) AS newFloat,
    b.bigFloat as newBigFloat
FROM
    integers AS i
    JOIN floats AS b ON CAST(i.smallNumber AS FLOAT) = b.smallFloat;

--
--Next using +-*/% and round
SELECT
    smallNumber, bigNumber,
    smallNumber + bigNumber AS numberSum, 
    bigNumber - smallNumber AS bigMinusSmall,
    bigNumber * smallNumber AS multiplied
FROM
    integers;

SELECT
    bigNumber, smallNumber,
    bigNumber / smallNumber AS divided,
    bigNumber % smallNumber AS remainder
FROM
    integers;

SELECT ROUND(bigfloat / smallFloat, 10) FROM floats;


--Drop if needed
DROP TABLE IF EXISTS strings;

DROP TABLE IF EXISTS integers;

DROP TABLE IF EXISTS floats;

DROP TABLE IF EXISTS mixedData;