"""
    Astro Database project

    References used or found below
    https://docs.python.org/3/library/sqlite3.html  NOTE Briefly skimmed. Keep reading.

    https://www.pythontutorial.net/tkinter/tkinter-scrollbar/ NOTE Scroll bar functionality

    https://stackoverflow.com/questions/9561030/vertical-and-horizontal-scrollbars-on-tkinter-widget NOTE Scroll bar functionality
    
    https://www.youtube.com/watch?v=0WafQCaok6g&t=483s NOTE Scroll bar functionality
    
    Short python file utilizing placeholder fake data in order to try to do a small commit of data to the database. I create some fake data and then verify that it is either a tuple or a list, and that it isn't empty, then I stick it into the database. This happpens for each individual table. appending to the database is fully scaleable thanks to executemany. However I am hitting a snag with figuring out how to properly scale a GUI for an easier way to display data. I have a start for it in the wip function (work in progress wip). If anyone has suggestions and experience with python's tkinter, I would greatly appreciate suggestions! Thank you!

    TODO Now that you have all the bones of what you want make it into OOP based

"""

import sqlite3 as sql
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
root = tk.Tk()
root.title("Astro Database")
# works for python 3.4 --Screen width+height utilized from stack overflow https://stackoverflow.com/questions/27574854/passing-variables-to-tkinter-geometry-method

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
screen_resolution = str(screen_width)+'x'+str(screen_height)

root.geometry(screen_resolution)

# centers the main content https://www.pythontutorial.net/tkinter/tkinter-grid/
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)

# cursor.execute("CREATE TABLE test(test1 TEXT, test2 TEXT, test3 TEXT)") #test of connectivity
# cursor.execute("DROP TABLE IF EXISTS test") #test of connectivity

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)


def drop_all_tables():
    """Checks to see if the tables exists and drops them"""
    db_conn = None
    try:
        db_conn = sql.connect('astro_db.db')
        cursor = db_conn.cursor()

        cursor.execute("""DROP TABLE IF EXISTS events""")

        cursor.execute("""DROP TABLE IF EXISTS astroStatus""")

        cursor.execute("""DROP TABLE IF EXISTS videos""")

        cursor.execute("""DROP TABLE IF EXISTS sensorReadings""")

        db_conn.commit()  # comment out for tests without pushing data in

        build_videos_gui()

    except ValueError:
        print("Invalid input. Please enter a number.")

    except sql.Error as e:
        print(f"Sqlite error occurred: {e}")
        db_conn.rollback()

    except Exception as e:
        print(f"An error occurred: {e}")
        db_conn.rollback()

    finally:
        if db_conn is not None:
            db_conn.close()


class MessageBoxes:
    def __init__(self, parent=None):
        self.parent = parent

    def ask_yes_no(self):
        question = messagebox.askyesno(
            "Are you sure?", "This will delete the database"
        )
        if question:
            drop_all_tables()
            messagebox.showinfo("Database deleted",
                                "The database has been dropped")
        else:
            messagebox.showinfo("Database not deleted",
                                "The database was not deleted.")


def restore_empty_tables():
    """
    Restores all tables to empty unfilled states.
    """
    db_conn = None
    try:
        db_conn = sql.connect('astro_db.db')
        cursor = db_conn.cursor()

        cursor.execute("""CREATE TABLE astroStatus (
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
            )""")

        cursor.execute("""CREATE TABLE
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
            )""")

        cursor.execute("""CREATE TABLE
        sensorReadings (
        readingID INTEGER PRIMARY KEY,
        gasReading TEXT NOT NULL,
        tempHumiReading TEXT NOT NULL,
        usReading TEXT NOT NULL, --(ultrasonic) 
        severity INTEGER NOT NULL, --(0 -10) 
        timeStamp TEXT NOT NULL,
        gpsLat REAL NOT NULL,
        gpsLong REAL NOT NULL
            )""")

        cursor.execute("""CREATE TABLE
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
            )""")

        print("All tables made. Commmiting...")

        db_conn.commit()  # comment out for tests without pushing data in

        build_videos_gui()

    except sql.Error as e:
        print(f"Sqlite error occurred: {e}")
        db_conn.rollback()

    except Exception as e:
        print(f"An error occurred: {e}")
        db_conn.rollback()

    finally:
        if db_conn is not None:
            db_conn.close()


