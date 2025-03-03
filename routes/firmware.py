from flask import Blueprint, jsonify, request, send_file, abort, current_app
from database import db
from models import Firmware
import os

firmware_bp = Blueprint('firmware', __name__)
FIRMWARE_BASE_DIR = os.path.join(os.getcwd(), "hardware")

# 바이너리 펌웨어 (.bin) 파일과 함께 HTTP 200 상태 코드 및 헤더 반환
@firmware_bp.route('/download/<version>', methods=['GET'])
def download_firmware(version):
    # DB에서 해당 버전의 펌웨어 정보 찾기
    firmware = Firmware.query.filter_by(version=version, status='active').first()
    if not firmware:
        return jsonify({"error": f"Firmware version {version} not found"}), 404

    # Flask 실행 디렉토리 기준으로 절대 경로 변환
    base_dir = os.getcwd()
    absolute_path = '/' + firmware.file_path.lstrip('/') # os.path.abspath(os.path.join(base_dir, firmware.file_path.lstrip('/')))
    # 파일 존재 여부 확인
    if not os.path.exists(absolute_path):
        print("Non file")
        return jsonify({"error": "Firmware file not found on server"}), 404
    
    # 원래 파일명 유지하여 전송
    filename = os.path.basename(absolute_path)  # 파일명만 추출
    print(filename)

    # Content-Disposition 헤더 명시적으로 설정
    headers = {
        "Content-Disposition": f"attachment; filename={filename}",
        "Content-Type": "application/octet-stream"
    }
    return send_file(absolute_path, as_attachment=True, download_name=filename, mimetype="application/octet-stream"), 200, headers

# 존재하는 데이터 확인 라우터
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
    # 활성화된 버전 중 가장 높은 버전 하나를 가져옴.
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

# 새로운 펌웨어 추가 함수
def add_firmware_entry(version, file_path, sha256, status):
    existing_firmware = Firmware.query.filter_by(version=version).first()
    if existing_firmware:
        print(f"이미 존재하는 버전: {version}, 추가하지 않음.")
        return

    file_size = os.path.getsize(file_path)
    
    # 새 펌웨어 데이터 생성 및 DB 추가
    new_firmware = Firmware(
        version=version,
        file_path=file_path,
        sha256=sha256,
        device_type="default",  # 필요 시 변경 가능
        size=file_size,
        status=status
    )
    db.session.add(new_firmware)
    db.session.commit()
    print(f"새 펌웨어 추가 완료: {version}")

# 펌웨어 파일을 탐색하는 함수
def find_firmware_files(base_dir):
    firmware_files = {}

    # 하위 폴더 순회하며 파일 찾기
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".ino.bin"):
                version = os.path.basename(os.path.dirname(os.path.dirname(root))) # 폴더명(버전) 가져오기
                firmware_files[version] = os.path.join(root, file)
                print(f"map에 {version} 추가, 파일 {file}, path: {firmware_files[version]}")

    return firmware_files

# 펌웨어(hardware) 폴더 네 파일 DB와 동기화
def sync_firmware_directory():
    firmware_dir = os.path.join(os.getcwd(), "hardware")
    os.makedirs(firmware_dir, exist_ok=True)  # 폴더가 없으면 생성

    # 현재 존재하는 펌웨어 파일 검색
    print("\n존재하는 펌웨어 파일 확인 중...")
    firmware_map = find_firmware_files(FIRMWARE_BASE_DIR)
    
    existing_firmware_versions = {fw.version for fw in Firmware.query.all()}  # 기존 DB 버전 가져오기

    for version, path in firmware_map.items():
        print(f"버전: {version} -> {path}")
        version_num = (version.replace(".ino.bin", "").split("V")[-1]).replace("_",".")

        # 이미 존재하는 버전이면 스킵
        if version_num in existing_firmware_versions:
            continue

        sha256_hash = calculate_sha256(path)
        
        # 키보드 입력으로 status 설정
        while True:
            status = input(f"펌웨어 {version}의 상태를 입력하세요 (active/deprecated): ").strip().lower()
            if status in ["active", "deprecated"]:
                break
            print("잘못된 입력! 'active' 또는 'deprecated'만 입력 가능")

        add_firmware_entry(version_num, path, sha256_hash, status)
        print(f"버전: {version_num} -> {path} 동기화 확인.")
    print("펌웨어 동기화 완료!")

import hashlib

# SHA-256 해시값 계산 함수
def calculate_sha256(file_path):
    """주어진 파일의 SHA-256 해시값을 계산"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# SHA-256 해시값을 동기화하는 함수
def sync_sha256():
    """Flask 애플리케이션 컨텍스트 내에서 SHA-256 해시값을 데이터베이스와 동기화"""
    with current_app.app_context():  # Flask 컨텍스트 활성화
        updated_files = []
        firmwares = Firmware.query.all()  # 애플리케이션 컨텍스트 내에서 실행

        for firmware in firmwares:
            absolute_path = '/' + firmware.file_path.lstrip('/') # os.path.join() # os.path.abspath()

            if os.path.exists(absolute_path):
                sha256_hash = calculate_sha256(absolute_path)
                firmware.sha256 = sha256_hash  # DB 업데이트
                db.session.commit()
                updated_files.append({"version": firmware.version, "sha256": sha256_hash})
            else:
                print(f"파일이 존재하지 않음: {absolute_path}")

        print("SHA-256 동기화 완료:", updated_files)

@firmware_bp.route('/sync_sha256', methods=['POST'])
def sync_sha256_api():
    """API를 통해 SHA-256 해시값 동기화 실행"""
    sync_sha256()
    return jsonify({"message": "SHA-256 sync completed"})