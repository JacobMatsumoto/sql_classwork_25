"""
    Astro Database project

    References used or found below
    https://docs.python.org/3/library/sqlite3.html  NOTE Briefly skimmed. Keep reading.

    Short python file utilizing placeholder fake data in order to try to do a small commit of data to the database. I create some fake data and then verify that it is either a tuple or a list, and that it isn't empty, then I stick it into the database. This happpens for each individual table. appending to the database is fully scaleable thanks to executemany. However I am hitting a snag with figuring out how to properly scale a GUI for an easier way to display data. I have a start for it in the wip function (work in progress wip). If anyone has suggestions and experience with python's tkinter, I would greatly appreciate suggestions! Thank you!

"""

import sqlite3 as sql
import tkinter as tk
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
    confirmed = False
    try:
        while not confirmed:
            try:

                user_input = int(input("Are you sure you want to drop all tables? \n"
                                       "Enter 1 if yes\n"
                                       "Enter 0 if no\n"
                                       "Enter:"))
                if user_input == 1:
                    db_conn = sql.connect('astro_db.db')
                    cursor = db_conn.cursor()

                    cursor.execute("""DROP TABLE IF EXISTS events""")

                    cursor.execute("""DROP TABLE IF EXISTS astroStatus""")

                    cursor.execute("""DROP TABLE IF EXISTS videos""")

                    cursor.execute("""DROP TABLE IF EXISTS sensorReadings""")

                    print("All tables dropped. Commiting...")

                    db_conn.commit()  # comment out for tests without pushing data in

                    confirmed = True

                elif user_input == 0:
                    print("Good choice. Database not dropped")
                    confirmed = True
                else:
                    print(
                        "Invalid input. Please enter a 0 to exit enter a 1 to drop everything")
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

    except sql.Error as e:
        print(f"Sqlite error occurred: {e}")
        db_conn.rollback()

    except Exception as e:
        print(f"An error occurred: {e}")
        db_conn.rollback()

    finally:
        if db_conn is not None:
            db_conn.close()


