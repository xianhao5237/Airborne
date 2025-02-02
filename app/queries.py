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

INSERT_SENSOR_RETURN_ID = """
INSERT INTO sensors (name, latitude, longitude) 
VALUES (%s, %s, %s) 
RETURNING id;
"""
INSERT_DATA = "INSERT INTO data (sensor_id, temperature, humidity, pm25, tvoc, co2, date) VALUES (%s, %s, %s, %s, %s, %s, %s);"

SENSOR_DETAILS_QUERY = "SELECT name, latitude, longitude FROM sensors WHERE id = %s;"







GLOBAL_NUMBER_OF_DAYS = "SELECT COUNT(DISTINCT DATE(date)) AS days FROM data;"
GLOBAL_AVG = "SELECT AVG(temperature) as average FROM data;"


SENSOR_NUMBER_OF_DAYS = "SELECT COUNT(DISTINCT DATE(date)) AS days FROM data WHERE sensor_id = (%s);"
SENSOR_ALL_TIME_AVG = "SELECT AVG(temperature) as average FROM data WHERE sensor_id = (%s);"
