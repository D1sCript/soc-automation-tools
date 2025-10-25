import requests
import csv
import os
import sys
from datetime import datetime
import socket

# Configuration
API_KEY = "Your API KEY"
INPUT_FILE = path_to_file_with_domain  # File with domains

# Create a name for the results file
input_directory = os.path.dirname(INPUT_FILE)
output_filename = f"abuseipdb_domains_results_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.csv"
OUTPUT_FILE = os.path.join(input_directory, output_filename)

def get_ip_from_domain(domain):
    """Function to get IP address from domain name"""
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.gaierror:
        print(f"   ❌ Error: Failed to resolve domain {domain}")
        return None

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
        print(f"   ❌ HTTP error: {err}")
    except Exception as err:
        print(f"   ❌ Another error: {err}")
    return None

def main():
    """Main function"""
    # v
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as file:
            domain_list = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"❌ File {INPUT_FILE} not found.")
        return

    print(f"🔍 Check {len(domain_list)} domains...")
    print("=" * 70)

    # Create and save the results to a CSV file
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write down the title
        writer.writerow(["Domain", "IP Address", "Abuse Confidence Score"])
        
        for domain in domain_list:
            print(f"🌐 Domain Analysis: {domain}")
            
            # Obtaining an IP from a domain
            ip_address = get_ip_from_domain(domain)
            
            if ip_address is None:
                print("   ❌ Failed to obtain IP address\n")
                writer.writerow([domain, "Resolution Error", "N/A"])
                print("-" * 50)
                continue
                
            print(f"   📡 IP-adress: {ip_address}")
            
            # Checking IP addresses using AbuseIPDB
            result = check_ip(ip_address)
            
            if result is None:
                print("   ❌ Failed to retrieve data from AbuseIPDB\n")
                writer.writerow([domain, ip_address, "API Error"])
                print("-" * 50)
                continue

            data = result.get('data', {})
            abuse_score = data.get('abuseConfidenceScore', 0)
            
            # Writing data to CSV
            writer.writerow([domain, ip_address, f"Abuse score {abuse_score}%"])
            
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
            
            # Forcefully flush the output buffer
            sys.stdout.flush()

    print(f"\n✅ The results are saved to a file.: {OUTPUT_FILE}")
    print("\n" + "=" * 70)
    input("🎯 Press Enter to exit...")

if __name__ == "__main__":
    main()
