
import sqlite3 as sql

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


def main():
    db_conn = None
    try:
        db_conn = sql.connect('astro_db.db')
        cursor = db_conn.cursor()

        if isinstance(fake_videos_data, (list, tuple)) and fake_videos_data:
            cursor.executemany("""INSERT INTO videos(videoID, filePath, fileName, videoDuration, timeStamp,
            whichCamera, resolution, gpsLat, gpsLong, location) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", fake_videos_data)

        if isinstance(fake_astro_status_data, (list, tuple)) and fake_astro_status_data:
            cursor.executemany("""INSERT INTO astroStatus(astroStatusID, batteryLife, locationInSchool, gpsStatus, gpsLat, gpsLong,
            camFrontStatus, camRearStatus, currentTask, timeStamp, errorLog) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", fake_astro_status_data)

        if isinstance(fake_sensor_readings_data, (list, tuple)) and fake_sensor_readings_data:
            cursor.executemany("""INSERT INTO sensorReadings(readingID, gasReading, tempHumiReading, usReading, severity,
            timeStamp, gpsLat, gpsLong) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", fake_sensor_readings_data)

        # Checks if the data is a list OR a tuple AND that it has data.
        if isinstance(fake_events_data, (list, tuple)) and fake_events_data:
            cursor.executemany("""INSERT INTO events(eventID, videoID, astroStatusID, readingID, eventType,
            confidence, urgency, timeStamp, detectedBy, whereOccured,
            gpsLat, gpsLong, eventReport) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", fake_events_data)

        db_conn.commit()  # comment out for tests without pushing data in

    except sql.Error as e:
        print(f"Sqlite error occurred: {e}")
        db_conn.rollback()

    except Exception as e:
        print(f"An error occurred: {e}")
        db_conn.rollback()

    finally:
        if db_conn is not None:
            db_conn.close
