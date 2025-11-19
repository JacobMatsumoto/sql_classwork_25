-- This SQL script includes intentional syntax errors
-- find and correct them, then run the result (debugged)
-- To test this, you will need to connect to a database
DROP TABLE IF EXISTS Courses;

DROP TABLE IF EXISTS Students;

DROP TABLE IF EXISTS Enrollments;

-- Create Students table
CREATE TABLE
    IF NOT EXISTS Students (
        StudentID INTEGER PRIMARY KEY,
        FirstName TEXT,
        LastName TEXT,
        DateOfBirth DATE,
        Email TEXT
    );

-- Insert data into Students table
INSERT INTO
    Students (
        StudentID,
        FirstName,
        LastName,
        DateOfBirth,
        Email
    )
VALUES
    (
        1,
        'John',
        'Doe',
        '1995-05-15',
        'john.doe@email.com'
    ),
    (
        2,
        'Jane',
        'Smith',
        '1998-08-21',
        'jane.smith@email.com'
    ),
    (
        3,
        'Mark',
        'Johnson',
        '1997-03-10',
        'mark.johnson@email.com'
    ),
    (
        4,
        'Mary',
        'Contrary',
        '1996-01-31',
        'contrarian@email.com'
    );

--Create Courses table
CREATE TABLE
    IF NOT EXISTS Courses (
        CourseID INTEGER PRIMARY KEY,
        CourseName TEXT,
        Instructor TEXT
    );

-- Insert data into Courses table
INSERT INTO
    Courses (CourseID, CourseName, Instructor)
VALUES
    (
        101,
        'Introduction to Computer Science',
        'Prof. Anderson'
    ),
    (102, 'Mathematics for Beginners', 'Prof. Davis'),
    (103, 'History of Art', 'Prof. Taylor'),
    (
        104,
        'Programming for Dummies',
        'Randolf Smartalec'
    );

-- Create Enrollments table
CREATE TABLE
    IF NOT EXISTS Enrollments (
        EnrollmentID INTEGER PRIMARY KEY,
        StudentID INTEGER,
        CourseID INTEGER,
        EnrollmentDate DATE,
        FOREIGN KEY (StudentID) REFERENCES Students (StudentID),
        FOREIGN KEY (CourseID) REFERENCES Courses (CourseID)
    );

-- Insert data into Enrollments table
INSERT INTO
    Enrollments (EnrollmentID, StudentID, CourseID, EnrollmentDate)
VALUES
    (1, 1, 101, '2023-01-10'),
    (2, 1, 102, '2023-01-15'),
    (3, 2, 103, '2023-02-01'),
    (4, 3, 101, '2023-02-10'),
    (5, 3, 102, '2023-02-15');

-- Examine the data for student enrollment by course
SELECT
    c.CourseID,
    c.CourseName,
    c.Instructor,
    e.EnrollmentDate,
    s.FirstName,
    s.LastName,
    s.DateOfBirth,
    s.Email
FROM
    Students AS s
    JOIN Enrollments AS e ON s.StudentID = e.StudentID
    JOIN Courses AS c ON e.CourseID = c.CourseID
ORDER BY
    c.CourseID,
    s.LastName,
    s.FirstName;

-- Get an enrollment count by course
SELECT
    c.CourseID,
    c.CourseName,
    c.Instructor,
    Count(e.EnrollmentID) AS Enrollment
FROM
    Courses AS c
    JOIN Enrollments AS e ON e.CourseID = c.CourseID
GROUP BY
    c.CourseID
ORDER BY
    c.CourseID;

-- See Courses with no enrollment
SELECT
    c.CourseName,
    c.Instructor
FROM
    Courses AS c
    LEFT JOIN Enrollments AS e ON e.CourseID = c.CourseID
WHERE
    e.EnrollmentID is NULL;

-- See Students with no courses
SELECT
    s.FirstName,
    s.LastName,
    s.DateOfBirth,
    s.Email
FROM
    Students AS s
    LEFT JOIN Enrollments AS e ON s.StudentID = e.StudentID
WHERE
    e.EnrollmentID is NULL;