# temporary fake data, list of tuples.
fake_videos_data = [
    (1, '/videos/front_cam/', 'front_001.mp4', '00:01:23',
     '2025-11-16 14:32:00', 'front', '1080p', 42.2598, -88.3683, 'Main Hall'),
    (2, '/videos/rear_cam/', 'rear_002.mp4', '00:02:10',
     '2025-11-16 14:35:00', 'rear', '720p', 42.2598, -88.3683, 'Science Wing')
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




def build_videos_gui():
    """
    This docstring applies to all 4 build_{tablename}_gui functions
    this function starts by destroying the current window. (I got that code from the coffee/donut shop project in advanced python) it then creates a new window. It uses the turn_tables_into_list_of_dicts function and assigns the values returned, it then uses only the relevant one to create the table by looping over the list of dictionaries the turn_tables_into_list_of_dicts function returns then assigning each row a dictionary, and each column of that row with it's respective dictionary value. It then goes and does the next row/dict. 
    """

    for widget in root.winfo_children():  # From homework file in advanced python, it destroys the previous window
        if isinstance(widget, tk.Frame):
            widget.destroy()  # end

    video_frame = tk.Frame(root)
    video_frame.pack(padx=10, pady=10)

    video_data, astroStatus_data, sensor_data, event_data = turn_tables_into_list_of_dicts()

    tk.Label(video_frame, text="Videos", font=("TkDefaultFont", 14, "bold")).grid(
        row=0, column=0, columnspan=2, pady=5, padx=5)
    
    field_col = 0
    field_labels = ("videoID", "filePath", "fileName",
                    "videoDuration", "timeStamp", "whichCamera", "resolution", "gpsLat", "gpsLong", "location")
    for field_label in field_labels:
        tk.Label(video_frame, text=f"{field_label}").grid(
            row=1, column=field_col, padx=10, pady=5)
        field_col += 1
    i = 2
    for data in video_data:
        tk.Label(video_frame, text=f"{data['videoID']}").grid(
            row=i, column=0, padx=10, pady=5)
        tk.Label(video_frame, text=f"{data['filePath']}").grid(
            row=i, column=1, padx=10, pady=5)
        tk.Label(video_frame, text=f"{data['fileName']}").grid(
            row=i, column=2, padx=10, pady=5)
        tk.Label(video_frame, text=f"{data['videoDuration']}").grid(
            row=i, column=3, padx=10, pady=5)
        tk.Label(video_frame, text=f"{data['timeStamp']}").grid(
            row=i, column=4, padx=10, pady=5)
        tk.Label(video_frame, text=f"{data['whichCamera']}").grid(
            row=i, column=5, padx=10, pady=5)
        tk.Label(video_frame, text=f"{data['resolution']}").grid(
            row=i, column=6, padx=10, pady=5)
        tk.Label(video_frame, text=f"{data['gpsLat']}").grid(
            row=i, column=7, padx=10, pady=5)
        tk.Label(video_frame, text=f"{data['gpsLong']}").grid(
            row=i, column=8, padx=10, pady=5)
        tk.Label(video_frame, text=f"{data['location']}").grid(
            row=i, column=9, padx=10, pady=5)
        i += 1


def build_astro_status_gui():
    """
    This docstring applies to all 4 build_{tablename}_gui functions
    this function starts by destroying the current window. (I got that code from the coffee/donut shop project in advanced python) it then creates a new window. It uses the turn_tables_into_list_of_dicts function and assigns the values returned, it then uses only the relevant one to create the table by looping over the list of dictionaries the turn_tables_into_list_of_dicts function returns then assigning each row a dictionary, and each column of that row with it's respective dictionary value. It then goes and does the next row/dict. 
    """

    for widget in root.winfo_children():  # From homework file in advanced python
        if isinstance(widget, tk.Frame):
            widget.destroy()  # end

    astro_status_frame = tk.Frame(root)
    astro_status_frame.pack(padx=10, pady=10)

    video_data, astroStatus_data, sensor_data, event_data = turn_tables_into_list_of_dicts()

    tk.Label(astro_status_frame, text="Astro's Status", font=("TkDefaultFont", 14, "bold")).grid(
        row=0, column=0, columnspan=2, pady=5, padx=5)

    field_col = 0
    field_labels = ("astroStatusID", "batteryLife", "locationInSchool",
                    "gpsStatus", "gpsLat", "gpsLong", "camFrontStatus", "camRearStatus", "currentTask", "timeStamp", "errorLog")
    for field_label in field_labels:
        tk.Label(astro_status_frame, text=f"{field_label}").grid(
            row=1, column=field_col, padx=10, pady=5)
        field_col += 1
    i = 2
    for data in astroStatus_data:
        tk.Label(astro_status_frame, text=f"{data['astroStatusID']}").grid(
            row=i, column=0, padx=10, pady=5)
        tk.Label(astro_status_frame, text=f"{data['batteryLife']}").grid(
            row=i, column=1, padx=10, pady=5)
        tk.Label(astro_status_frame, text=f"{data['locationInSchool']}").grid(
            row=i, column=2, padx=10, pady=5)
        tk.Label(astro_status_frame, text=f"{data['gpsStatus']}").grid(
            row=i, column=3, padx=10, pady=5)
        tk.Label(astro_status_frame, text=f"{data['gpsLat']}").grid(
            row=i, column=4, padx=10, pady=5)
        tk.Label(astro_status_frame, text=f"{data['gpsLong']}").grid(
            row=i, column=5, padx=10, pady=5)
        tk.Label(astro_status_frame, text=f"{data['camFrontStatus']}").grid(
            row=i, column=6, padx=10, pady=5)
        tk.Label(astro_status_frame, text=f"{data['camRearStatus']}").grid(
            row=i, column=7, padx=10, pady=5)
        tk.Label(astro_status_frame, text=f"{data['currentTask']}").grid(
            row=i, column=8, padx=10, pady=5)
        tk.Label(astro_status_frame, text=f"{data['timeStamp']}").grid(
            row=i, column=9, padx=10, pady=5)
        tk.Label(astro_status_frame, text=f"{data['errorLog']}").grid(
            row=i, column=10, padx=10, pady=5)
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
    sensor_readings_frame.pack(padx=10, pady=10)

    video_data, astroStatus_data, sensor_data, event_data = turn_tables_into_list_of_dicts()

    tk.Label(sensor_readings_frame, text="Sensor Data", font=("TkDefaultFont", 14, "bold")).grid(
        row=0, column=0, columnspan=2, pady=5, padx=5)

    field_col = 0
    field_labels = (
        "readingID", "gasReading", "tempHumiReading", "usReading",
        "severity", "timeStamp", "gpsLat", "gpsLong"
    )
    for field_label in field_labels:
        tk.Label(sensor_readings_frame, text=f"{field_label}").grid(
            row=1, column=field_col, padx=10, pady=5)
        field_col += 1

    i = 2
    for data in sensor_data:
        tk.Label(sensor_readings_frame, text=f"{data['readingID']}").grid(
            row=i, column=0, padx=10, pady=5)
        tk.Label(sensor_readings_frame, text=f"{data['gasReading']}").grid(
            row=i, column=1, padx=10, pady=5)
        tk.Label(sensor_readings_frame, text=f"{data['tempHumiReading']}").grid(
            row=i, column=2, padx=10, pady=5)
        tk.Label(sensor_readings_frame, text=f"{data['usReading']}").grid(
            row=i, column=3, padx=10, pady=5)
        tk.Label(sensor_readings_frame, text=f"{data['severity']}").grid(
            row=i, column=4, padx=10, pady=5)
        tk.Label(sensor_readings_frame, text=f"{data['timeStamp']}").grid(
            row=i, column=5, padx=10, pady=5)
        tk.Label(sensor_readings_frame, text=f"{data['gpsLat']}").grid(
            row=i, column=6, padx=10, pady=5)
        tk.Label(sensor_readings_frame, text=f"{data['gpsLong']}").grid(
            row=i, column=7, padx=10, pady=5)
        i += 1


def build_events_gui():
    """
    This docstring applies to all 4 build_{tablename}_gui functions
    this function starts by destroying the current window. (I got that code from the coffee/donut shop project in advanced python) it then creates a new window. It uses the turn_tables_into_list_of_dicts function and assigns the values returned, it then uses only the relevant one to create the table by looping over the list of dictionaries the turn_tables_into_list_of_dicts function returns then assigning each row a dictionary, and each column of that row with it's respective dictionary value. It then goes and does the next row/dict. 
    """
    
    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame):
            widget.destroy()

    events_frame = tk.Frame(root)
    events_frame.pack(padx=10, pady=10)

    video_data, astroStatus_data, sensor_data, event_data = turn_tables_into_list_of_dicts()

    tk.Label(events_frame, text="Events", font=("TkDefaultFont", 14, "bold")).grid(
        row=0, column=0, columnspan=2, pady=5, padx=5)

    field_col = 0
    field_labels = (
        "eventID", "videoID", "astroStatusID", "readingID",
        "eventType", "confidence", "urgency", "timeStamp",
        "detectedBy", "whereOccured", "gpsLat", "gpsLong", "eventReport"
    )
    for field_label in field_labels:
        tk.Label(events_frame, text=f"{field_label}").grid(
            row=1, column=field_col, padx=10, pady=5)
        field_col += 1

    i = 2
    for data in event_data:
        tk.Label(events_frame, text=f"{data['eventID']}").grid(
            row=i, column=0, padx=10, pady=5)
        tk.Label(events_frame, text=f"{data['videoID']}").grid(
            row=i, column=1, padx=10, pady=5)
        tk.Label(events_frame, text=f"{data['astroStatusID']}").grid(
            row=i, column=2, padx=10, pady=5)
        tk.Label(events_frame, text=f"{data['readingID']}").grid(
            row=i, column=3, padx=10, pady=5)
        tk.Label(events_frame, text=f"{data['eventType']}").grid(
            row=i, column=4, padx=10, pady=5)
        tk.Label(events_frame, text=f"{data['confidence']}").grid(
            row=i, column=5, padx=10, pady=5)
        tk.Label(events_frame, text=f"{data['urgency']}").grid(
            row=i, column=6, padx=10, pady=5)
        tk.Label(events_frame, text=f"{data['timeStamp']}").grid(
            row=i, column=7, padx=10, pady=5)
        tk.Label(events_frame, text=f"{data['detectedBy']}").grid(
            row=i, column=8, padx=10, pady=5)
        tk.Label(events_frame, text=f"{data['whereOccured']}").grid(
            row=i, column=9, padx=10, pady=5)
        tk.Label(events_frame, text=f"{data['gpsLat']}").grid(
            row=i, column=10, padx=10, pady=5)
        tk.Label(events_frame, text=f"{data['gpsLong']}").grid(
            row=i, column=11, padx=10, pady=5)
        tk.Label(events_frame, text=f"{data['eventReport']}").grid(
            row=i, column=12, padx=10, pady=5)
        i += 1

def make_menu():
    """
    Adapted from an assignment in Python 2 (Coffee/donut shop)
    """
    video_menu = tk.Menu(menu_bar, tearoff=0)
    astro_status_menu = tk.Menu(menu_bar, tearoff=0)
    sensor_readings_menu = tk.Menu(menu_bar, tearoff=0)
    events_menu = tk.Menu(menu_bar, tearoff=0)

    menu_bar.add_cascade(label="Videos", menu=video_menu)
    menu_bar.add_cascade(label="Astro's Status", menu=astro_status_menu)
    menu_bar.add_cascade(label="Sensor Readings", menu=sensor_readings_menu)
    menu_bar.add_cascade(label="Events", menu=events_menu)


    video_menu.add_command(label="Show Videos", command=build_videos_gui)
    astro_status_menu.add_command(
        label="Show Astro's Status", command=build_astro_status_gui)
    sensor_readings_menu.add_command(
        label="Show Sensor Readings", command=build_sensor_readings_gui)
    events_menu.add_command(label="Show Events", command=build_events_gui)

make_menu()

build_videos_gui()

root.mainloop()