# temporary fake data, list of tuples. Co-pilot generated
fake_videos_data = [
    (1, '/videos/front_cam/', 'front_001.mp4', '00:01:23',
     '2025-11-16 14:32:00', 'front', '1080p', 42.2598, -88.3683, 'Main Hall'),
    (2, '/videos/rear_cam/', 'rear_002.mp4', '00:02:10',
     '2025-11-16 14:35:00', 'rear', '720p', 42.2598, -88.3683, 'Science Wing'),
    (3, '/videos/side_cam/', 'side_003.mp4', '00:01:45',
     '2025-11-16 14:38:00', 'side', '1080p', 42.2598, -88.3683, 'Library'),
    (4, '/videos/front_cam/', 'front_004.mp4', '00:02:05',
     '2025-11-16 14:41:00', 'front', '720p', 42.2598, -88.3683, 'Gym'),
    (5, '/videos/rear_cam/', 'rear_005.mp4', '00:01:55',
     '2025-11-16 14:44:00', 'rear', '4K', 42.2598, -88.3683, 'Parking Lot'),
    (6, '/videos/side_cam/', 'side_006.mp4', '00:02:20',
     '2025-11-16 14:47:00', 'side', '1080p', 42.2598, -88.3683, 'Main Hall'),
    (7, '/videos/front_cam/', 'front_007.mp4', '00:01:40',
     '2025-11-16 14:50:00', 'front', '720p', 42.2598, -88.3683, 'Science Wing'),
    (8, '/videos/rear_cam/', 'rear_008.mp4', '00:02:15',
     '2025-11-16 14:53:00', 'rear', '1080p', 42.2598, -88.3683, 'Library'),
    (9, '/videos/side_cam/', 'side_009.mp4', '00:01:50',
     '2025-11-16 14:56:00', 'side', '4K', 42.2598, -88.3683, 'Gym'),
    (10, '/videos/front_cam/', 'front_010.mp4', '00:02:00',
     '2025-11-16 14:59:00', 'front', '1080p', 42.2598, -88.3683, 'Parking Lot'),
    (11, '/videos/rear_cam/', 'rear_011.mp4', '00:01:35',
     '2025-11-16 15:02:00', 'rear', '720p', 42.2598, -88.3683, 'Main Hall'),
    (12, '/videos/side_cam/', 'side_012.mp4', '00:02:25',
     '2025-11-16 15:05:00', 'side', '1080p', 42.2598, -88.3683, 'Science Wing'),
    (13, '/videos/front_cam/', 'front_013.mp4', '00:01:30',
     '2025-11-16 15:08:00', 'front', '4K', 42.2598, -88.3683, 'Library'),
    (14, '/videos/rear_cam/', 'rear_014.mp4', '00:02:12',
     '2025-11-16 15:11:00', 'rear', '1080p', 42.2598, -88.3683, 'Gym'),
    (15, '/videos/side_cam/', 'side_015.mp4', '00:01:48',
     '2025-11-16 15:14:00', 'side', '720p', 42.2598, -88.3683, 'Parking Lot'),
    (16, '/videos/front_cam/', 'front_016.mp4', '00:02:08',
     '2025-11-16 15:17:00', 'front', '1080p', 42.2598, -88.3683, 'Main Hall'),
    (17, '/videos/rear_cam/', 'rear_017.mp4', '00:01:42',
     '2025-11-16 15:20:00', 'rear', '4K', 42.2598, -88.3683, 'Science Wing'),
    (18, '/videos/side_cam/', 'side_018.mp4', '00:02:18',
     '2025-11-16 15:23:00', 'side', '1080p', 42.2598, -88.3683, 'Library'),
    (19, '/videos/front_cam/', 'front_019.mp4', '00:01:52',
     '2025-11-16 15:26:00', 'front', '720p', 42.2598, -88.3683, 'Gym'),
    (20, '/videos/rear_cam/', 'rear_020.mp4', '00:02:03',
     '2025-11-16 15:29:00', 'rear', '1080p', 42.2598, -88.3683, 'Parking Lot'),
    (21, '/videos/side_cam/', 'side_021.mp4', '00:01:37',
     '2025-11-16 15:32:00', 'side', '4K', 42.2598, -88.3683, 'Main Hall'),
    (22, '/videos/front_cam/', 'front_022.mp4', '00:02:22',
     '2025-11-16 15:35:00', 'front', '1080p', 42.2598, -88.3683, 'Science Wing'),
    (23, '/videos/rear_cam/', 'rear_023.mp4', '00:01:46',
     '2025-11-16 15:38:00', 'rear', '720p', 42.2598, -88.3683, 'Library'),
    (24, '/videos/side_cam/', 'side_024.mp4', '00:02:10',
     '2025-11-16 15:41:00', 'side', '1080p', 42.2598, -88.3683, 'Gym'),
    (25, '/videos/front_cam/', 'front_025.mp4', '00:01:55',
     '2025-11-16 15:44:00', 'front', '4K', 42.2598, -88.3683, 'Parking Lot'),
    (26, '/videos/rear_cam/', 'rear_026.mp4', '00:02:07',
     '2025-11-16 15:47:00', 'rear', '1080p', 42.2598, -88.3683, 'Main Hall'),
    (27, '/videos/side_cam/', 'side_027.mp4', '00:01:43',
     '2025-11-16 15:50:00', 'side', '720p', 42.2598, -88.3683, 'Science Wing'),
    (28, '/videos/front_cam/', 'front_028.mp4', '00:02:17',
     '2025-11-16 15:53:00', 'front', '1080p', 42.2598, -88.3683, 'Library'),
    (29, '/videos/rear_cam/', 'rear_029.mp4', '00:01:49',
     '2025-11-16 15:56:00', 'rear', '4K', 42.2598, -88.3683, 'Gym'),
    (30, '/videos/side_cam/', 'side_030.mp4', '00:02:11',
     '2025-11-16 15:59:00', 'side', '1080p', 42.2598, -88.3683, 'Parking Lot'),
    (31, '/videos/front_cam/', 'front_031.mp4', '00:01:44',
     '2025-11-16 16:02:00', 'front', '1080p', 42.2598, -88.3683, 'Main Hall'),
    (32, '/videos/rear_cam/', 'rear_032.mp4', '00:02:09',
     '2025-11-16 16:05:00', 'rear', '720p', 42.2598, -88.3683, 'Science Wing'),
    (33, '/videos/side_cam/', 'side_033.mp4', '00:01:53',
     '2025-11-16 16:08:00', 'side', '4K', 42.2598, -88.3683, 'Library'),
    (34, '/videos/front_cam/', 'front_034.mp4', '00:02:06',
     '2025-11-16 16:11:00', 'front', '1080p', 42.2598, -88.3683, 'Gym'),
    (35, '/videos/rear_cam/', 'rear_035.mp4', '00:01:39',
     '2025-11-16 16:14:00', 'rear', '720p', 42.2598, -88.3683, 'Parking Lot'),
    (36, '/videos/side_cam/', 'side_036.mp4', '00:02:14',
     '2025-11-16 16:17:00', 'side', '1080p', 42.2598, -88.3683, 'Main Hall'),
    (37, '/videos/front_cam/', 'front_037.mp4', '00:01:47',
     '2025-11-16 16:20:00', 'front', '4K', 42.2598, -88.3683, 'Science Wing'),
    (38, '/videos/rear_cam/', 'rear_038.mp4', '00:02:02',
     '2025-11-16 16:23:00', 'rear', '1080p', 42.2598, -88.3683, 'Library'),
    (39, '/videos/side_cam/', 'side_039.mp4', '00:01:41',
     '2025-11-16 16:26:00', 'side', '720p', 42.2598, -88.3683, 'Gym'),
    (40, '/videos/front_cam/', 'front_040.mp4', '00:02:19',
     '2025-11-16 16:29:00', 'front', '1080p', 42.2598, -88.3683, 'Parking Lot'),
    (41, '/videos/rear_cam/', 'rear_041.mp4', '00:01:36',
     '2025-11-16 16:32:00', 'rear', '4K', 42.2598, -88.3683, 'Main Hall'),
    (42, '/videos/side_cam/', 'side_042.mp4', '00:02:23',
     '2025-11-16 16:35:00', 'side', '1080p', 42.2598, -88.3683, 'Science Wing'),
    (43, '/videos/front_cam/', 'front_043.mp4', '00:01:51',
     '2025-11-16 16:38:00', 'front', '720p', 42.2598, -88.3683, 'Library'),
    (44, '/videos/rear_cam/', 'rear_044.mp4', '00:02:04',
     '2025-11-16 16:41:00', 'rear', '1080p', 42.2598, -88.3683, 'Gym'),
    (45, '/videos/side_cam/', 'side_045.mp4', '00:01:49',
     '2025-11-16 16:44:00', 'side', '4K', 42.2598, -88.3683, 'Parking Lot'),
    (46, '/videos/front_cam/', 'front_046.mp4', '00:02:16',
     '2025-11-16 16:47:00', 'front', '1080p', 42.2598, -88.3683, 'Main Hall'),
    (47, '/videos/rear_cam/', 'rear_047.mp4', '00:01:38',
     '2025-11-16 16:50:00', 'rear', '720p', 42.2598, -88.3683, 'Science Wing'),
    (48, '/videos/side_cam/', 'side_048.mp4', '00:02:13',
     '2025-11-16 16:53:00', 'side', '1080p', 42.2598, -88.3683, 'Library'),
    (49, '/videos/front_cam/', 'front_049.mp4', '00:01:54',
     '2025-11-16 16:56:00', 'front', '4K', 42.2598, -88.3683, 'Gym'),
    (50, '/videos/rear_cam/', 'rear_050.mp4', '00:02:01',
     '2025-11-16 16:59:00', 'rear', '1080p', 42.2598, -88.3683, 'Parking Lot')
]


