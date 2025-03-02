#include "esp_ota_ops.h"
#include "esp_partition.h"
#include "esp_system.h"
#include "esp_err.h"
#include "esp_partition.h"
#include "esp_log.h"
#include <string.h>
#define LED_PIN 23  // ESP32의 GPIO 23번 핀에 LED 연결
#define VERSION_PARTITION_LABEL "version"
#include <LiquidCrystal_I2C.h>        //LiquidCrysta_I2C 라이브러리 포함
LiquidCrystal_I2C lcd(0x3F, 16, 2);   // I2C lcd 주소값 확인 , 16x2

// 버전 설정
const float my_firmware_version = 1.1f;

void initLED() {
    pinMode(LED_PIN, OUTPUT);
}

void blinkLED() {
        digitalWrite(LED_PIN, HIGH);
        delay(500);
        digitalWrite(LED_PIN, LOW);
        delay(500);
    }
void print_error(esp_err_t err) {
    char err_buf[64];  // 에러 메시지를 저장할 버퍼
    esp_err_to_name_r(err, err_buf, sizeof(err_buf));
    Serial.printf("⚠ ESP_ERROR(%d): %s\n", err, err_buf);
}
// 펌웨어 버전을 특정 version 파티션에 저장
void write_firmware_version(float version) {
    const esp_partition_t* version_partition = esp_partition_find_first(ESP_PARTITION_TYPE_DATA, ESP_PARTITION_SUBTYPE_ANY, VERSION_PARTITION_LABEL);
    if (version_partition == NULL) {
        Serial.println("🚨 Version partition not found!");
        return;
    }
    Serial.printf("📌 Name: %s | Type: %d | SubType: %d | Offset: 0x%X | Size: %dKB\n",
                      version_partition->label, version_partition->type, version_partition->subtype, version_partition->address, version_partition->size / 1024);
    // 기존 데이터 지우기
    size_t erase_size = version_partition->size;  // 전체 파티션 크기 (32KB)
    esp_err_t err = esp_partition_erase_range(version_partition, 0, erase_size);
    if (err != ESP_OK) {
        print_error(err);  // 에러 메시지 출력
        return;
    }

    // 새로운 버전 정보 쓰기
    err = esp_partition_write(version_partition, 0, &version, sizeof(float));
    if (err == ESP_OK) {
        Serial.printf("✅ Firmware version %.2f written successfully.\n", version);
    } else {
        Serial.printf("⚠ Failed to write firmware version: %d\n", err);
    }
}

// 펌웨어 버전을 특정 NVS 파티션에서 읽어오기
void read_firmware_version() {
    const esp_partition_t* version_partition = esp_partition_find_first(ESP_PARTITION_TYPE_DATA, ESP_PARTITION_SUBTYPE_ANY, VERSION_PARTITION_LABEL);
    if (version_partition == NULL) {
        Serial.println("🚨 Version partition not found!");
        return;
    }

    float version = 0.0;
    esp_err_t err = esp_partition_read(version_partition, 0, &version, sizeof(float));
    if (err == ESP_OK) {
        Serial.printf("🔍 Current firmware version: %.2f\n", version);
    } else {
        Serial.printf("⚠ Failed to read firmware version: %d\n", err);
    }
}

void print_partitions() {
    Serial.println("🔍 현재 적용된 파티션 목록:");

    esp_partition_iterator_t it = esp_partition_find(ESP_PARTITION_TYPE_ANY, ESP_PARTITION_SUBTYPE_ANY, NULL);
    while (it != NULL) {
        const esp_partition_t *part = esp_partition_get(it);
        Serial.printf("📌 Name: %s | Type: %d | SubType: %d | Offset: 0x%X | Size: %dKB\n",
                      part->label, part->type, part->subtype, part->address, part->size / 1024);
        it = esp_partition_next(it);
    }

    Serial.println("✅ 파티션 정보 출력 완료.");
}

bool is_firmware_valid(const uint8_t *buffer, size_t size) {
    Serial.print("📥 Read buffer data: ");
    for (int i = 0; i < size; i++) {
        Serial.printf("%02X ", buffer[i]);
    }
    Serial.println();

    // 🔹 단순한 검증이 아니라, 보다 정확한 조건 추가 가능 (예: 특정 펌웨어 헤더 확인)
    return (buffer[0] != 0xFF);
}
#include "nvs_flash.h"
#include "nvs.h"

void init_nvs() {
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);
}

void check_running_partition() {
    const esp_partition_t *running = esp_ota_get_running_partition();
    Serial.printf("🔍 Currently running partition: %s\n", running->label);
}
void check_otadata() {
    const esp_partition_t* boot_partition = esp_ota_get_boot_partition();
    Serial.printf("Boot partition: %s\n", boot_partition->label);
}
void VisualizeFirmwareVersion(){
  lcd.init();               // lcd 초기화
  lcd.clear();
lcd.backlight();          // lcd 백라이트 on
lcd.setCursor(0, 0);      // 커서를 0,0 위치에 이동
lcd.print("It's LED Example");      
lcd.setCursor(0, 1);      // 커서를 0,1 위치에 이동
lcd.print("Version : ");
lcd.setCursor(10, 1);      // 커서를 0,1 위치에 이동
lcd.print(my_firmware_version);      // 5,1위치 부터 "World!" 출력 
}
void setup() {
    Serial.begin(115200);
    init_nvs();
    // print_partitions();

    // 현재 사용 중인 파티션 이름 출력 -> "app0", "app1"
    // check_running_partition();

    initLED();  // 버전 별 LED 초기화 함수 실행
    // read_firmware_version(); // 저장된 버전 읽기
    VisualizeFirmwareVersion();
}

void loop() {
    // check_otadata();
    // print_partitions();
    // read_firmware_version(); // 저장된 버전 읽기
    blinkLED();
}