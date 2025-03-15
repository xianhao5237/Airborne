from flask import Blueprint, request, jsonify
from app.database import get_connection
from app.queries import CREATE_DATA_TABLE, INSERT_DATA, SENSOR_LAST_10_TEMP_AVG, SENSOR_LAST_10_HUMIDITY_AVG, SENSOR_LATEST_READING
from app.queries import SENSOR_PM25_LAST_7_DAYS_AVG, SENSOR_TVOC_LAST_7_DAYS_AVG, SENSOR_CO2_LAST_7_DAYS_AVG
from app.queries import PM25_HOURLY_AVG, TVOC_HOURLY_AVG, CO2_HOURLY_AVG
from app.queries import CREATE_USER_DATA_TABLE, INSERT_USER_DATA
from datetime import datetime, timezone, timedelta
import pytz

data_bp = Blueprint('data', __name__)

@data_bp.route("/api/data", methods=["POST"])
def add_data():
    data = request.get_json()

    sensor_id = data.get("sensor")
    if not sensor_id:
        return {"error": "Missing 'sensor' in payload"}, 400

    temperature = data.get("temperature")
    humidity = data.get("humidity")
    pm25 = data.get("pm25")
    tvoc = data.get("tvoc")
    co2 = data.get("co2")

    try:
        date = datetime.strptime(data["date"], "%m-%d-%Y %H:%M:%S")
    except KeyError:
        date = datetime.now(timezone.utc) - timedelta(hours=4)

        # utc_now = datetime.now(timezone.utc)
        # est_tz = pytz.timezone('America/New_York')
        # date = utc_now.astimezone(est_tz)

    except ValueError:
        return {"error": "Invalid 'date' format. Use '%m-%d-%Y %H:%M:%S'"}, 400

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(CREATE_DATA_TABLE)  
            cursor.execute(INSERT_DATA, (sensor_id, temperature, humidity, pm25, tvoc, co2, date))

    return {"message": "Data added successfully."}, 201

@data_bp.route("/api/data/temp/avg/<uuid:sensor_id>", methods=["GET"])
def get_sensor_avg_last_10_min(sensor_id):
    """
    Get the average temperature for a specific sensor in the last 10 minutes.
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(SENSOR_LAST_10_TEMP_AVG, (str(sensor_id),))
            result = cursor.fetchone()

    if not result or result["average"] is None:
        return jsonify({"error": f"No temperature data available for sensor {sensor_id} in the last 10 minutes."}), 404

    return jsonify({
        "sensor_id": str(sensor_id),
        "average_temperature": round(result["average"], 2),
        "time_range": "10 minutes"
    }), 200

@data_bp.route("/api/data/humidity/avg/<uuid:sensor_id>", methods=["GET"])
def get_sensor_humidity_avg_last_10_min(sensor_id):
    """
    Get the average humidity for a specific sensor in the last 10 minutes.
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(SENSOR_LAST_10_HUMIDITY_AVG, (str(sensor_id),))
            result = cursor.fetchone()

    if not result or result["average"] is None:
        return jsonify({"error": f"No humidity data available for sensor {sensor_id} in the last 10 minutes."}), 404

    return jsonify({
        "sensor_id": str(sensor_id),
        "average_humidity": round(result["average"], 2),
        "time_range": "Last 10 minutes"
    }), 200

