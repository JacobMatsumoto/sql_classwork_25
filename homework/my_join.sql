/*I'm importing my bar patrons and lets say this bar is like Garfields 
or Beer Bazaar where there is a bar and store and maybe
they want to keep seperate but similar records of patrons 
So I will create the barPatrons table using a foreign key (email) from a storePatrons table.
My
*/
                                                                                                                                                                              


--FIRST
CREATE TABLE storePatrons (
    id INTEGER PRIMARY KEY, -- id primary keys
    email TEXT UNIQUE, -- forces unique emails
    name TEXT NOT NULL, -- names can not be null
    age INTEGER, --no age check
    favoriteSnack TEXT DEFAULT 'Lays' --default for someones snack choice
);

CREATE TABLE barPatrons (
    id INTEGER PRIMARY KEY, --makes id primary keys
    email TEXT UNIQUE, --ensures people can only use an email once
    name TEXT NOT NULL, --doesn't accept NULL as the name must be filled out with anything
    age INTEGER CHECK(age >= 21), --makes sure they are over 21 
    FOREIGN KEY (email) REFERENCES storePatrons(email) --a bar patron's email must exist in store patrons
    -- https://www.w3schools.com/sql/sql_foreignkey.asp
);

ALTER TABLE barPatrons ADD favoriteDrink TEXT DEFAULT 'Water'; --adds favoriteDrink as a collum

--NEXT
INSERT INTO storePatrons (email, name, age, favoriteSnack) VALUES ('test@gmail','John Smith', 23, 'Doritos');
INSERT INTO storePatrons (email, name, age, favoriteSnack) VALUES ('test2@gmail','Coleene Smith', 45, 'M&Ms');
INSERT INTO storePatrons (email, name, age, favoriteSnack) VALUES ('test3@gmail','Jimbo', 67, 'Sun Chips');
INSERT INTO storePatrons (name, age, favoriteSnack) VALUES ('Bill', 44, 'Snickers'); -- no email should fill NULL (can only do this once? is NULL considered as unique? Would a second NULL break?) Will be in LEFT JOIN but not normal join 
--Works
INSERT INTO storePatrons (email, name, age) VALUES ('test6@gmail','Jimmy Smith', 14); -- repeat name and no chosen snack


--Below these must have emails unique to this table AND exist in storePatrons
INSERT INTO barPatrons (email, name, age, favoriteDrink) VALUES ('test@gmail','John Smith', 23, 'Whiskey');
INSERT INTO barPatrons (email, name, age, favoriteDrink) VALUES ('test2@gmail','Coleene Smith', 45, 'Wine');
INSERT INTO barPatrons (email, name, age, favoriteDrink) VALUES ('test3@gmail','Jimbo', 67, 'Bourbon');


SELECT * FROM barPatrons;
SELECT * FROM storePatrons;

--NEXT
INSERT INTO barPatrons (name, age, favoriteDrink) VALUES ('Billy', 66, 'Bourbon'); -- no email

INSERT INTO barPatrons (email, name, age) VALUES ('test70@gmail','John Smith', 24); -- repeat name and no chosen drink Notice! changed to an invalid email. should fail since it can't find test70 in storePatrons

INSERT INTO storePatrons (name, age, favoriteSnack) VALUES ('Cal', 44, 'Cookies'); -- no email should fill NULL (can only do this once? is NULL considered as unique? Would a second NULL break?)
--Works


SELECT s.email AS email, s.name AS patronName, s.favoriteSnack, b.favoriteDrink
FROM storePatrons AS s 
JOIN barPatrons AS b ON s.email = b.email;
--Lets me pull up emails and name along with their favorite snack and drink

SELECT s.email AS email, s.name AS patronName, s.favoriteSnack, b.favoriteDrink
FROM storePatrons AS s 
LEFT JOIN barPatrons AS b ON s.email = b.email;
--This left join lets us see the patrons that might also be only a store patron.3

DROP TABLE IF EXISTS barPatrons;
DROP TABLE IF EXISTS storePatrons;