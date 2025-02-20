from flask import Blueprint, jsonify, request
from models import Firmware

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    device_id = data.get("device_id")

    if not device_id:
        return jsonify({"error": "device_id is required"}), 400

    user = Firmware.query.filter_by(device_id=device_id).first()
    if user:
        return jsonify({"message": "Login successful", "user": {"id": user.id, "username": user.username}})
    return jsonify({"error": "Invalid device_id"}), 401
