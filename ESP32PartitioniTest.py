import subprocess

# ESP32 연결 정보
SERIAL_PORT = "/dev/ttyUSB0"
FLASH_ADDRESS = "0xe000"  # OTA 데이터 위치
FLASH_SIZE = "0x200"  # 읽을 데이터 크기
OUTPUT_FILE = "otadata.bin"  # 저장할 파일 이름

def read_esp_partition():
    """
    ESP32의 실행 중인 OTA 파티션 정보를 읽어 확인하는 함수
    """
    try:

        ESPTOOL_PATH = "/home/alohyomora/.arduino15/packages/esp32/tools/esptool_py/4.9.dev3/esptool"

        # 1️⃣ `esptool.py`로 otadata.bin 읽기
        esptool_cmd = [
            ESPTOOL_PATH, "--chip", "esp32", "--port", SERIAL_PORT, 
            "read_flash", FLASH_ADDRESS, FLASH_SIZE, OUTPUT_FILE
        ]
        subprocess.run(esptool_cmd, check=True)

        # 2️⃣ `hexdump`를 사용하여 파티션 정보 확인
        hexdump_cmd = ["hexdump", "-C", OUTPUT_FILE]
        hexdump_output = subprocess.check_output(hexdump_cmd).decode("utf-8")

        # 3️⃣ 실행 중인 파티션 찾기 (첫 번째 바이트 값 확인)
        first_byte = hexdump_output.split()[1]  # 첫 번째 바이트 값 추출
        print(first_byte)
        if first_byte == "01":
            return "ota_0 (app0)"
        elif first_byte == "02":
            return "ota_1 (app1)"
        else:
            return "⚠️ 파티션 정보를 확인할 수 없습니다."

    except subprocess.CalledProcessError as e:
        return f"🚨 오류 발생: {e}"
    except Exception as e:
        return f"❌ 예외 발생: {e}"

# 실행 중인 파티션 확인
running_partition = read_esp_partition()
print(f"✅ 현재 실행 중인 파티션: {running_partition}")