@data_bp.route("/api/data/latest/<uuid:sensor_id>/<uuid:user_id>", methods=["GET"])
def get_sensor_latest_reading(sensor_id, user_id):
    """
    Get the latest reading for each metric (temperature, humidity, PM2.5, TVOC, CO2) for a specific sensor.
    Insert the latest data into the user_data table.
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            # Fetch the latest reading from sensor data
            cursor.execute(SENSOR_LATEST_READING, (str(sensor_id),))
            result = cursor.fetchone()

            if not result:
                return jsonify({"error": f"No data available for sensor {sensor_id}."}), 404

            # Prepare latest data
            latest_data = {
                "temperature": result["temperature"],
                "humidity": result["humidity"],
                "pm25": result["pm25"],
                "tvoc": result["tvoc"],
                "co2": result["co2"],
                "timestamp": result["date"]
            }

            cursor.execute(CREATE_USER_DATA_TABLE)
            cursor.execute(INSERT_USER_DATA, (
                str(user_id), result["temperature"], result["humidity"], result["pm25"], result["tvoc"], result["co2"], result["date"]))

    return jsonify({
        "sensor_id": str(sensor_id),
        "user_id": str(user_id),
        "latest_reading": latest_data,
        "message": "Latest reading retrieved and inserted into user_data."
    }), 200







# 7 day averages
@data_bp.route("/api/data/pm25/avg/<uuid:sensor_id>", methods=["GET"])
def get_sensor_pm25_avg_last_7_days(sensor_id):
    """
    Get the average PM2.5 levels per day for a specific sensor over the last 7 days.
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(SENSOR_PM25_LAST_7_DAYS_AVG, (str(sensor_id),))
            results = cursor.fetchall()

    if not results:
        return jsonify({"error": f"No PM2.5 data available for sensor {sensor_id} in the last 7 days."}), 404

    pm25_data = [{"date": str(row["day"]), "average_pm25": round(row["average_pm25"], 2)} for row in results]

    return jsonify({
        "sensor_id": str(sensor_id),
        "pm25_daily_averages": pm25_data,
        "time_range": "Last 7 days"
    }), 200

@data_bp.route("/api/data/tvoc/avg/<uuid:sensor_id>", methods=["GET"])
def get_sensor_tvoc_avg_last_7_days(sensor_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(SENSOR_TVOC_LAST_7_DAYS_AVG, (str(sensor_id),))
            results = cursor.fetchall()

    tvoc_data = [{"date": str(row["day"]), "average_tvoc": round(row["average_tvoc"], 2)} for row in results]

    return jsonify({
        "sensor_id": str(sensor_id),
        "tvoc_daily_averages": tvoc_data,
        "time_range": "Last 7 days"
    }), 200

@data_bp.route("/api/data/co2/avg/<uuid:sensor_id>", methods=["GET"])
def get_sensor_co2_avg_last_7_days(sensor_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(SENSOR_CO2_LAST_7_DAYS_AVG, (str(sensor_id),))
            results = cursor.fetchall()

    co2_data = [{"date": str(row["day"]), "average_co2": round(row["average_co2"], 2)} for row in results]

    return jsonify({
        "sensor_id": str(sensor_id),
        "co2_daily_averages": co2_data,
        "time_range": "Last 7 days"
    }), 200

# Hourly averages
@data_bp.route("/api/data/pm25/hourly/<uuid:sensor_id>", methods=["GET"])
def get_hourly_pm25_avg_sensor(sensor_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(PM25_HOURLY_AVG, (str(sensor_id),))
            results = cursor.fetchall()

    # Format response
    hourly_data = [{"hour": str(row["hour"]), "avg_pm25": round(row["avg_pm25"], 2)} for row in results]

    return jsonify({
        "sensor_id": str(sensor_id),
        "time_zone": "Eastern Time (EST/EDT)",
        "pm25_hourly_averages": hourly_data
    }), 200

@data_bp.route("/api/data/tvoc/hourly/<uuid:sensor_id>", methods=["GET"])
def get_hourly_tvoc_avg_sensor(sensor_id):

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(TVOC_HOURLY_AVG, (str(sensor_id),))
            results = cursor.fetchall()

    # Format response
    hourly_data = [{"hour": str(row["hour"]), "avg_tvoc": round(row["avg_tvoc"], 2)} for row in results]

    return jsonify({
        "sensor_id": str(sensor_id),
        "time_zone": "Eastern Time (EST/EDT)",
        "tvoc_hourly_averages": hourly_data
    }), 200

@data_bp.route("/api/data/co2/hourly/<uuid:sensor_id>", methods=["GET"])
def get_hourly_co2_avg_sensor(sensor_id):

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(CO2_HOURLY_AVG, (str(sensor_id),))
            results = cursor.fetchall()

    # Format response
    hourly_data = [{"hour": str(row["hour"]), "avg_co2": round(row["avg_co2"], 2)} for row in results]

    return jsonify({
        "sensor_id": str(sensor_id),
        "time_zone": "Eastern Time (EST/EDT)",
        "co2_hourly_averages": hourly_data
    }), 200
