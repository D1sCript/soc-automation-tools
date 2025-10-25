import requests
import csv
import os
import sys
from datetime import datetime

# Конфигурация
API_KEY = "YOUR_API_KEY"
INPUT_FILE = path_to_file_with_domain

# Создаем имя для файла с результатами
input_directory = os.path.dirname(INPUT_FILE)
output_filename = f"abuseipdb_results_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.csv"
OUTPUT_FILE = os.path.join(input_directory, output_filename)

def check_ip(ip_address):
    """Функция для проверки одного IP-адреса через AbuseIPDB API"""
    url = 'https://api.abuseipdb.com/api/v2/check'
    
    headers = {
        'Accept': 'application/json',
        'Key': API_KEY
    }
    
    querystring = {
        'ipAddress': ip_address,
        'maxAgeInDays': '90'
    }

    try:
        response = requests.request(method='GET', url=url, headers=headers, params=querystring)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP ошибка для IP {ip_address}: {err}")
    except Exception as err:
        print(f"Другая ошибка для IP {ip_address}: {err}")
    return None

def main():
    """Основная функция"""
    # Читаем IP-адреса из файла
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as file:
            ip_list = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Файл {INPUT_FILE} не найден.")
        return

    print(f"🔍 Проверяем {len(ip_list)} IP-адресов...")
    print("=" * 70)

    # Создаем и записываем результаты в CSV файл
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["IP Address", "Abuse Confidence Score"])
        
        for ip in ip_list:
            print(f"\n📡 Анализ IP: {ip}")
            result = check_ip(ip)
            
            if result is None:
                print("   ❌ Не удалось получить данные")
                writer.writerow([ip, "Error"])
                continue

            data = result.get('data', {})
            abuse_score = data.get('abuseConfidenceScore', 0)
            
            # Записываем данные в CSV
            writer.writerow([ip, f"Abuse score {abuse_score}%"])
            
            # ДЕТАЛЬНЫЙ ВЫВОД НА ЭКРАН
            country = data.get('countryCode', 'N/A')
            usage_type = data.get('usageType', 'N/A')
            isp = data.get('isp', 'N/A')
            total_reports = data.get('totalReports', 0)
            is_whitelisted = data.get('isWhitelisted', False)
            last_reported = data.get('lastReportedAt', 'N/A')
            
            print(f"   ✅ Уровень угрозы: {abuse_score}%")
            print(f"   🌍 Страна: {country}")
            print(f"   💼 Тип использования: {usage_type}")
            print(f"   📡 Провайдер: {isp}")
            print(f"   📊 Всего отчетов: {total_reports}")
            print(f"   🛡️  В белом списке: {is_whitelisted}")
            print(f"   ⏰ Последний отчет: {last_reported}")
            print("-" * 50)
            
            # Принудительно сбрасываем буфер вывода :cite[9]
            sys.stdout.flush()

    print(f"\n✅ Результаты сохранены в файл: {OUTPUT_FILE}")
    print("\n" + "=" * 70)
    input("🎯 Нажмите Enter чтобы выйти...")

if __name__ == "__main__":
    main()
