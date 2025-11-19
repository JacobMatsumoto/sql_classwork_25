/* 
Creation of the tables for Astro project
 */
CREATE TABLE
    videos (
        videoID INTEGER PRIMARY KEY,
        filePath TEXT NOT NULL,
        fileName TEXT NOT NULL,
        videoDuration TEXT NOT NULL,
        timeStamp TEXT NOT NULL,
        whichCamera TEXT, --(note: front or rear)
        resolution TEXT,
        gpsLat REAL NOT NULL,
        gpsLong REAL NOT NULL,
        location TEXT
    );

CREATE TABLE
    astroStatus (
        astroStatusID INTEGER PRIMARY KEY,
        batteryLife INT NOT NULL,
        locationInSchool TEXT NOT NULL,
        gpsStatus TEXT NOT NULL,
        gpsLat REAL NOT NULL,
        gpsLong REAL NOT NULL,
        camFrontStatus TEXT,
        camRearStatus TEXT,
        currentTask TEXT,
        timeStamp TEXT NOT NULL,
        errorLog TEXT
    );

CREATE TABLE
    sensorReadings (
        readingID INTEGER PRIMARY KEY,
        gasReading TEXT NOT NULL,
        tempHumiReading TEXT NOT NULL,
        usReading TEXT NOT NULL, --(ultrasonic) 
        severity INTEGER NOT NULL, --(0 -10) 
        timeStamp TEXT NOT NULL,
        gpsLat REAL NOT NULL,
        gpsLong REAL NOT NULL
    );

CREATE TABLE
    events (
        eventID INTEGER PRIMARY KEY,
        videoID INTEGER NOT NULL,
        astroStatusID INTEGER NOT NULL,
        readingID INTEGER NOT NULL,
        eventType TEXT NOT NULL,
        confidence REAL NOT NULL, --(1 -100) 
        urgency INTEGER NOT NULL, --(0 -10) 
        timeStamp TEXT NOT NULL,
        detectedBy TEXT NOT NULL,
        whereOccured TEXT NOT NULL,
        gpsLat REAL NOT NULL,
        gpsLong REAL NOT NULL,
        eventReport TEXT NOT NULL,
        FOREIGN KEY (videoID) REFERENCES videos (videoID),
        FOREIGN KEY (astroStatusID) REFERENCES astroStatus (astroStatusID),
        FOREIGN KEY (readingID) REFERENCES sensorReadings (readingID)
    );

--BELOW FOR DROPS
DROP TABLE IF EXISTS videos;

DROP TABLE IF EXISTS astroStatus;

DROP TABLE IF EXISTS sensorReadings;

DROP TABLE IF EXISTS events;

--BELOW FOR QUERIES
SELECT * FROM videos;
SELECT * FROM astroStatus;
SELECT * FROM sensorReadings;
SELECT * FROM events;