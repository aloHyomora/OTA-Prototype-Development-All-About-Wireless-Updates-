import subprocess
import time
import os
import struct

# ESP32 연결 정보
# TODO: Rasberry Pi 환경에 맞게 변경 필요
ESPTOOL_PATH = "./.arduino15/packages/esp32/tools/esptool_py/4.9.dev3/esptool"
SERIAL_PORT = "/dev/ttyUSB0"

# ESP32 SPI Flash 정보
FLASH_ADDRESS_OTADATA = "0xe000"  # OTA 데이터 위치
FLASH_SIZE_OTADATA = "0x200"  # OTA 데이터 크기
OUTPUT_FILE_OTADATA = "otadata.bin"  # OTA 데이터 저장 파일
FLASH_ADDRESS_VERSION = "0x3E0000"  # 버전 정보가 저장된 플래시 오프셋
FLASH_SIZE_VERSION = "0x8000"       # 버전 정보 저장 크기 (32KB)
OUTPUT_FILE_VERSION = "version_data.bin"  # 읽어온 데이터를 저장할 파일 경로

# OTA 파티션 주소 (현재 실행 중인 파티션을 기준으로 자동 결정)
FLASH_ADDRESS_APP0 = "0x10000"
FLASH_ADDRESS_APP1 = "0x150000"

def read_firmware_version():
    """
    현재 실행 중인 펌웨어 버전을 읽어오는 함수.
    """
    esptool_cmd = [
        ESPTOOL_PATH, "--chip", "esp32", "--port", SERIAL_PORT,
        "read_flash", FLASH_ADDRESS_VERSION, FLASH_SIZE_VERSION, OUTPUT_FILE_VERSION
    ]

    try:
        # esptool 실행하여 버전 데이터 읽어오기
        subprocess.run(esptool_cmd, check=True, capture_output=True)
        
        # 읽어온 데이터 파일에서 버전 정보 추출
        with open(OUTPUT_FILE_VERSION, "rb") as f:
            version_data = f.read(4)  # float 크기(4바이트)만큼 읽기
            version = struct.unpack("f", version_data)[0]  # 바이트 데이터를 float로 변환
        
        print(f"현재 실행 중인 펌웨어 버전: {version:.2f}")
        return version

    except subprocess.CalledProcessError as e:
        print(f"esptool 실행 실패: {e}")
    except Exception as e:
        print(f"버전 데이터 읽기 실패: {e}")

    return None

def read_esp_partition():
    """
    ESP32의 이미 저장되어 있는 OTA 파티션 정보를 읽어오는 함수
    """
    try:
        # 기존 otadata 파일 제거 (이전 데이터 남아 있을 가능성 방지)
        if os.path.exists(OUTPUT_FILE_OTADATA):
            os.remove(OUTPUT_FILE_OTADATA)

        # `esptool`로 otadata.bin 읽기
        esptool_cmd = [
            ESPTOOL_PATH, "--chip", "esp32", "--port", SERIAL_PORT,
            "read_flash", FLASH_ADDRESS_OTADATA, FLASH_SIZE_OTADATA, OUTPUT_FILE_OTADATA
        ]
        subprocess.run(esptool_cmd, check=True)

        # 1초 대기 (ESP32 플래시 데이터가 완전히 반영되도록)
        time.sleep(1.0)

        # 파일에서 첫 번째 바이트 직접 읽기
        with open(OUTPUT_FILE_OTADATA, "rb") as f:
            first_byte = f.read(1)  # 첫 번째 바이트만 읽기

        first_byte_hex = first_byte.hex().upper()  # 16진수로 변환
        if first_byte_hex == "01":
            print(f"현재 실행 중인 파티션 정보: app0")
            return "app0"
        elif first_byte_hex == "02":
            print(f"현재 실행 중인 파티션 정보: app1")
            return "app1"
        else:
            return None  # 알 수 없는 값일 경우 None 반환

    except subprocess.CalledProcessError as e:
        print(f"오류 발생: {e}")
        return None
    except Exception as e:
        print(f"예외 발생: {e}")
        return None

def restore_otadata(previous_partition):
    """
    otadata(0xe000) 영역을 기존 실행 중이던 파티션 정보로 복구하는 함수
    """
    try:
        if previous_partition == "app0":
            otadata_flag = b'\x01\x00\x00\x00' + b'\xFF' * 12  # 16바이트 유지
        elif previous_partition == "app1":
            otadata_flag = b'\x02\x00\x00\x00' + b'\xFF' * 12  # 16바이트 유지
        else:
            print("현재 실행 중인 파티션 정보를 알 수 없습니다.")
            return

        # otadata.bin 생성 및 데이터 기록
        with open(OUTPUT_FILE_OTADATA, "wb") as f:
            f.write(otadata_flag)

        # otadata 영역 복구
        restore_cmd = [
            ESPTOOL_PATH, "--chip", "esp32", "--port", SERIAL_PORT, 
            "write_flash", FLASH_ADDRESS_OTADATA, OUTPUT_FILE_OTADATA
        ]
        subprocess.run(restore_cmd, check=True)

        print(f"otadata를 {previous_partition}로 복구 완료!")

    except subprocess.CalledProcessError as e:
        print(f"otadata 복구 중 오류 발생: {e}")
    except Exception as e:
        print(f"예외 발생: {e}")

