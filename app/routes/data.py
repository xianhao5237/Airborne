from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
from app.database import get_connection
from app.queries import CREATE_DATA_TABLE, INSERT_DATA, GLOBAL_AVG, GLOBAL_NUMBER_OF_DAYS

data_bp = Blueprint('data', __name__)

@data_bp.route("/", methods=["POST"])
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
        date = datetime.now(timezone.utc)
    except ValueError:
        return {"error": "Invalid 'date' format. Use '%m-%d-%Y %H:%M:%S'"}, 400

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(CREATE_DATA_TABLE)  
            cursor.execute(INSERT_DATA, (sensor_id, temperature, humidity, pm25, tvoc, co2, date))

    return {"message": "Data added successfully."}, 201





#fix and add more below
@data_bp.route("/average", methods=["GET"])
def get_global_average():
    """
    Fetches the global average temperature and the number of unique days with data.
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(GLOBAL_AVG)
            average = cursor.fetchone()["average"]
            cursor.execute(GLOBAL_NUMBER_OF_DAYS)
            days = cursor.fetchone()["days"]

    if average is None:
        return jsonify({"error": "No data available."}), 404

    return jsonify({"average": round(average, 2), "days": days})
