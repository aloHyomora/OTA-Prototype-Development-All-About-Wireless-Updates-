import requests
import hashlib
import os


# Flask server details
FLASK_SERVER = "http://192.168.0.2:5000"
# FIRMWARE_VERSION = "10.1.0" For Test

# 1️. Fetch the latest firmware details from the server
response = requests.get(f"{FLASK_SERVER}/firmware/latest")
if response.status_code != 200:
    print("Failed to retrieve firmware details from the server.")
    exit()

firmware_info = response.json()
server_sha256 = firmware_info["sha256"]  # Expected SHA-256 hash from the server
file_request_url = f"{FLASK_SERVER}/firmware/download/{firmware_info['version']}"
file_name = os.path.basename(firmware_info["file_path"])  # Preserve original filename

print(f"Firmware file from server: {file_name}")
print(f"Expected SHA-256 from server: {server_sha256}")

# 2️. Download the firmware file

# 저장할 폴더 경로 설정
save_dir = "/home/aloho/OTAProject/Firmware"  # 원하는 폴더 경로 설정
os.makedirs(save_dir, exist_ok=True)  # 폴더가 없으면 생성
# 전체 저장 경로
save_file_path = os.path.join(save_dir, file_name)

print(f"Downloading firmware... {file_request_url}")
response = requests.get(file_request_url, stream=True)
if response.status_code != 200:
    print("Firmware download failed!")
    exit()

# Save the downloaded firmware
with open(save_file_path, "wb") as file:
    for chunk in response.iter_content(chunk_size=1024):  # Download in 1KB chunks
        file.write(chunk)

print(f"Download completed: {file_name}")

# 3️. Compute SHA-256 hash of the downloaded file
def calculate_sha256(file_path):
    """Compute the SHA-256 hash of a given file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

local_sha256 = calculate_sha256(save_dir + '/' + file_name)
print(f"Computed SHA-256: {local_sha256}")

# 4️. Compare the computed hash with the expected hash from the server
if local_sha256 == server_sha256:
    print("[Perfect] Integrity check passed: The file is not corrupted.")
    
    # 5. Proceed with firmware update on MCU
    import esp_firmware_manager
    print("Firmware will be updated soon...")
    esp_firmware_manager.write_firmware(save_file_path, float(firmware_info["version"]))
    esp_firmware_manager.erase_unused_ota_partition()

else:
    print("Integrity check failed: The file is corrupted!")
    os.remove(file_name)  # Delete the corrupted file
    print("Corrupted file has been deleted.")