def write_firmware_version(version):
    """
    펌웨어 버전을 flash에 기록하는 함수.
    """
    try:
        version_data = struct.pack("f", version)  # float 값을 4바이트 binary로 변환
        version_file = "version.bin"

        # 1️. 바이너리 데이터를 임시 파일로 저장
        with open(version_file, "wb") as f:
            f.write(version_data)

        # 2️. 저장한 파일을 이용해 flash에 기록
        esptool_cmd = [
            ESPTOOL_PATH, "--chip", "esp32", "--port", SERIAL_PORT,
            "write_flash", FLASH_ADDRESS_VERSION, version_file
        ]
        subprocess.run(esptool_cmd, check=True)
        print(f"펌웨어 버전 {version:.2f} 기록 완료.")

        # 3️. 사용한 임시 파일 삭제 (필요한 경우)
        os.remove(version_file)

    except subprocess.CalledProcessError as e:
        print(f"펌웨어 버전 기록 실패: {e}")
    except Exception as e:
        print(f"예외 발생: {e}")

def write_otadata(target_partition):
    """
    OTA 데이터 파티션을 업데이트하여 부팅할 펌웨어 선택.
    """
    try:
        # 1️. OTA 데이터 생성
        ota_data = b'\x01\x00\x00\x00' + b'\xFF' * 12 if target_partition == "app0" else b'\x02\x00\x00\x00' + b'\xFF' * 12
        ota_file = "otadata.bin"

        # 2️. OTA 데이터를 임시 파일로 저장
        with open(ota_file, "wb") as f:
            f.write(ota_data)

        # 3️. 저장된 파일을 사용하여 write_flash 실행
        esptool_cmd = [
            ESPTOOL_PATH, "--chip", "esp32", "--port", SERIAL_PORT,
            "write_flash", "0xe000", ota_file
        ]
        subprocess.run(esptool_cmd, check=True)
        print(f"OTA 데이터 업데이트 완료: {target_partition}")

        # 4️. 사용한 임시 파일 삭제
        os.remove(ota_file)

    except subprocess.CalledProcessError as e:
        print(f"OTA 데이터 업데이트 실패: {e}")
    except Exception as e:
        print(f"예외 발생: {e}")

def write_firmware(firmware_bin, firmware_version):
    """
    새로운 펌웨어를 특정 OTA 파티션에 write하고, 현재 실행 중인 버전보다 높은 경우에만 write 수행.
    """
    try:
        # # 1️. 현재 실행 중인 펌웨어 버전 확인
        # current_version = read_firmware_version()
        # if current_version is None:
        #     print("현재 펌웨어 버전 확인 실패.")
        #     return

        # # 2️. 새 버전이 현재 버전보다 높은 경우에만 진행
        # if firmware_version <= current_version:
        #     print(f"현재 펌웨어 버전({current_version:.2f})보다 같거나 낮은 버전({firmware_version:.2f})은 업데이트하지 않습니다.")
        #     return

        print(f"새로운 버전({firmware_version:.2f})이 확인됨. 업데이트 진행...")

        # 3️. 현재 실행 중인 파티션 확인
        previous_partition = read_esp_partition()
        if not previous_partition:
            print("현재 실행 중인 파티션 정보를 확인할 수 없습니다.")
            return

        # 4️. OTA 파티션 주소 자동 결정
        target_partition = "app1" if previous_partition == "app0" else "app0"
        flash_address = FLASH_ADDRESS_APP1 if previous_partition == "app0" else FLASH_ADDRESS_APP0

        print(f"{target_partition} ({flash_address})에 {firmware_bin} 업로드 중...")
        write_cmd = [
            ESPTOOL_PATH, "--chip", "esp32", "--port", SERIAL_PORT,
            "--baud", "115200", "--before", "default_reset", "--after", "hard_reset",
            "write_flash", "-z", flash_address, firmware_bin
        ]
        subprocess.run(write_cmd, check=True)
        print(f"{target_partition} ({flash_address})에 {firmware_bin} 업로드 완료")

        # 5️.OTA 데이터 업데이트
        write_otadata(target_partition)

        # 6️. 펌웨어 버전 업데이트
        write_firmware_version(firmware_version)


    except subprocess.CalledProcessError as e:
        print(f"오류 발생: {e}")
    except Exception as e:
        print(f"예외 발생: {e}")

def erase_unused_ota_partition():
    """
    현재 실행 중이지 않은 OTA 파티션을 찾아 데이터를 지우는 함수.
    """
    try:
        # 1️. 현재 실행 중인 파티션 확인
        current_partition = read_esp_partition()
        if not current_partition:
            print("현재 실행 중인 파티션 정보를 확인할 수 없습니다.")
            return
        
        # 2️. 지울 대상 파티션 결정
        target_partition = "app1" if current_partition == "app0" else "app0"
        flash_address = FLASH_ADDRESS_APP1 if target_partition == "app1" else FLASH_ADDRESS_APP0

        print(f"사용하지 않는 OTA 파티션 {target_partition} ({flash_address}) 지우기 시작...")

        # 3️. erase 명령 실행
        erase_cmd = [
            ESPTOOL_PATH, "--chip", "esp32", "--port", SERIAL_PORT,
            "erase_region", flash_address, "0x140000"  # OTA 파티션 크기 (1.25MB)
        ]
        subprocess.run(erase_cmd, check=True)
        
        print(f"{target_partition} ({flash_address}) 데이터 삭제 완료.")

    except subprocess.CalledProcessError as e:
        print(f"오류 발생: {e}")
    except Exception as e:
        print(f"예외 발생: {e}")

# 최신 버전 비교, 검사 로직 제거
# write_firmware("/home/alohyomora/Flask-FastAPI-Study/hardware/LEDControllerV1_0/build/esp32.esp32.esp32/LEDControllerV1_0.ino.bin", 1.0)
# write_firmware("/home/alohyomora/Flask-FastAPI-Study/hardware/LEDControllerV1_1/build/esp32.esp32.esp32/LEDControllerV1_1.ino.bin", 1.1)
# erase_unused_ota_partition()
# read_esp_partition()
# read_firmware_version()
# write_firmware_version(0.0)
# write_otadata("app1")