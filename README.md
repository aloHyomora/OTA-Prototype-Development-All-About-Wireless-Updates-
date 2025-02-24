# 🚀 Wireless OTA Prototype: Raspberry Pi & Flask 기반 펌웨어 업데이트 시스템

## 📌 프로젝트 소개
이 프로젝트는 **Raspberry Pi**, **Flask 서버**, **MySQL**, **추가적인 하드웨어**를 활용하여 무선으로 펌웨어를 업데이트하는 **OTA(Over-The-Air) 시스템**을 구축하는 것을 목표로 합니다.

- **Flask 서버**: 펌웨어 파일을 관리하고 Raspberry Pi에서 요청 시 다운로드 가능하도록 구성
- **Raspberry Pi(CCU 역할)**: Flask 서버에서 최신 펌웨어를 다운로드하고 무결성을 검증한 후 업데이트 수행
- **MySQL 데이터베이스**: 펌웨어 버전 및 해시값 관리, 다운로드 기록 저장

## ⚙️ 시스템 아키텍처
```
+----------------------+          +----------------------+
|   Raspberry Pi (CCU) | <------> |   Flask OTA Server  |
| - 펌웨어 다운로드     |          | - 펌웨어 관리        |
| - 무결성 검증         |          | - MySQL 연동        |
| - 펌웨어 적용         |          | - API 제공          |
+----------------------+          +----------------------+
```

## 🚀 주요 기능
✅ **Flask 서버에서 펌웨어 업로드 및 관리**
✅ **MySQL을 이용한 펌웨어 정보 저장 및 버전 관리**
✅ **Raspberry Pi에서 최신 펌웨어 다운로드**
✅ **SHA-256을 이용한 무결성 검증**
✅ **펌웨어를 EEPROM/Flash 메모리에 적용하여 업데이트 수행**

## 🖥️ 실행 방법
### 1️⃣ Flask 서버 실행 (Laptop / PC)
```bash
# 서버 실행
python -m flask run --host=0.0.0.0
```

### 2️⃣ Raspberry Pi에서 최신 펌웨어 다운로드
```bash
python3 download_firmware.py
```

### 3️⃣ SHA-256 해시 검증 및 펌웨어 업데이트
```bash
sha256sum firmware_v1.1.0.bin
```

## 🔗 API 엔드포인트
| Method | Endpoint | 설명 |
|--------|------------|-------------------------------|
| **GET** | `/firmware/latest` | 최신 펌웨어 정보 조회 |
| **GET** | `/firmware/download/<version>` | 특정 버전 펌웨어 다운로드 |
| **POST** | `/firmware/sync_sha256` | SHA-256 해시 동기화 |

## 🎯 향후 개선 사항
🔹 Raspberry Pi에서 **자동 업데이트 스케줄링** 구현
🔹 OTA 적용 대상 확장 (ESP32, STM32 등 추가 지원)
🔹 펌웨어 롤백 기능 추가

---
🚀 **무선 업데이트 시스템을 구축하고 최적화하는 과정을 공유합니다!**

