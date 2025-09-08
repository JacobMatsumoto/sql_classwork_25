/*-- This SQL script includes intentional syntax errors -- find and correct them,
then run the result
-- 1.find all Zelda games playable on some version of the Game Boy system
SELECT FROM Zelda WHERE Systems LIKE 'Game Boy'
-- 2.update all records having the Timeline "Child Timeline" to read "Child
timeline"
UPDATE Zelda SET Timeline = 'Child timeline";
-- 3.add a new record
INSRT INTO Zelda Timeline, Title, ReleaseYear, Systems
VALUES 'Imaginary timeline', 'The Future of Zelda', 2034, 'Super Duper New Nintendo
Switcheroo';
-- 4.remove the record with GameID 3
REMOVE FROM Zelda WHERE GameID = 3;
-- 5. Display the corrected results (this statement has correct syntax)
SELECT * FROM Zelda;
*/


SELECT * FROM Zelda WHERE Systems LIKE 'Game Boy%'; -- added the * between SELECT and FROM, also added % to make it find partial matches. 

UPDATE Zelda SET Timeline = 'Child timeline' WHERE Timeline = 'Child Timeline'; -- made it target only the typoed 'Child Timeline' where it had been targeting every Timeline

INSERT INTO Zelda (Timeline, Title, ReleaseYear, Systems) --fixed INSRT and added ()
VALUES ('Imaginary timeline', 'The Future of Zelda', 2034, 'Super Duper New Nintendo
Switcheroo');

DELETE FROM Zelda WHERE GameID = 3; --delete, not remove

SELECT * FROM Zelda --no changes