from flask import Blueprint, request
from app.database import get_connection
from app.queries import CREATE_SENSORS_TABLE, INSERT_SENSOR_RETURN_ID, SENSOR_DETAILS_QUERY

sensors_bp = Blueprint('sensors', __name__)

@sensors_bp.route("/", methods=["POST"])
def create_sensor():
    data = request.get_json()
    name = data["name"]
    latitude = data.get("latitude") 
    longitude = data.get("longitude") 

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(CREATE_SENSORS_TABLE)
            cursor.execute(INSERT_SENSOR_RETURN_ID, (name, latitude, longitude))
            sensor_id = cursor.fetchone()["id"]
    return {"id": sensor_id, "message": f"Sensor {name} created."}, 201


@sensors_bp.route("/<uuid:sensor_id>", methods=["GET"])
def get_sensor_details(sensor_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(SENSOR_DETAILS_QUERY, (str(sensor_id),))
            result = cursor.fetchone()

    if not result:
        return {"error": f"Sensor with ID '{sensor_id}' not found."}, 404

    return {
        "id": str(sensor_id),
        "name": result["name"],
        "latitude": result["latitude"],
        "longitude": result["longitude"]
    }, 200


@sensors_bp.route("/<uuid:sensor_id>", methods=["DELETE"])
def delete_sensor(sensor_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM sensors WHERE id = %s;", (str(sensor_id),))
            result = cursor.fetchone()

            if not result:
                return {"error": f"Sensor with ID '{sensor_id}' not found."}, 404

            cursor.execute("DELETE FROM sensors WHERE id = %s;", (str(sensor_id),))

    return {
        "message": f"Sensor with ID '{sensor_id}' and its associated data were deleted."
    }, 200
