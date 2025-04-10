### 🚀 **OTA Firmware Update System for Embedded Devices**  

## 📌 **Project Overview**  
This project aims to **build an OTA (Over-the-Air) firmware update system using ESP32 and Raspberry Pi**.  
The **Flask-based OTA server** distributes firmware updates, and the **Raspberry Pi (CCU)** downloads and applies them to the **ESP32 (DCU)**.  

이 프로젝트는 **Raspberry Pi**, **Flask 서버**, **MySQL**, **추가적인 하드웨어**를 활용하여 무선으로 펌웨어를 업데이트하는 **OTA(Over-The-Air) 시스템**을 구축하는 것을 목표로 합니다.

첨부된 링크 속 영상을 바탕으로 프로젝트를 설계했습니다.

[[HMG Developer Conference] 모뎀기반 고성능 제어기 속 OTA 개발기- HMG Developer Conference](https://www.youtube.com/watch?v=CeR6zv0dGu0&t=901s)

[Project Summary -  현대차 OTA 구조를 최대한 반영하여 프로토타입을 제작](https://dev-alohyomora.tistory.com/entry/%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%EA%B0%9C%EC%9A%94-%EB%AC%B4%EC%84%A0-%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8%EC%9D%98-%EB%AA%A8%EB%93%A0-%EA%B2%83-OTA-%ED%94%84%EB%A1%9C%ED%86%A0%ED%83%80%EC%9E%85-%EC%A0%9C%EC%9E%91%EA%B8%B0-%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98-%EB%B0%8F-%EC%A0%9C%ED%95%9C-%EC%82%AC%ED%95%AD-%EB%B6%84%EC%84%9D-%ED%98%84%EB%8C%80%EC%B0%A8-OTA-%EA%B5%AC%EC%A1%B0%EB%A5%BC-%EC%B5%9C%EB%8C%80%ED%95%9C-%EB%B0%98%EC%98%81%ED%95%9C-%ED%94%84%EB%A1%9C%ED%86%A0%ED%83%80%EC%9E%85)

---

- **Flask Server**: Manage firmware files and configure them to be downloadable on request from Raspberry Pi
- **Raspberry Pi (as CCU)**: Download the latest firmware from the Flask server, verify integrity, and perform an update
- **MySQL database**: Manage firmware versions and hash values, save download history
---

## 🎯 **Objectives**  
✅ **Develop a Flask-based OTA server** to manage firmware files  
✅ **Enable Raspberry Pi to download and verify firmware** (SHA-256 checksum validation)  
✅ **Implement MCU firmware updates on ESP32**  
✅ **Verify successful firmware application** after an update  

---

### Preview
[![Prototype Video Link]![image](https://github.com/user-attachments/assets/b7592a59-6aea-4c02-a5fa-7ee366f797c3)](https://www.youtube.com/watch?v=Toe-4wZa16E)


## ⚙️ System Architecture

```plaintext
+---------------------------+        +------------------------+
|  Raspberry Pi (CCU)       | <----> |  Flask OTA Server      |
|  - Download Firmware      |        |  - Firmware Management |
|  - Integrity Verification |        |  - MySQL Interworking  |
|  - Apply firmware         |        |  - API provision       |
+---------------------------+        +------------------------+
```

## 🛠️ **Tech Stack**  

### 🔹 **Software**  
- Python 3.x  
- Flask (Firmware distribution server)  
- Arduino IDE (ESP32 firmware development)  
- esptool.py (ESP32 firmware flashing)  
- Requests (HTTP API handling)  
- Bash (Automation scripts)  

### 🔹 **Hardware**  
- Raspberry Pi 5 (CCU)  
- ESP32-WROOM-32 (DCU)  
- UART communication (ESP32 <-> Raspberry Pi)  
- MicroSD card (Optional external storage)  

---

## 📂 **Project Structure**  

```
📁 OTA-Firmware-Update
│── 📂 firmware/                # Directory for firmware files
│── 📂 routes/                  # Flask API routes
│    │── firmware.py            # Firmware download API
│    │── auth.py                # Authentication API
│── 📂 Rasberrypi_Code          # Automation scripts for updates
│    │── download_firmware.py   # Download firmware from the Flask server
│    │── esp_firmware_manager.py # Flash firmware to ESP32
│── 📂 static/                  # Static files
│── 📂 templates/               # Web UI templates
│── app.py                      # Flask application entry point
│── config.py                   # Configuration file
│── database.py                 # Database connection settings
│── models.py                   # Database models
│── requirements.txt            # List of Python dependencies
│── README.md                   # Project documentation (this file)
```

---

## 🚀 **How to Run the Project**  

### 1️⃣ **Start the OTA Server (Flask)**
```bash
git clone https://github.com/your-repo-name/OTA-Firmware-Update.git
cd OTA-Firmware-Update
pip install -r requirements.txt
python app.py or flask run --host=0.0.0.0
```
✅ Once running, visit `http://localhost:5000 or your local ip` to check the firmware API  

---

### 2️⃣ **Download Firmware on Raspberry Pi**  
```bash
python3 Rasberrypi_Code/download_firmware.py
```
✅ The Raspberry Pi fetches the latest firmware from the Flask server and saves it locally.  

---

### 3️⃣ **Flash Firmware to ESP32**  
```bash
python3 Rasberrypi_Code/esp_firmware_manager.py
```
✅ Uses **esptool.py** to flash the `.bin` firmware to the ESP32.  

---

## 📌 **Project Progress**  

| **Step** | **Description** | **Status** |
| --- | --- | --- |
| **1. Firmware distribution via Flask server** | Firmware files can be downloaded through Flask API | ✅ Completed |
| **2. Download firmware on Raspberry Pi** | Using `curl` or Python script to fetch firmware from the server | ✅ Completed |
| **3. Verify firmware integrity** | Check SHA-256 checksum to ensure file integrity | ✅ Completed |
| **4. Test MCU firmware execution via UART in Arduino IDE** | Verify correct execution | ✅ Completed |
| **5. Prepare to apply firmware** | Compare old and new firmware to decide whether to update | ✅ Completed |
| **6. Apply firmware update (Write)** | Flash the downloaded `.bin` file to ESP32 | ✅ Completed |
| **7. Verify updated firmware** | Check if the new firmware runs correctly after reboot | ✅ Completed |
| **8. Implement rollback (Optional)** | Restore previous firmware if the update fails | ⏳ Pending |
| **9. Move firmware application to Raspberry Pi** | Manage firmware flashing via CCU instead of Ubuntu | ✅ Completed |

---

## 📝 **References**  
- [ESP32 OTA Update Official Documentation](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/index.html)  
- [Flask Official Documentation](https://flask.palletsprojects.com/)  
- [esptool.py GitHub Repository](https://github.com/espressif/esptool)  

---

## 📌 **License**  
This project is licensed under the **MIT License**. Feel free to modify and distribute it.  
**Pull requests** for improvements are always welcome! 🚀  
