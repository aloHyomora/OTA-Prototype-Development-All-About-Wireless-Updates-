# 데이터베이스 모델을 정의합니다. Firmware 테이블 구조 반영
from database import db

class Firmware(db.Model):
    __tablename__ = 'firmware'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    version = db.Column(db.String(10), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    sha256 = db.Column(db.String(64), nullable=False)
    uploaded_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    device_type = db.Column(db.String(20), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum('active', 'deprecated'), nullable=False, default='active')
    notes = db.Column(db.Text)

    def __repr__(self):
        return f'<Firmware {self.version} ({self.device_type})>'
