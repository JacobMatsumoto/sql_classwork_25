/* 
I'm making a database using different DATETIME functions (date(), time() and datetime(),strftime(), julianday(), and unixepoch()) I'm going to use each one somehow to make a sort of daily tracker, I'll use datetime to get the current datetime date and time on their own to get the date and time respectively. I'll utilize strftime with the %x's to pull exactly what i want (day of week, only the year and only the month). Then I can use juliantime to check the days that have passed since one log day to another. As well as using unixepoch to get an entry dates unix time, it's still really unclear to me exactly what that is/does though.



https://www.sqlite.org/lang_datefunc.html
%d		day of month: 01-31
%e		day of month without leading zero: 1-31
%f		fractional seconds: SS.SSS
%F		ISO 8601 date: YYYY-MM-DD
%G		ISO 8601 year corresponding to %V
%g		2-digit ISO 8601 year corresponding to %V
%H		hour: 00-24
%I		hour for 12-hour clock: 01-12
%j		day of year: 001-366
%J		Julian day number (fractional)
%k		hour without leading zero: 0-24
%l		%I without leading zero: 1-12
%m		month: 01-12
%M		minute: 00-59
%p		"AM" or "PM" depending on the hour
%P		"am" or "pm" depending on the hour
%R		ISO 8601 time: HH:MM
%s		seconds since 1970-01-01
%S		seconds: 00-59
%T		ISO 8601 time: HH:MM:SS
%U		week of year (00-53) - week 01 starts on the first Sunday
%u		day of week 1-7 with Monday==1
%V		ISO 8601 week of year
%w		day of week 0-6 with Sunday==0
%W		week of year (00-53) - week 01 starts on the first Monday
%Y		year: 0000-9999
%%		%
 */
CREATE TABLE
    logbook (
        id INTEGER PRIMARY KEY,
        my_entry TEXT,
        created_at TEXT,
        time_num TEXT,
        year_num TEXT,
        month_num TEXT,
        day_num TEXT,
        day_of_week TEXT
    );

INSERT INTO -- making entries 
    logbook (
        my_entry,
        created_at,
        time_num,
        year_num,
        month_num,
        day_num,
        day_of_week
    )
VALUES
    (
        'Today I did homework and hung out with my SO',
        DATETIME ('now', 'localtime'), --created at
        time('now', 'localtime'), -- Time
        strftime ('%Y', 'now', 'localtime'), -- year
        strftime ('%m', 'now', 'localtime'), -- month
        date ('now', 'localtime'), -- day
        strftime ('%w', 'now', 'localtime') -- day of week
    );

INSERT INTO -- -1 day
    logbook (
        my_entry,
        created_at,
        time_num,
        year_num,
        month_num,
        day_num,
        day_of_week
    )
VALUES
    (
        'Today I went to work and worked on my UIUX project',
        DATETIME ('now', '-1 day', 'localtime'), --created at
        time('now', '-1 day', 'localtime'), -- Time
        strftime ('%Y', 'now', '-1 day', 'localtime'), -- year
        strftime ('%m', 'now', '-1 day', 'localtime'), -- month
        date ('now', '-1 day', 'localtime'), -- day
        strftime ('%w', 'now', '-1 day', 'localtime') -- day of week
    );

INSERT INTO -- -3 days
    logbook (
        my_entry,
        created_at,
        time_num,
        year_num,
        month_num,
        day_num,
        day_of_week
    )
VALUES
    (
        'Today I walked around the neighborhood and did english homework',
        DATETIME ('now', '-3 days', 'localtime'), --created at
        time('now', '-3 day', 'localtime'), -- Time
        strftime ('%Y', 'now', '-3 days', 'localtime'), -- year
        strftime ('%m', 'now', '-3 days', 'localtime'), -- month
        date ('now', '-3 days', 'localtime'), -- day
        strftime ('%w', 'now', '-3 days', 'localtime') -- day of week
    );
SELECT * FROM logbook;
--using julianday to see how many days have passed between entries
SELECT
    julianday (a.created_at) - julianday (b.created_at) AS days_since
FROM
    logbook a
    JOIN logbook b
WHERE
    a.id = 1
    AND b.id = 2;

--using unixepoch
SELECT --shows unix time 
    unixepoch (created_at) AS unix_time
FROM
    logbook
WHERE
    id = 1;

DROP TABLE IF EXISTS logbook;