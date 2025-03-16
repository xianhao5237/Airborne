from flask import Blueprint, request, jsonify
from app.database import get_connection
from app.queries import USER_PM25_LAST_7_DAYS_AVG, USER_TVOC_LAST_7_DAYS_AVG, USER_CO2_LAST_7_DAYS_AVG
from app.queries import USER_PM25_HOURLY_AVG, USER_TVOC_HOURLY_AVG, USER_CO2_HOURLY_AVG

user_data_bp = Blueprint('user_data', __name__)

@user_data_bp.route("/api/data/pm25/avg/user/<uuid:user_id>", methods=["GET"])
def get_user_pm25_avg_last_7_days(user_id):
    """
    Get the average PM2.5 levels per day for a specific user over the last 7 days.
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(USER_PM25_LAST_7_DAYS_AVG, (str(user_id),))
            results = cursor.fetchall()

    if not results:
        return jsonify({"error": f"No PM2.5 data available for user {user_id} in the last 7 days."}), 404

    pm25_data = [{"date": str(row["day"]), "average_pm25": round(row["average_pm25"], 2)} for row in results]

    return jsonify({
        "user_id": str(user_id),
        "pm25_daily_averages": pm25_data,
        "time_range": "Last 7 days"
    }), 200


@user_data_bp.route("/api/data/tvoc/avg/user/<uuid:user_id>", methods=["GET"])
def get_user_tvoc_avg_last_7_days(user_id):
    """
    Get the average TVOC levels per day for a specific user over the last 7 days.
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(USER_TVOC_LAST_7_DAYS_AVG, (str(user_id),))
            results = cursor.fetchall()

    if not results:
        return jsonify({"error": f"No TVOC data available for user {user_id} in the last 7 days."}), 404

    tvoc_data = [{"date": str(row["day"]), "average_tvoc": round(row["average_tvoc"], 2)} for row in results]

    return jsonify({
        "user_id": str(user_id),
        "tvoc_daily_averages": tvoc_data,
        "time_range": "Last 7 days"
    }), 200


@user_data_bp.route("/api/data/co2/avg/user/<uuid:user_id>", methods=["GET"])
def get_user_co2_avg_last_7_days(user_id):
    """
    Get the average CO2 levels per day for a specific user over the last 7 days.
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(USER_CO2_LAST_7_DAYS_AVG, (str(user_id),))
            results = cursor.fetchall()

    if not results:
        return jsonify({"error": f"No CO2 data available for user {user_id} in the last 7 days."}), 404

    co2_data = [{"date": str(row["day"]), "average_co2": round(row["average_co2"], 2)} for row in results]

    return jsonify({
        "user_id": str(user_id),
        "co2_daily_averages": co2_data,
        "time_range": "Last 7 days"
    }), 200


@user_data_bp.route("/api/data/pm25/hourly/user/<uuid:user_id>", methods=["GET"])
def get_hourly_pm25_avg_user(user_id):
    """
    Get the average PM2.5 per hour for a specific user.
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(USER_PM25_HOURLY_AVG, (str(user_id),))
            results = cursor.fetchall()

    if not results:
        return jsonify({"error": f"No PM2.5 data available for user {user_id}."}), 404

    hourly_data = [{"hour": str(row["hour"]), "avg_pm25": round(row["avg_pm25"], 2)} for row in results]

    return jsonify({
        "user_id": str(user_id),
        "time_zone": "Eastern Time (EST/EDT)",
        "pm25_hourly_averages": hourly_data
    }), 200


@user_data_bp.route("/api/data/tvoc/hourly/user/<uuid:user_id>", methods=["GET"])
def get_hourly_tvoc_avg_user(user_id):
    """
    Get the average TVOC per hour for a specific user.
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(USER_TVOC_HOURLY_AVG, (str(user_id),))
            results = cursor.fetchall()

    if not results:
        return jsonify({"error": f"No TVOC data available for user {user_id}."}), 404

    hourly_data = [{"hour": str(row["hour"]), "avg_tvoc": round(row["avg_tvoc"], 2)} for row in results]

    return jsonify({
        "user_id": str(user_id),
        "time_zone": "Eastern Time (EST/EDT)",
        "tvoc_hourly_averages": hourly_data
    }), 200


@user_data_bp.route("/api/data/co2/hourly/user/<uuid:user_id>", methods=["GET"])
def get_hourly_co2_avg_user(user_id):
    """
    Get the average CO2 per hour for a specific user.
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(USER_CO2_HOURLY_AVG, (str(user_id),))
            results = cursor.fetchall()

    if not results:
        return jsonify({"error": f"No CO2 data available for user {user_id}."}), 404

    hourly_data = [{"hour": str(row["hour"]), "avg_co2": round(row["avg_co2"], 2)} for row in results]

    return jsonify({
        "user_id": str(user_id),
        "time_zone": "Eastern Time (EST/EDT)",
        "co2_hourly_averages": hourly_data
    }), 200
