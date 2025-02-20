from flask import Blueprint, jsonify, request
from database import db
from models import Firmware

firmware_bp = Blueprint('firmware', __name__)

@firmware_bp.route('/all', methods=['GET'])
def get_all_firmwares():
    firmwares = Firmware.query.all()
    return jsonify([
        {
            "id": fw.id,
            "version": fw.version,
            "file_path": fw.file_path,
            "sha256": fw.sha256,
            "uploaded_at": fw.uploaded_at,
            "device_type": fw.device_type,
            "size": fw.size,
            "status": fw.status,
            "notes": fw.notes
        } for fw in firmwares
    ])

@firmware_bp.route('/latest', methods=['GET'])
def get_latest_firmware():
    firmware = Firmware.query.filter_by(status='active').order_by(Firmware.version.desc()).first()
    if firmware:
        return jsonify({
            "version": firmware.version,
            "file_path": firmware.file_path,
            "sha256": firmware.sha256,
            "device_type": firmware.device_type,
            "size": firmware.size
        })
    return jsonify({"error": "No active firmware found"}), 404

@firmware_bp.route('/add', methods=['POST'])
def add_firmware():
    data = request.json
    new_firmware = Firmware(
        version=data['version'],
        file_path=data['file_path'],
        sha256=data['sha256'],
        device_type=data['device_type'],
        size=data['size'],
        status=data.get('status', 'active'),
        notes=data.get('notes', '')
    )
    db.session.add(new_firmware)
    db.session.commit()
    return jsonify({"message": "Firmware added successfully!"})
