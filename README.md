# 🛡️ SOC Automation Tools

A collection of Python scripts designed for SOC analysts to automate threat intelligence enrichment using the AbuseIPDB API.

## 📋 Features

- **IP Reputation Checker**: Batch check IP addresses against AbuseIPDB database
- **Domain Reputation Checker**: Batch check domains against AbuseIPDB database
- **CSV Export**: Automatically generate detailed CSV reports with threat scores and IOC information
- **Easy to Use**: Simple command-line interface for quick analysis during incident response

## 🔧 Prerequisites

- Python 3.8+
- AbuseIPDB API key (free tier available at [abuseipdb.com](https://www.abuseipdb.com))
- requests library

## 📦 Installation

1. Clone the repository:
git clone https://github.com/D1sCript/soc-automation-tools.git
cd soc-automation-tools


2. Install dependencies:
pip install requests


3. Set your AbuseIPDB API key in the scripts:
   - Open `ip_abuse_checker/ip_checker.py`
   - Replace `api_key` with your actual API key
   - Do the same for `domain_abuse_checker/domain_checker.py`

## 🚀 Usage

### IP Reputation Checker

python ip_abuse_checker/ip_checker.py


**How to use:**
1. Create a file with IP addresses (one per line), e.g., `ips.txt`
2. Update `INPUT_FILE` in the script to point to your file
3. Run the script
4. Results will be saved to a CSV file with timestamp

**Example input file:**
8.8.8.8
1.1.1.1
185.220.101.1
192.168.1.1


**Example output:**
IP Address,Abuse Confidence Score
8.8.8.8,Abuse score 0%
185.220.101.1,Abuse score 85%


### Domain Reputation Checker

python domain_abuse_checker/domain_checker.py


**How to use:**
1. Create a file with domains (one per line), e.g., `domains.txt`
2. Update `INPUT_FILE` in the script to point to your file
3. Run the script
4. Results will be saved to a CSV file with timestamp

**Example input file:**
google.com
example.com
suspicious-site.xyz


## 📊 Use Cases

- **Incident Response**: Quickly check reputation of suspicious IPs/domains from logs
- **Threat Hunting**: Batch check indicators of compromise (IOCs)
- **SIEM Integration**: Enrich security alerts with threat intelligence
- **Phishing Investigation**: Verify domains from suspicious emails
- **Security Research**: Analyze malicious infrastructure

## ⚠️ Disclaimer

These tools are provided for educational and professional security purposes only. Always ensure you have proper authorization before checking IP addresses or domains. The author is not responsible for any misuse.

## 📜 License

MIT License - See [LICENSE](LICENSE) for details

## 👤 Author

**D1sCript**
- GitHub: [@D1sCript](https://github.com/D1sCript)
- Telegram: [@D1sCript](https://t.me/D1sCript)

## 🙏 Acknowledgments

- [AbuseIPDB](https://www.abuseipdb.com) for providing the threat intelligence API
- SOC and Blue Team community

## 📞 Support

For issues or questions, please open an issue on GitHub.

---

⭐ If these tools are helpful, please consider giving a star!