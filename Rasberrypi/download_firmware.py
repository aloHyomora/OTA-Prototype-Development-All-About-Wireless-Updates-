import requests
import hashlib
import os

# Flask server details
FLASK_SERVER = "http://192.168.0.2:5000"
FIRMWARE_VERSION = "10.1.0"

# 1️⃣ Fetch the latest firmware details from the server
response = requests.get(f"{FLASK_SERVER}/firmware/latest")
if response.status_code != 200:
    print("❌ Failed to retrieve firmware details from the server.")
    exit()

firmware_info = response.json()
server_sha256 = firmware_info["sha256"]  # Expected SHA-256 hash from the server
file_url = f"{FLASK_SERVER}/firmware/download/{FIRMWARE_VERSION}"
file_name = os.path.basename(firmware_info["file_path"])  # Preserve original filename

print(f"✅ Firmware file from server: {file_name}")
print(f"✅ Expected SHA-256 from server: {server_sha256}")

# 2️⃣ Download the firmware file
print("📥 Downloading firmware...")
response = requests.get(file_url, stream=True)
if response.status_code != 200:
    print("❌ Firmware download failed!")
    exit()

# Save the downloaded firmware
with open(file_name, "wb") as file:
    for chunk in response.iter_content(chunk_size=1024):  # Download in 1KB chunks
        file.write(chunk)

print(f"✅ Download completed: {file_name}")

# 3️⃣ Compute SHA-256 hash of the downloaded file
def calculate_sha256(file_path):
    """Compute the SHA-256 hash of a given file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

local_sha256 = calculate_sha256(file_name)
print(f"✅ Computed SHA-256: {local_sha256}")

# 4️⃣ Compare the computed hash with the expected hash from the server
if local_sha256 == server_sha256:
    print("✅ Integrity check passed: The file is not corrupted.")
    # TODO: Proceed with firmware update on MCU
else:
    print("❌ Integrity check failed: The file is corrupted!")
    os.remove(file_name)  # Delete the corrupted file
    print("🗑️ Corrupted file has been deleted.")
