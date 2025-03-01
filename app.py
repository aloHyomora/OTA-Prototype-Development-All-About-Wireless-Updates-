# Flask를 이용하여 MySQL DB(ota_db)와 연동
# OTA 서버에서 최신 펌웨어 정보를 제공하는 API 구현
# CCU(라즈베리파이)가 Flask 서버로부터 펌웨어를 다운로드할 수 있도록 구성

# 필요한 모듈들을 임포트합니다.
from flask import Flask                     # Flask 애플리케이션
from config import Config                   # DB 세팅
from database import db                     # DB 인스턴스
from routes.firmware import firmware_bp     # 펌웨어 관련 라우트
from routes.auth import auth_bp             # 인증 관련 라우트
from routes.firmware import firmware_bp, sync_sha256, sync_firmware_directory # sync_sha256 가져오기, 서버 시작시 SHA-256 자동 동기화

app = Flask(__name__)
app.config.from_object(Config)

# 데이터베이스 초기화
db.init_app(app)

app.register_blueprint(firmware_bp, url_prefix='/firmware')
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == "__main__":
    with app.app_context():
        print("Flask 애플리케이션 컨텍스트 활성화")  # 실행 확인 로그
        db.create_all()  # DB 테이블 생성
        print("데이터베이스 테이블 생성 완료")  # 실행 확인 로그
        sync_sha256()  # SHA-256 동기화 실행
        print("서버 시작 전 SHA-256 동기화 실행 완료")  # 실행 확인 로그
        sync_firmware_directory()  # 펌웨어 파일 DB 업데이트
        print("서버 시작 전 SHA-256 동기화 및 펌웨어 추가 완료\n")

    app.run(host="0.0.0.0", port=5000)