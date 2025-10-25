import requests
import csv
import os
import sys
from datetime import datetime

# Configuration
API_KEY = "YOUR_API_KEY"
INPUT_FILE = path_to_file_with_domain

# Create a name for the results file
input_directory = os.path.dirname(INPUT_FILE)
output_filename = f"abuseipdb_results_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.csv"
OUTPUT_FILE = os.path.join(input_directory, output_filename)

def check_ip(ip_address):
    """A function for checking a single IP address via the AbuseIPDB API"""
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
        print(f"HTTP error for IP {ip_address}: {err}")
    except Exception as err:
        print(f"Another error for IP {ip_address}: {err}")
    return None

def main():
    """Main function"""
    # Reading IP addresses from a file
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as file:
            ip_list = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"File {INPUT_FILE} not found.")
        return

    print(f"🔍 Checking {len(ip_list)} IP addresses...")
    print("=" * 70)

    # Create and save the results to a CSV file
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["IP Address", "Abuse Confidence Score"])
        
        for ip in ip_list:
            print(f"\n📡 Analysis IP: {ip}")
            result = check_ip(ip)
            
            if result is None:
                print("   ❌ Failed to retrieve data")
                writer.writerow([ip, "Error"])
                continue

            data = result.get('data', {})
            abuse_score = data.get('abuseConfidenceScore', 0)
            
            # Writing data to CSV
            writer.writerow([ip, f"Abuse score {abuse_score}%"])
            
            # DETAILED SCREEN OUTPUT
            country = data.get('countryCode', 'N/A')
            usage_type = data.get('usageType', 'N/A')
            isp = data.get('isp', 'N/A')
            total_reports = data.get('totalReports', 0)
            is_whitelisted = data.get('isWhitelisted', False)
            last_reported = data.get('lastReportedAt', 'N/A')
            
            print(f"   ✅ Threat level: {abuse_score}%")
            print(f"   🌍 Country: {country}")
            print(f"   💼 Type of use: {usage_type}")
            print(f"   📡 Provider: {isp}")
            print(f"   📊 Total reports: {total_reports}")
            print(f"   🛡️  Whitelisted: {is_whitelisted}")
            print(f"   ⏰ Latest report: {last_reported}")
            print("-" * 50)
            
            # Forcefully flush the output buffer :cite[9]
            sys.stdout.flush()

    print(f"\n✅ The results are saved to a file.: {OUTPUT_FILE}")
    print("\n" + "=" * 70)
    input("🎯 Press Enter to exit...")

if __name__ == "__main__":
    main()