fake_astro_status_data = [
    (1, 85, 'Main Hall', 'Active', 42.2598, -88.3683, 'Recording',
     'Idle', 'Monitoring', '2025-11-16 14:32:00', ''),
    (2, 78, 'Science Wing', 'Active', 42.2598, -88.3683, 'Idle',
     'Recording', 'Scanning', '2025-11-16 14:35:00', 'Low light detected')
]

fake_sensor_readings_data = [
    (1, 'Normal', '22C/45%', '1.2m', 2, '2025-11-16 14:32:00', 42.2598, -88.3683),
    (2, 'Elevated CO2', '24C/50%', '0.8m', 6,
     '2025-11-16 14:35:00', 42.2598, -88.3683)
]

# Temporary, if I can figure out how to grab data from these I'd like to generate the last section "Report" in Python
fake_events_data = [
    (1, 1, 1, 1, 'Routine Check', 95.0, 2, '2025-11-16 14:32:00',
     'AstroBot', 'Main Hall', 42.2598, -88.3683, 'Everything is normal'),
    (2, 2, 2, 2, 'Gas Alert', 88.5, 7, '2025-11-16 14:35:00', 'AstroBot',
     'Science Wing', 42.2598, -88.3683, 'Elevated CO2 levels detected.')
]


def commit_videos(video_data):
    """Takes an argument and checks if it is a list or tuple and tries to push it into the videos table"""
    db_conn = None
    try:
        db_conn = sql.connect('astro_db.db')
        cursor = db_conn.cursor()

        if isinstance(video_data, (list, tuple)) and video_data:
            cursor.executemany("""INSERT INTO videos(videoID, filePath, fileName, videoDuration, timeStamp,
            whichCamera, resolution, gpsLat, gpsLong, location) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", video_data)
            print("Inserting data into videos table... Committing...\nCommit done.")
            db_conn.commit()  # comment out for tests without pushing data in

    except sql.Error as e:
        print(f"Sqlite error occurred: {e}")
        db_conn.rollback()

    except Exception as e:
        print(f"An error occurred: {e}")
        db_conn.rollback()


def commit_astro_status(astro_status_data):
    """Takes an argument and checks if it is a list or tuple and tries to push it into the astroStatus table"""
    db_conn = None
    try:
        db_conn = sql.connect('astro_db.db')
        cursor = db_conn.cursor()

        if isinstance(astro_status_data, (list, tuple)) and astro_status_data:
            cursor.executemany("""INSERT INTO astroStatus(astroStatusID, batteryLife, locationInSchool, gpsStatus, gpsLat, gpsLong,
            camFrontStatus, camRearStatus, currentTask, timeStamp, errorLog) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", astro_status_data)
            print("Inserting data into astroStatus table... Committing...\nCommit done.")
            db_conn.commit()  # comment out for tests without pushing data in

    except sql.Error as e:
        print(f"Sqlite error occurred: {e}")
        db_conn.rollback()

    except Exception as e:
        print(f"An error occurred: {e}")
        db_conn.rollback()


def commit_sensor_data(sensor_data):
    """Takes an argument and checks if it is a list or tuple and tries to push it into the sensorReadings table"""
    db_conn = None
    try:
        db_conn = sql.connect('astro_db.db')
        cursor = db_conn.cursor()

        if isinstance(sensor_data, (list, tuple)) and sensor_data:
            cursor.executemany("""INSERT INTO sensorReadings(readingID, gasReading, tempHumiReading, usReading, severity,
            timeStamp, gpsLat, gpsLong) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", sensor_data)
            print(
                "Inserting data into sensorReadings table... Committing...\nCommit done.")
            db_conn.commit()  # comment out for tests without pushing data in

    except sql.Error as e:
        print(f"Sqlite error occurred: {e}")
        db_conn.rollback()

    except Exception as e:
        print(f"An error occurred: {e}")
        db_conn.rollback()


def commit_event_data(event_data):
    """Takes an argument and checks if it is a list or tuple and tries to push it into the event table"""
    db_conn = None
    try:
        db_conn = sql.connect('astro_db.db')
        cursor = db_conn.cursor()

        if isinstance(event_data, (list, tuple)) and event_data:
            cursor.executemany("""INSERT INTO events(eventID, videoID, astroStatusID, readingID, eventType,
            confidence, urgency, timeStamp, detectedBy, whereOccured,
            gpsLat, gpsLong, eventReport) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", event_data)
            print("Inserting data into events table... Committing...\nCommit done.")
            db_conn.commit()  # comment out for tests without pushing data in

    except sql.Error as e:
        print(f"Sqlite error occurred: {e}")
        db_conn.rollback()

    except Exception as e:
        print(f"An error occurred: {e}")
        db_conn.rollback()


def turn_tables_into_list_of_dicts():
    """
    Creates a list of dictionaries for each set of data for each table. Allows for easy assigning variables to specific data for later.

    Would be done/accessed like this:

    video_data, astroStatus_data, sensor_data, event_data = turn_tables_into_list_of_dicts()
    location_video_2 = video_data[1]["location"]

    this will help me (hopefully) make a gui (later) to display data nicer and potentially make a CRUD. Primarily planning this for display and maybe adding a "notes" column to each table for someone to edit and add to it. Would also help to fix data if something gets past future error checking
    """

    try:
        db_conn = sql.connect('astro_db.db')

        cursor = db_conn.cursor()

        cursor.execute("SELECT * FROM videos")

        video_rows = cursor.fetchall()

        video_data = []

        for row in video_rows:
            """
            !NOTE For reference
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
            """
            row_dict = {
                "videoID": row[0],
                "filePath": row[1],
                "fileName": row[2],
                "videoDuration": row[3],
                "timeStamp": row[4],
                "whichCamera": row[5],
                "resolution": row[6],
                "gpsLat": row[7],
                "gpsLong": row[8],
                "location": row[9]
            }
            video_data.append(row_dict)

        cursor.execute("SELECT * FROM astroStatus")

        astroStatus_rows = cursor.fetchall()

        astroStatus_data = []

        for row in astroStatus_rows:
            """
            !NOTE For reference
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
            """
            row_dict = {
                "astroStatusID": row[0],
                "batteryLife": row[1],
                "locationInSchool": row[2],
                "gpsStatus": row[3],
                "gpsLat": row[4],
                "gpsLong": row[5],
                "camFrontStatus": row[6],
                "camRearStatus": row[7],
                "currentTask": row[8],
                "timeStamp": row[9],
                "errorLog": row[10]
            }
            astroStatus_data.append(row_dict)

        cursor.execute("SELECT * FROM sensorReadings")

        sensor_rows = cursor.fetchall()

        sensor_data = []

        for row in sensor_rows:
            """
            !NOTE For reference
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
            """
            row_dict = {
                "readingID": row[0],
                "gasReading": row[1],
                "tempHumiReading": row[2],
                "usReading": row[3],
                "severity": row[4],
                "timeStamp": row[5],
                "gpsLat": row[6],
                "gpsLong": row[7]
            }
            sensor_data.append(row_dict)

        cursor.execute("SELECT * FROM events")

        event_rows = cursor.fetchall()

        event_data = []

        for row in event_rows:
            """
            !NOTE For reference
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
            """
            row_dict = {
                "eventID": row[0],
                "videoID": row[1],
                "astroStatusID": row[2],
                "readingID": row[3],
                "eventType": row[4],
                "confidence": row[5],
                "urgency": row[6],
                "timeStamp": row[7],
                "detectedBy": row[8],
                "whereOccured": row[9],
                "gpsLat": row[10],
                "gpsLong": row[11],
                "eventReport": row[12]
            }
            event_data.append(row_dict)

        return video_data, astroStatus_data, sensor_data, event_data

    except sql.Error as e:
        print(f"Sqlite error occurred: {e}")
        db_conn.rollback()

    except Exception as e:
        print(f"An error occurred: {e}")
        db_conn.rollback()

    finally:
        if db_conn is not None:
            db_conn.close()


def delete_row_videos(row):
    """
    All 4 delete_row functions are identical in a sense, they each take row as an argument and deletes the row from it's respective table. row is gathered from each build_gui's iterating i variable.
    """
    try:
        db_conn = sql.connect('astro_db.db')

        cursor = db_conn.cursor()

        cursor.execute(f"DELETE FROM videos WHERE videoID = {row}")
        db_conn.commit()

        build_videos_gui()

    except sql.Error as e:
        print(f"Sqlite error occurred: {e}")
        db_conn.rollback()

    except Exception as e:
        print(f"An error occurred: {e}")
        db_conn.rollback()

    finally:
        if db_conn is not None:
            db_conn.close()


def delete_row_sensor(row):

    try:
        db_conn = sql.connect('astro_db.db')

        cursor = db_conn.cursor()

        cursor.execute(f"DELETE FROM sensorReadings WHERE readingID = {row}")
        db_conn.commit()

        build_sensor_readings_gui()

    except sql.Error as e:
        print(f"Sqlite error occurred: {e}")
        db_conn.rollback()

    except Exception as e:
        print(f"An error occurred: {e}")
        db_conn.rollback()

    finally:
        if db_conn is not None:
            db_conn.close()


def delete_row_status(row):

    try:
        db_conn = sql.connect('astro_db.db')

        cursor = db_conn.cursor()

        cursor.execute(f"DELETE FROM astroStatus WHERE astroStatusID = {row}")
        db_conn.commit()

        build_astro_status_gui()

    except sql.Error as e:
        print(f"Sqlite error occurred: {e}")
        db_conn.rollback()

    except Exception as e:
        print(f"An error occurred: {e}")
        db_conn.rollback()

    finally:
        if db_conn is not None:
            db_conn.close()


def delete_row_event(row):

    try:
        db_conn = sql.connect('astro_db.db')

        cursor = db_conn.cursor()

        cursor.execute(f"DELETE FROM events WHERE eventID = {row}")
        db_conn.commit()

        build_events_gui()

    except sql.Error as e:
        print(f"Sqlite error occurred: {e}")
        db_conn.rollback()

    except Exception as e:
        print(f"An error occurred: {e}")
        db_conn.rollback()

    finally:
        if db_conn is not None:
            db_conn.close()


def update_video_row(row):
    """
    takes row as an agrument, creates a frame with a radio button menu to select what to change and a field entry for what to fill it with. error checking and data integrity will need to be added
    TODO DATA INTEGRITY AND ERROR CHECKING
    """

    try:
        db_conn = sql.connect('astro_db.db')

        cursor = db_conn.cursor()

        new_value_frame = tk.Frame(root, width=500, height=500)
        new_value_frame.pack(padx=10, pady=10)
        fields_frame = tk.Frame(new_value_frame, relief="sunken")
        fields_frame.grid(row=0, column=0)
        col_choice = tk.StringVar()

        video_fields = ("videoID", "filePath", "fileName", "videoDuration",
                        "timeStamp", "whichCamera", "resolution", "gpsLat", "gpsLong", "location")
        i = 0  # for cols
        for field in video_fields:  # makes the radio buttons nice and easy
            button = tk.Radiobutton(
                fields_frame, text=f"{field}", variable=col_choice, value=f"{field}").grid(row=0, column=i)
            i += 1

        new_value_entry = tk.Entry(new_value_frame, width=60)
        new_value_entry.grid(row=2, column=0)
        new_value = tk.StringVar()

        def set_value(): return new_value.set(new_value_entry.get())

        confirm_button = tk.Button(new_value_frame, text="Confirm Entry",  background="light blue",  command=lambda: (set_value(), cursor.execute(
            f"UPDATE videos SET {col_choice.get()} = ? WHERE videoID = {row}", (new_value.get(),)), db_conn.commit(), build_videos_gui())).grid(row=3, column=0, pady=5)

        cancel_button = tk.Button(new_value_frame, text="Cancel", background="red",
                                  command=new_value_frame.destroy).grid(row=3, column=1)

        """This confirm button is a lot to take in, it uses lambda to bypass command's 1 function limitation, sticks 4 commands into a tuple within the lambda to do a lot in one button press. set value updates new_value to the text entered in the entry field, then it uses the cursor to execute the change using the data collected from the entry field, what field needs to be changed from the radio button, and the row the update button that was pressed. Then it commits it and rebuilds the database frame to update the data as well as destroy the field update frame"""
    except sql.Error as e:
        print(f"Sqlite error occurred: {e}")
        messagebox.showerror("ERROR", "An error occured, please try again")
        db_conn.rollback()

    except Exception as e:
        print(f"An error occurred: {e}")
        messagebox.showerror("ERROR", "An error occured, please try again")
        db_conn.rollback()


def update_astro_status_row(row):
    """
    takes row as an agrument, creates a frame with a radio button menu to select what to change and a field entry for what to fill it with. error checking and data integrity will need to be added
    TODO DATA INTEGRITY AND ERROR CHECKING
    """

    try:
        db_conn = sql.connect('astro_db.db')

        cursor = db_conn.cursor()

        new_value_frame = tk.Frame(root, width=500, height=500)
        new_value_frame.pack(padx=10, pady=10)
        fields_frame = tk.Frame(new_value_frame, relief="sunken")
        fields_frame.grid(row=0, column=0)
        col_choice = tk.StringVar()

        fields = ("astroStatusID", "batteryLife", "locationInSchool", "gpsStatus", "gpsLat", "gpsLong",
                  "camFrontStatus", "camRearStatus", "currentTask", "timeStamp", "errorLog")
        i = 0  # for cols
        for field in fields:  # makes the radio buttons nice and easy
            button = tk.Radiobutton(
                fields_frame, text=f"{field}", variable=col_choice, value=f"{field}").grid(row=0, column=i)
            i += 1

        new_value_entry = tk.Entry(new_value_frame, width=60)
        new_value_entry.grid(row=2, column=0)
        new_value = tk.StringVar()

        def set_value(): return new_value.set(new_value_entry.get())

        confirm_button = tk.Button(new_value_frame, text="Confirm Entry",  background="light blue",  command=lambda: (set_value(), cursor.execute(
            f"UPDATE astroStatus SET {col_choice.get()} = ? WHERE astroStatusID = {row}", (new_value.get(),)), db_conn.commit(), build_astro_status_gui())).grid(row=3, column=0, pady=5)

        cancel_button = tk.Button(new_value_frame, text="Cancel", background="red",
                                  command=new_value_frame.destroy).grid(row=3, column=1)

        """This confirm button is a lot to take in, it uses lambda to bypass command's 1 function limitation, sticks 4 commands into a tuple within the lambda to do a lot in one button press. set value updates new_value to the text entered in the entry field, then it uses the cursor to execute the change using the data collected from the entry field, what field needs to be changed from the radio button, and the row the update button that was pressed. Then it commits it and rebuilds the database frame to update the data as well as destroy the field update frame"""
    except sql.Error as e:
        print(f"Sqlite error occurred: {e}")
        messagebox.showerror("ERROR", "An error occured, please try again")
        db_conn.rollback()

    except Exception as e:
        print(f"An error occurred: {e}")
        messagebox.showerror("ERROR", "An error occured, please try again")
        db_conn.rollback()


def update_sensor_row(row):
    """
    takes row as an agrument, creates a frame with a radio button menu to select what to change and a field entry for what to fill it with. error checking and data integrity will need to be added
    TODO DATA INTEGRITY AND ERROR CHECKING
    """

    try:
        db_conn = sql.connect('astro_db.db')

        cursor = db_conn.cursor()

        new_value_frame = tk.Frame(root, width=500, height=500)
        new_value_frame.pack(padx=10, pady=10)
        fields_frame = tk.Frame(new_value_frame, relief="sunken")
        fields_frame.grid(row=0, column=0)
        col_choice = tk.StringVar()

        fields = ("readingID", "gasReading", "tempHumiReading", "usReading", "severity",
                  "timeStamp", "gpsLat", "gpsLong")
        i = 0  # for cols
        for field in fields:  # makes the radio buttons nice and easy
            button = tk.Radiobutton(
                fields_frame, text=f"{field}", variable=col_choice, value=f"{field}").grid(row=0, column=i)
            i += 1

        new_value_entry = tk.Entry(new_value_frame, width=60)
        new_value_entry.grid(row=2, column=0)
        new_value = tk.StringVar()

        def set_value(): return new_value.set(new_value_entry.get())

        confirm_button = tk.Button(new_value_frame, text="Confirm Entry",  background="light blue",  command=lambda: (set_value(), cursor.execute(
            f"UPDATE sensorReadings SET {col_choice.get()} = ? WHERE readingID = {row}", (new_value.get(),)), db_conn.commit(), build_sensor_readings_gui())).grid(row=3, column=0, pady=5)

        cancel_button = tk.Button(new_value_frame, text="Cancel", background="red",
                                  command=new_value_frame.destroy).grid(row=3, column=1)

        """This confirm button is a lot to take in, it uses lambda to bypass command's 1 function limitation, sticks 4 commands into a tuple within the lambda to do a lot in one button press. set value updates new_value to the text entered in the entry field, then it uses the cursor to execute the change using the data collected from the entry field, what field needs to be changed from the radio button, and the row the update button that was pressed. Then it commits it and rebuilds the database frame to update the data as well as destroy the field update frame"""
    except sql.Error as e:
        print(f"Sqlite error occurred: {e}")
        messagebox.showerror("ERROR", "An error occured, please try again")
        db_conn.rollback()

    except Exception as e:
        print(f"An error occurred: {e}")
        messagebox.showerror("ERROR", "An error occured, please try again")
        db_conn.rollback()


def update_event_row(row):
    """
    takes row as an agrument, creates a frame with a radio button menu to select what to change and a field entry for what to fill it with. error checking and data integrity will need to be added
    TODO DATA INTEGRITY AND ERROR CHECKING
    """

    try:
        db_conn = sql.connect('astro_db.db')

        cursor = db_conn.cursor()

        new_value_frame = tk.Frame(root, width=500, height=500)
        new_value_frame.pack(padx=10, pady=10)
        fields_frame = tk.Frame(new_value_frame, relief="sunken")
        fields_frame.grid(row=0, column=0)
        col_choice = tk.StringVar()

        fields = ("eventID", "videoID", "astroStatusID", "readingID", "eventType", "confidence",
                  "urgency", "timeStamp", "detectedBy", "whereOccured", "gpsLat", "gpsLong", "eventReport")
        i = 0  # for cols
        for field in fields:  # makes the radio buttons nice and easy
            button = tk.Radiobutton(
                fields_frame, text=f"{field}", variable=col_choice, value=f"{field}").grid(row=0, column=i)
            i += 1

        new_value_entry = tk.Entry(new_value_frame, width=60)
        new_value_entry.grid(row=2, column=0)
        new_value = tk.StringVar()

        def set_value(): return new_value.set(new_value_entry.get())

        confirm_button = tk.Button(new_value_frame, text="Confirm Entry",  background="light blue",  command=lambda: (set_value(), cursor.execute(
            f"UPDATE events SET {col_choice.get()} = ? WHERE eventID = {row}", (new_value.get(),)), db_conn.commit(), build_events_gui())).grid(row=3, column=0, pady=5)

        cancel_button = tk.Button(new_value_frame, text="Cancel", background="red",
                                  command=new_value_frame.destroy).grid(row=3, column=1)

        """This confirm button is a lot to take in, it uses lambda to bypass command's 1 function limitation, sticks 4 commands into a tuple within the lambda to do a lot in one button press. set value updates new_value to the text entered in the entry field, then it uses the cursor to execute the change using the data collected from the entry field, what field needs to be changed from the radio button, and the row the update button that was pressed. Then it commits it and rebuilds the database frame to update the data as well as destroy the field update frame"""

    except sql.Error as e:
        print(f"Sqlite error occurred: {e}")
        messagebox.showerror("ERROR", "An error occured, please try again")
        db_conn.rollback()

    except Exception as e:
        print(f"An error occurred: {e}")
        messagebox.showerror("ERROR", "An error occured, please try again")
        db_conn.rollback()


def build_videos_gui():
    """
    This docstring applies to all 4 build_{tablename}_gui functions
    this function starts by destroying the current window. (I got that code from the coffee/donut shop project in advanced python) it then creates a new window. It uses the turn_tables_into_list_of_dicts function and assigns the values returned, it then uses only the relevant one to create the table by looping over the list of dictionaries the turn_tables_into_list_of_dicts function returns then assigning each row a dictionary, and each column of that row with it's respective dictionary value. It then goes and does the next row/dict. 
    """

    for widget in root.winfo_children():  # From homework file in advanced python, it destroys the previous window
        if isinstance(widget, tk.Frame):
            widget.destroy()  # end

    video_frame = tk.Frame(root)
    video_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # CANVAS
    video_canvas = tk.Canvas(video_frame)
    video_canvas.pack(side="left", fill="both", expand=True)

    # SCROLLER
    video_scroll_bar = ttk.Scrollbar(
        video_frame, orient="vertical", command=video_canvas.yview)
    video_scroll_bar.pack(side="right", fill="y")

    # CONFIG CANVAS
    video_canvas.configure(yscrollcommand=video_scroll_bar.set)

    # Frame inside canvas
    video_frame2 = tk.Frame(video_canvas)
    video_frame2.bind('<Configure>', lambda e: video_canvas.configure(
        scrollregion=video_canvas.bbox("all")))
    # Add new freame to window in canvas
    video_canvas.create_window((0, 0), window=video_frame2, anchor="nw")

    video_data, astroStatus_data, sensor_data, event_data = turn_tables_into_list_of_dicts()

    tk.Label(video_frame2, text="Videos", font=("TkDefaultFont", 14, "bold")).grid(
        row=0, column=0, columnspan=2, pady=5, padx=5)

    field_col = 0
    field_labels = ("videoID", "filePath", "fileName",
                    "videoDuration", "timeStamp", "whichCamera", "resolution", "gpsLat", "gpsLong", "location")
    for field_label in field_labels:
        tk.Label(video_frame2, text=f"{field_label}", background="white", width=15).grid(
            row=1, column=field_col, padx=1, pady=1)
        field_col += 1
    i = 2
    for data in video_data:
        tk.Label(video_frame2, text=f"{data['videoID']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=0)
        tk.Label(video_frame2, text=f"{data['filePath']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=1)
        tk.Label(video_frame2, text=f"{data['fileName']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=2)
        tk.Label(video_frame2, text=f"{data['videoDuration']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=3)
        tk.Label(video_frame2, text=f"{data['timeStamp']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=4)
        tk.Label(video_frame2, text=f"{data['whichCamera']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=5)
        tk.Label(video_frame2, text=f"{data['resolution']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=6)
        tk.Label(video_frame2, text=f"{data['gpsLat']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=7)
        tk.Label(video_frame2, text=f"{data['gpsLong']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=8)
        tk.Label(video_frame2, text=f"{data['location']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=9)

        # Delete specific row
        tk.Button(video_frame2, text="Delete row", background="dark red",
                  foreground="white", width=10, command=lambda id=data['videoID']:  delete_row_videos(id)).grid(row=i, column=10)

        # Update specific row
        tk.Button(video_frame2, text="Update row", background="teal", foreground="white", width=10,
                  command=lambda id=data['videoID']:  update_video_row(id)).grid(row=i, column=11)
        i += 1


def build_astro_status_gui():
    """
    This docstring applies to all 4 build_{tablename}_gui functions
    this function starts by destroying the current window. (I got that code from the coffee/donut shop project in advanced python) it then creates a new window. It uses the turn_tables_into_list_of_dicts function and assigns the values returned, it then uses only the relevant one to create the table by looping over the list of dictionaries the turn_tables_into_list_of_dicts function returns then assigning each row a dictionary, and each column of that row with it's respective dictionary value. It then goes and does the next row/dict. 
    """

    for widget in root.winfo_children():  # From homework file in advanced python
        if isinstance(widget, tk.Frame):
            widget.destroy()  # end

    status_frame = tk.Frame(root)
    status_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # CANVAS
    status_canvas = tk.Canvas(status_frame)
    status_canvas.pack(side="top", fill="both", expand=True)

    # SCROLLER
    status_scroll_bar_y = ttk.Scrollbar(
        status_frame, orient="vertical", command=status_canvas.yview)
    status_scroll_bar_y.pack(side="right", fill="y")

    status_scroll_bar_x = ttk.Scrollbar(
        status_frame, orient="horizontal", command=status_canvas.xview)
    status_scroll_bar_x.pack(side="bottom", fill="x")

    # CONFIG CANVAS
    status_canvas.configure(
        yscrollcommand=status_scroll_bar_y.set)

    status_canvas.configure(
        xscrollcommand=status_scroll_bar_x.set)

    # Frame inside canvas
    status_frame2 = tk.Frame(status_canvas)
    status_frame2.bind('<Configure>', lambda e: status_canvas.configure(
        scrollregion=status_canvas.bbox("all")))

    # Add new frame to window in canvas
    status_canvas.create_window(
        (0, 0), window=status_frame2, anchor="nw")

    video_data, astroStatus_data, sensor_data, event_data = turn_tables_into_list_of_dicts()

    tk.Label(status_frame2, text="Astro's Status", font=("TkDefaultFont", 14, "bold")).grid(
        row=0, column=0, columnspan=2, pady=5, padx=5)

    field_col = 0
    field_labels = ("astroStatusID", "batteryLife", "locationInSchool",
                    "gpsStatus", "gpsLat", "gpsLong", "camFrontStatus", "camRearStatus", "currentTask", "timeStamp", "errorLog")
    for field_label in field_labels:
        tk.Label(status_frame2, text=f"{field_label}", background="white", width=15).grid(
            row=1, column=field_col, padx=1, pady=1)
        field_col += 1
    i = 2
    for data in astroStatus_data:
        tk.Label(status_frame2, text=f"{data['astroStatusID']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=0)
        tk.Label(status_frame2, text=f"{data['batteryLife']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=1)
        tk.Label(status_frame2, text=f"{data['locationInSchool']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=2)
        tk.Label(status_frame2, text=f"{data['gpsStatus']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=3)
        tk.Label(status_frame2, text=f"{data['gpsLat']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=4)
        tk.Label(status_frame2, text=f"{data['gpsLong']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=5)
        tk.Label(status_frame2, text=f"{data['camFrontStatus']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=6)
        tk.Label(status_frame2, text=f"{data['camRearStatus']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=7)
        tk.Label(status_frame2, text=f"{data['currentTask']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=8)
        tk.Label(status_frame2, text=f"{data['timeStamp']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=9)
        tk.Label(status_frame2, text=f"{data['errorLog']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=10)

        # Delete specific row
        tk.Button(status_frame2, text="Delete row", background="dark red",
                  foreground="white", width=10, command=lambda id=data['astroStatusID']:  delete_row_status(id)).grid(row=i, column=11)

        # Update specific row
        tk.Button(status_frame2, text="Update row", background="teal", foreground="white", width=10,
                  command=lambda id=data['astroStatusID']:  update_astro_status_row(id)).grid(row=i, column=12)
        i += 1


def build_sensor_readings_gui():
    """
    This docstring applies to all 4 build_{tablename}_gui functions
    this function starts by destroying the current window. (I got that code from the coffee/donut shop project in advanced python) it then creates a new window. It uses the turn_tables_into_list_of_dicts function and assigns the values returned, it then uses only the relevant one to create the table by looping over the list of dictionaries the turn_tables_into_list_of_dicts function returns then assigning each row a dictionary, and each column of that row with it's respective dictionary value. It then goes and does the next row/dict. 
    """

    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame):
            widget.destroy()

    sensor_readings_frame = tk.Frame(root)
    sensor_readings_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # CANVAS
    sensor_readings_canvas = tk.Canvas(sensor_readings_frame)
    sensor_readings_canvas.pack(side="left", fill="both", expand=True)

    # SCROLLER
    sensor_readings_scroll_bar_y = ttk.Scrollbar(
        sensor_readings_frame, orient="vertical", command=sensor_readings_canvas.yview)
    sensor_readings_scroll_bar_y.pack(side="right", fill="y")

    sensor_readings_scroll_bar_x = ttk.Scrollbar(
        sensor_readings_frame, orient="horizontal", command=sensor_readings_canvas.xview)
    sensor_readings_scroll_bar_x.pack(side="bottom", fill="x")

    # CONFIG CANVAS
    sensor_readings_canvas.configure(
        yscrollcommand=sensor_readings_scroll_bar_y.set)

    sensor_readings_canvas.configure(
        xscrollcommand=sensor_readings_scroll_bar_x.set)

    sensor_readings_frame2 = tk.Frame(sensor_readings_canvas)

    sensor_readings_frame2.bind('<Configure>', lambda e: sensor_readings_canvas.configure(
        scrollregion=sensor_readings_canvas.bbox("all")))
    # Frame inside canvas

    # Add new freame to window in canvas
    sensor_readings_canvas.create_window(
        (0, 0), window=sensor_readings_frame2, anchor="nw")

    video_data, astroStatus_data, sensor_data, event_data = turn_tables_into_list_of_dicts()

    tk.Label(sensor_readings_frame2, text="Sensor Data", font=("TkDefaultFont", 14, "bold")).grid(
        row=0, column=0, columnspan=2, pady=5, padx=5)

    field_col = 0
    field_labels = (
        "readingID", "gasReading", "THReading", "usReading",
        "severity", "timeStamp", "gpsLat", "gpsLong"
    )
    for field_label in field_labels:
        tk.Label(sensor_readings_frame2, text=f"{field_label}", background="white", width=15).grid(
            row=1, column=field_col, padx=1, pady=1)
        field_col += 1

    i = 2
    for data in sensor_data:
        tk.Label(sensor_readings_frame2, text=f"{data['readingID']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=0)
        tk.Label(sensor_readings_frame2, text=f"{data['gasReading']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=1)
        tk.Label(sensor_readings_frame2, text=f"{data['tempHumiReading']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=2)
        tk.Label(sensor_readings_frame2, text=f"{data['usReading']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=3)
        tk.Label(sensor_readings_frame2, text=f"{data['severity']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=4)
        tk.Label(sensor_readings_frame2, text=f"{data['timeStamp']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=5)
        tk.Label(sensor_readings_frame2, text=f"{data['gpsLat']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=6)
        tk.Label(sensor_readings_frame2, text=f"{data['gpsLong']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=7)

        tk.Button(sensor_readings_frame2, text="Delete row", background="dark red",
                  foreground="white", width=10, command=lambda id=data['readingID']:  delete_row_sensor(id)).grid(row=i, column=8)

        # Update specific row
        tk.Button(sensor_readings_frame2, text="Update row", background="teal", foreground="white", width=10,
                  command=lambda id=data['readingID']:  update_sensor_row(id)).grid(row=i, column=9)
        i += 1


def build_events_gui():
    """
    This docstring applies to all 4 build_{tablename}_gui functions
    this function starts by destroying the current window. (I got that code from the coffee/donut shop project in advanced python) it then creates a new window. It uses the turn_tables_into_list_of_dicts function and assigns the values returned, it then uses only the relevant one to create the table by looping over the list of dictionaries the turn_tables_into_list_of_dicts function returns then assigning each row a dictionary, and each column of that row with it's respective dictionary value. It then goes and does the next row/dict. 
    """

    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame):
            widget.destroy()

    event_frame = tk.Frame(root)
    event_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # CANVAS
    event_canvas = tk.Canvas(event_frame)
    event_canvas.pack(side="top", fill="both", expand=True)

    # SCROLLER
    event_scroll_bar_y = ttk.Scrollbar(
        event_frame, orient="vertical", command=event_canvas.yview)
    event_scroll_bar_y.pack(side="right", fill="y")

    event_scroll_bar_x = ttk.Scrollbar(
        event_frame, orient="horizontal", command=event_canvas.xview)
    event_scroll_bar_x.pack(side="bottom", fill="x")

    # CONFIG CANVAS
    event_canvas.configure(
        yscrollcommand=event_scroll_bar_y.set)

    event_canvas.configure(
        xscrollcommand=event_scroll_bar_x.set)
    # event_canvas.bind('<Configure>', lambda e: event_canvas.configure(
    #     scrollregion=event_canvas.bbox("all")))
    # Frame inside canvas
    event_frame2 = tk.Frame(event_canvas)
    event_frame2.bind('<Configure>', lambda e: event_canvas.configure(
        scrollregion=event_canvas.bbox("all")))
    # Add new freame to window in canvas
    event_canvas.create_window(
        (0, 0), window=event_frame2, anchor="nw")

    video_data, astroStatus_data, sensor_data, event_data = turn_tables_into_list_of_dicts()

    tk.Label(event_frame2, text="Events", font=("TkDefaultFont", 14, "bold")).grid(
        row=0, column=0, columnspan=2, pady=5, padx=5)

    field_col = 0
    field_labels = (
        "eventID", "videoID", "astroStatusID", "readingID",
        "eventType", "confidence", "urgency", "timeStamp",
        "detectedBy", "whereOccured", "gpsLat", "gpsLong", "eventReport"
    )
    for field_label in field_labels:
        if "eventReport" not in field_label:
            tk.Label(event_frame2, text=f"{field_label}", background="white", width=15).grid(
                row=1, column=field_col, padx=1, pady=1)
        elif "eventReport" in field_label:
            tk.Label(event_frame2, text=f"{field_label}", background="white", width=25).grid(
                row=1, column=field_col, padx=1, pady=1)
        field_col += 1

    i = 2
    for data in event_data:
        tk.Label(event_frame2, text=f"{data['eventID']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=0)
        tk.Label(event_frame2, text=f"{data['videoID']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=1)
        tk.Label(event_frame2, text=f"{data['astroStatusID']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=2)
        tk.Label(event_frame2, text=f"{data['readingID']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=3)
        tk.Label(event_frame2, text=f"{data['eventType']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=4)
        tk.Label(event_frame2, text=f"{data['confidence']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=5)
        tk.Label(event_frame2, text=f"{data['urgency']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=6)
        tk.Label(event_frame2, text=f"{data['timeStamp']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=7)
        tk.Label(event_frame2, text=f"{data['detectedBy']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=8)
        tk.Label(event_frame2, text=f"{data['whereOccured']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=9)
        tk.Label(event_frame2, text=f"{data['gpsLat']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=10)
        tk.Label(event_frame2, text=f"{data['gpsLong']}", background="light grey", borderwidth=1, width=15, relief="ridge").grid(
            row=i, column=11)
        tk.Label(event_frame2, text=f"{data['eventReport']}", background="light grey", borderwidth=1, width=25, relief="ridge").grid(
            row=i, column=12)

        tk.Button(event_frame2, text="Delete row", background="dark red",
                  foreground="white", width=10, command=lambda id=data['eventID']:  delete_row_event(id)).grid(row=i, column=13)

        tk.Button(event_frame2, text="Update row", background="teal", foreground="white", width=10,
                  command=lambda id=data['eventID']:  update_event_row(id)).grid(row=i, column=14)
        i += 1


def make_menu():
    """
    Adapted from an assignment in Python 2 (Coffee/donut shop)
    """
    video_menu = tk.Menu(menu_bar, tearoff=0)
    astro_status_menu = tk.Menu(menu_bar, tearoff=0)
    sensor_readings_menu = tk.Menu(menu_bar, tearoff=0)
    events_menu = tk.Menu(menu_bar, tearoff=0)
    pull_data_menu = tk.Menu(menu_bar, tearoff=0)
    table_manip_menu = tk.Menu(menu_bar, tearoff=0)

    msgbox = MessageBoxes()

    menu_bar.add_cascade(label="Videos", menu=video_menu)
    menu_bar.add_cascade(label="Astro's Status", menu=astro_status_menu)
    menu_bar.add_cascade(label="Sensor Readings", menu=sensor_readings_menu)
    menu_bar.add_cascade(label="Events", menu=events_menu)
    menu_bar.add_cascade(label="Pull Data", menu=pull_data_menu)
    menu_bar.add_cascade(label="Table Manipulation", menu=table_manip_menu)

    video_menu.add_command(label="Show Videos", command=build_videos_gui)
    video_menu.add_command(label="Refresh", command=build_videos_gui)

    astro_status_menu.add_command(
        label="Show Astro's Status", command=build_astro_status_gui)
    astro_status_menu.add_command(
        label="Refresh", command=build_astro_status_gui)

    sensor_readings_menu.add_command(
        label="Show Sensor Readings", command=build_sensor_readings_gui)
    sensor_readings_menu.add_command(
        label="Refresh", command=build_sensor_readings_gui)

    events_menu.add_command(label="Show Events", command=build_events_gui)
    events_menu.add_command(label="Refresh", command=build_events_gui)

    pull_data_menu.add_command(
        label="Pull Video Data", command=lambda: (commit_videos(fake_videos_data), build_videos_gui()))
    pull_data_menu.add_command(
        label="Pull Astro's Status Data", command=lambda: (commit_astro_status(fake_astro_status_data), build_astro_status_gui()))
    pull_data_menu.add_command(
        label="Pull Sensor Data", command=lambda: (commit_sensor_data(fake_sensor_readings_data), build_sensor_readings_gui()))
    pull_data_menu.add_command(
        label="Pull Event Data", command=lambda: (commit_event_data(fake_events_data), build_events_gui()))

    table_manip_menu.add_command(
        label="Drop All Tables", command=msgbox.ask_yes_no)

    table_manip_menu.add_command(label="Refresh", command=build_videos_gui)

    table_manip_menu.add_command(
        label="Restore Empty Tables", command=restore_empty_tables)


def main():
    """
    This was the simplist way I could think to make sure this runs properly each time.
    If I tried just a build gui function but there was no tables in the database file, the build guis can't work. So this tries the turn tables into dicts function and if that works it builds the first screen, if it doesn't I have a blanket exception to restore the empty tables then build the gui. Also I only call main now rather than multiple things.
    """
    try:
        v, a_s, s_r, e = turn_tables_into_list_of_dicts()
        make_menu()
        build_videos_gui()
        root.mainloop()
    except:
        restore_empty_tables()
        make_menu()
        build_videos_gui()
        root.mainloop()


main()
