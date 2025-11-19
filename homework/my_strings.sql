/*I'm importing my bar patrons and store patrons again since a lot of grunt work is done and I can just make small modifications to accomplish the goals of the new task. In this one I added a first name and last name collum into store patrons and bar patrons. In this program I'm copy pasting my previous going database of storePatrons table and barPatrons tables and this time I'm going to utilize LENGTH to check how long strings are, SUBSTR to check specific parts of strings, TRIM to remove parts of strings i don't need and/or leading/ trailing empty space. LTRIM and RTRIM to trim the left and right side of data respectively. LOWER and UPPER to change cases for strings, use LIKE to pull data that fits certain criteria, || to concatanate. And will try to find a way to implement FORMAT

I used this https://www.alphacodingskills.com/sqlite/notes/sqlite-func-format.php for how to use format this is also noted where i used it

In real world examples you would want the trims to atempt to fix bad data that your user might input to your database(s). || to concatanate strings reduce how many collums you have like i do for first name last name in this. substr to break apart data into specific peices. Formatting is good for formatting data in a nicer more readable way and also can make decimal point numbers be cut off at a desired point. UPPER and LOWER are good for comparing strings to make sure they are in the same case for = opperations, Like is good for pulling specific data to fit criteria you set. Trims let you take off leading or trailing whitespace or undesired characters. 
 */
--FIRST
CREATE TABLE
    storePatrons (
        id INTEGER PRIMARY KEY, -- id primary keys
        email TEXT UNIQUE NOT NULL, -- forces unique emails Added not null
        firstName TEXT NOT NULL, -- names can not be null split first and last name
        lastName TEXT NOT NULL, -- names can not be null
        birthday TEXT NOT NULL, --birthday has to be text and not null
        --I want to make it able to automatically make age from birthday but I don't have the skills and knowledge to do so yet.
        age INTEGER, --no age check
        favoriteSnack TEXT DEFAULT 'Lays' --default for someones snack choice
    );

--NEXT
INSERT INTO
    storePatrons (
        email,
        firstName,
        lastName,
        birthday,
        age,
        favoriteSnack
    )
VALUES
    (
        'test@gmail',
        'John',
        'Smith',
        '2002-03-15',
        23,
        'Doritos'
    );

INSERT INTO
    storePatrons (
        email,
        firstName,
        lastName,
        birthday,
        age,
        favoriteSnack
    )
VALUES
    (
        'test2@gmail',
        'Coleene',
        'smith ',
        '1980-11-02',
        45,
        'M&Ms'
    );

INSERT INTO
    storePatrons (
        email,
        firstName,
        lastName,
        birthday,
        age,
        favoriteSnack
    )
VALUES
    (
        'test3@gmail',
        'Jimbo',
        'Slims',
        '1958-06-30',
        67,
        'Sun Chips'
    );

INSERT INTO
    storePatrons (
        email,
        firstName,
        lastName,
        birthday,
        age,
        favoriteSnack
    )
VALUES
    (
        'test4@gmail',
        'Bill',
        'Conroy',
        '1981-01-09',
        44,
        'Snickers'
    );

INSERT INTO
    storePatrons (email, firstName, lastName, birthday, age)
VALUES
    (
        'test5@gmail',
        'Jimmy',
        'Smithy',
        '2011-08-05',
        14
    );

-- no chosen snack
INSERT INTO
    storePatrons (
        email,
        firstName,
        lastName,
        birthday,
        age,
        favoriteSnack
    )
VALUES
    (
        'test6@gmail',
        '.Johnathan.',
        'Smithsons',
        '1982-04-12',
        43,
        'Twix'
    );

INSERT INTO
    storePatrons (
        email,
        firstName,
        lastName,
        birthday,
        age,
        favoriteSnack
    )
VALUES
    (
        'test6@gmail',
        '         Johnson',
        'Conroy',
        '1985-01-21',
        40,
        'doritos'
    );

INSERT INTO
    storePatrons (
        email,
        firstName,
        lastName,
        birthday,
        age,
        favoriteSnack
    )
VALUES
    (
        'test6@gmail',
        'Johnny      ',
        'Cash',
        '1979-01-09',
        46,
        '100 Grand Bar'
    );

--NEXT (Using LIKE and the various TRIMs)
SELECT
    firstName
FROM
    storePatrons
WHERE
    LTRIM (firstName) LIKE 'John%';

--This selects all names starting with John removing leadingempty space as it does so to catch misinputs
SELECT
    lastName
FROM
    storePatrons
WHERE
    RTRIM (lastName) LIKE '%s';

--This selects all last names ending in s RTRIMing any empty spaces for you
SELECT
    TRIM(firstName, '.')
FROM
    storePatrons;

--NEXT (Using LENGTH)
SELECT
    LENGTH (birthday) AS charactersInBirthday
FROM
    storePatrons;

--NEXT (Using || to concatenate data and SUBSTR to break up strings and reuses trim)
SELECT
    TRIM(TRIM(firstName, '.')) || ' ' || lastName AS fullName,
    birthday, --Here I'm taking storePatrons' first & last name fields and concatinating them to make "fullName" as a field
    --I'm using trim to fix the .s and then clear empty spaces
    --I'm also using substr to break the year, month and day off of the full birthday string.
    SUBSTR (birthday, 1, 4) AS year, --selects only the first 4 characters from the yyyy-mm-dd birthday format
    SUBSTR (birthday, 6, 2) AS month, --selects characters 6&7 from birthday and makes it a collum called month
    SUBSTR (birthday, 9, 2) AS day --selects characters 9&10 from birthday and makes it a collum called month
FROM
    storePatrons
ORDER BY
    birthday;

--Pull from storePatrons ordered by birthdays
--NEXT (Using of LOWER and UPPER)
SELECT
    firstName || ' ' || lastName AS fullName,
    favoriteSnack
FROM
    storePatrons
WHERE
    UPPER(favoriteSnack) = 'DORITOS';

SELECT
    firstName || ' ' || lastName AS fullName,
    favoriteSnack
FROM
    storePatrons
WHERE
    lastName = 'smith';

SELECT
    firstName || ' ' || lastName AS fullName,
    favoriteSnack
FROM
    storePatrons
WHERE
    lower(lastName) = 'smith';

--NEXT (Using FORMAT) I used this https://www.alphacodingskills.com/sqlite/notes/sqlite-func-format.php for how to use format
SELECT
    FORMAT ('%s %s: %s', firstName, lastName, email) AS contactInfo -- %s acts as string placeholders
FROM
    storePatrons;

SELECT
    *
FROM
    storePatrons;

DROP TABLE IF EXISTS storePatrons;