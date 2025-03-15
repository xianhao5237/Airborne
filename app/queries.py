CREATE_SENSORS_TABLE = """
CREATE TABLE IF NOT EXISTS sensors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    latitude DOUBLE PRECISION DEFAULT NULL,
    longitude DOUBLE PRECISION DEFAULT NULL
);
"""
CREATE_DATA_TABLE = """
CREATE TABLE IF NOT EXISTS data (
    sensor_id UUID,
    temperature DOUBLE PRECISION DEFAULT NULL,
    humidity DOUBLE PRECISION DEFAULT NULL,
    pm25 DOUBLE PRECISION DEFAULT NULL,
    tvoc DOUBLE PRECISION DEFAULT NULL,
    co2 DOUBLE PRECISION DEFAULT NULL,
    date TIMESTAMP,
    FOREIGN KEY (sensor_id) REFERENCES sensors (id) ON DELETE CASCADE
);
"""
CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
"""
CREATE_USER_DATA_TABLE = """
CREATE TABLE IF NOT EXISTS user_data (
    user_id UUID,
    temperature DOUBLE PRECISION DEFAULT NULL,
    humidity DOUBLE PRECISION DEFAULT NULL,
    pm25 DOUBLE PRECISION DEFAULT NULL,
    tvoc DOUBLE PRECISION DEFAULT NULL,
    co2 DOUBLE PRECISION DEFAULT NULL,
    date TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
"""



INSERT_SENSOR_RETURN_ID = """
INSERT INTO sensors (name, latitude, longitude) 
VALUES (%s, %s, %s) 
RETURNING id;
"""
INSERT_DATA = "INSERT INTO data (sensor_id, temperature, humidity, pm25, tvoc, co2, date) VALUES (%s, %s, %s, %s, %s, %s, %s);"

INSERT_USER_RETURN_ID = """
INSERT INTO users (username, password) 
VALUES (%s, %s) 
RETURNING id;
"""

INSERT_USER_DATA = """
INSERT INTO user_data (user_id, temperature, humidity, pm25, tvoc, co2, date)
VALUES (%s, %s, %s, %s, %s, %s, %s);
"""



SENSOR_DETAILS_QUERY = "SELECT name, latitude, longitude FROM sensors WHERE id = %s;"

SENSOR_LAST_10_TEMP_AVG = """
SELECT AVG(temperature) as average 
FROM data 
WHERE sensor_id = %s AND date >= NOW() - INTERVAL '10 minutes';
"""
SENSOR_LAST_10_HUMIDITY_AVG = """
SELECT AVG(humidity) as average 
FROM data 
WHERE sensor_id = %s AND date >= NOW() - INTERVAL '10 minutes';
"""
# SENSOR_PM25_LAST_7_DAYS_AVG = """
# SELECT DATE(date) AS day, AVG(pm25) AS average_pm25
# FROM data
# WHERE sensor_id = %s 
#   AND date >= NOW() - INTERVAL '7 days'
# GROUP BY day
# ORDER BY day DESC;
# """

SENSOR_PM25_LAST_7_DAYS_AVG = """
WITH last_7_days AS (
    SELECT generate_series(
        (NOW() - INTERVAL '4 hours')::date - INTERVAL '6 days',  
        (NOW() - INTERVAL '4 hours')::date,                      
        '1 day'::interval
    )::date AS day
)
SELECT last_7_days.day, COALESCE(AVG(data.pm25), 0) AS average_pm25
FROM last_7_days
LEFT JOIN data ON DATE(data.date) = last_7_days.day AND data.sensor_id = %s
GROUP BY last_7_days.day
ORDER BY last_7_days.day DESC;
"""
USER_PM25_LAST_7_DAYS_AVG = """
WITH last_7_days AS (
    SELECT generate_series(
        (NOW() - INTERVAL '4 hours')::date - INTERVAL '6 days',  
        (NOW() - INTERVAL '4 hours')::date,                       
        '1 day'::interval
    )::date AS day
)
SELECT last_7_days.day, COALESCE(AVG(user_data.pm25), 0) AS average_pm25
FROM last_7_days
LEFT JOIN user_data ON DATE(user_data.date) = last_7_days.day AND user_data.user_id = %s
GROUP BY last_7_days.day
ORDER BY last_7_days.day DESC;
"""


SENSOR_TVOC_LAST_7_DAYS_AVG = """
WITH last_7_days AS (
    SELECT generate_series(
        (NOW() - INTERVAL '4 hours')::date - INTERVAL '6 days',  
        (NOW() - INTERVAL '4 hours')::date,                      
        '1 day'::interval
    )::date AS day
)
SELECT last_7_days.day, COALESCE(AVG(data.tvoc), 0) AS average_tvoc
FROM last_7_days
LEFT JOIN data ON DATE(data.date) = last_7_days.day AND data.sensor_id = %s
GROUP BY last_7_days.day
ORDER BY last_7_days.day DESC;
"""
USER_TVOC_LAST_7_DAYS_AVG = """
WITH last_7_days AS (
    SELECT generate_series(
        (NOW() - INTERVAL '4 hours')::date - INTERVAL '6 days',  
        (NOW() - INTERVAL '4 hours')::date,                       
        '1 day'::interval
    )::date AS day
)
SELECT last_7_days.day, COALESCE(AVG(user_data.tvoc), 0) AS average_tvoc
FROM last_7_days
LEFT JOIN user_data ON DATE(user_data.date) = last_7_days.day AND user_data.user_id = %s
GROUP BY last_7_days.day
ORDER BY last_7_days.day DESC;
"""

SENSOR_CO2_LAST_7_DAYS_AVG = """
WITH last_7_days AS (
    SELECT generate_series(
        (NOW() - INTERVAL '4 hours')::date - INTERVAL '6 days',  
        (NOW() - INTERVAL '4 hours')::date,                      
        '1 day'::interval
    )::date AS day
)
SELECT last_7_days.day, COALESCE(AVG(data.co2), 0) AS average_co2
FROM last_7_days
LEFT JOIN data ON DATE(data.date) = last_7_days.day AND data.sensor_id = %s
GROUP BY last_7_days.day
ORDER BY last_7_days.day DESC;
"""

USER_CO2_LAST_7_DAYS_AVG = """
WITH last_7_days AS (
    SELECT generate_series(
        (NOW() - INTERVAL '4 hours')::date - INTERVAL '6 days',  
        (NOW() - INTERVAL '4 hours')::date,                       
        '1 day'::interval
    )::date AS day
)
SELECT last_7_days.day, COALESCE(AVG(user_data.co2), 0) AS average_co2
FROM last_7_days
LEFT JOIN user_data ON DATE(user_data.date) = last_7_days.day AND user_data.user_id = %s
GROUP BY last_7_days.day
ORDER BY last_7_days.day DESC;
"""



PM25_HOURLY_AVG = """
WITH hours AS (
    SELECT generate_series(
        DATE_TRUNC('day', NOW() - INTERVAL '4 hours'),
        DATE_TRUNC('hour', NOW() - INTERVAL '4 hours'),
        INTERVAL '1 hour'
    ) AS hour
)
SELECT hours.hour, COALESCE(AVG(d.pm25), 0) AS avg_pm25
FROM hours
LEFT JOIN data d ON DATE_TRUNC('hour', d.date) = hours.hour
AND d.sensor_id = %s
GROUP BY hours.hour
ORDER BY hours.hour;
"""

USER_PM25_HOURLY_AVG = """
WITH hours AS (
    SELECT generate_series(
        DATE_TRUNC('day', NOW() - INTERVAL '4 hours'),
        DATE_TRUNC('hour', NOW() - INTERVAL '4 hours'),
        INTERVAL '1 hour'
    ) AS hour
)
SELECT hours.hour, COALESCE(AVG(ud.pm25), 0) AS avg_pm25
FROM hours
LEFT JOIN user_data ud ON DATE_TRUNC('hour', ud.date) = hours.hour
AND ud.user_id = %s
GROUP BY hours.hour
ORDER BY hours.hour;
"""


TVOC_HOURLY_AVG = """
WITH hours AS (
    SELECT generate_series(
        DATE_TRUNC('day', NOW() - INTERVAL '4 hours'),
        DATE_TRUNC('hour', NOW() - INTERVAL '4 hours'),
        INTERVAL '1 hour'
    ) AS hour
)
SELECT hours.hour, COALESCE(AVG(d.tvoc), 0) AS avg_tvoc
FROM hours
LEFT JOIN data d ON DATE_TRUNC('hour', d.date) = hours.hour
AND d.sensor_id = %s
GROUP BY hours.hour
ORDER BY hours.hour;
"""

USER_TVOC_HOURLY_AVG = """
WITH hours AS (
    SELECT generate_series(
        DATE_TRUNC('day', NOW() - INTERVAL '4 hours'),
        DATE_TRUNC('hour', NOW() - INTERVAL '4 hours'),
        INTERVAL '1 hour'
    ) AS hour
)
SELECT hours.hour, COALESCE(AVG(ud.tvoc), 0) AS avg_tvoc
FROM hours
LEFT JOIN user_data ud ON DATE_TRUNC('hour', ud.date) = hours.hour
AND ud.user_id = %s
GROUP BY hours.hour
ORDER BY hours.hour;
"""


CO2_HOURLY_AVG = """
WITH hours AS (
    SELECT generate_series(
        DATE_TRUNC('day', NOW() - INTERVAL '4 hours'),
        DATE_TRUNC('hour', NOW() - INTERVAL '4 hours'),
        INTERVAL '1 hour'
    ) AS hour
)
SELECT hours.hour, COALESCE(AVG(d.co2), 0) AS avg_co2
FROM hours
LEFT JOIN data d ON DATE_TRUNC('hour', d.date) = hours.hour
AND d.sensor_id = %s
GROUP BY hours.hour
ORDER BY hours.hour;
"""

USER_CO2_HOURLY_AVG = """
WITH hours AS (
    SELECT generate_series(
        DATE_TRUNC('day', NOW() - INTERVAL '4 hours'),
        DATE_TRUNC('hour', NOW() - INTERVAL '4 hours'),
        INTERVAL '1 hour'
    ) AS hour
)
SELECT hours.hour, COALESCE(AVG(ud.co2), 0) AS avg_co2
FROM hours
LEFT JOIN user_data ud ON DATE_TRUNC('hour', ud.date) = hours.hour
AND ud.user_id = %s
GROUP BY hours.hour
ORDER BY hours.hour;
"""




SENSOR_LATEST_READING = """
SELECT temperature, humidity, pm25, tvoc, co2, date
FROM data
WHERE sensor_id = %s
ORDER BY date DESC
LIMIT 1;
"""



# GLOBAL_NUMBER_OF_DAYS = "SELECT COUNT(DISTINCT DATE(date)) AS days FROM data;"
# GLOBAL_AVG = "SELECT AVG(temperature) as average FROM data;"


# SENSOR_NUMBER_OF_DAYS = "SELECT COUNT(DISTINCT DATE(date)) AS days FROM data WHERE sensor_id = (%s);"
# SENSOR_ALL_TIME_AVG = "SELECT AVG(temperature) as average FROM data WHERE sensor_id = (%s);"



