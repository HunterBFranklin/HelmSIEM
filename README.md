<div align="center">
<img src="https://img.shields.io/badge/🛡️_Self--Hosted-Personal_SIEM_System-2ea44f?style=for-the-badge&logoColor=white&labelColor=1a3a2a" width="600"/>
<br>
<img src="https://img.shields.io/badge/Current_Version_:_2.0-238636?style=for-the-badge&labelColor=1a3a2a" width="180"/>
</div>
<br>

A self-hosted Security Information and Event Management (SIEM) system built from the ground up using Docker, Wazuh, and the Elasticsearch/Logstash/Kibana (ELK) Stack. 
This project simulates a real-world security operations environment by monitoring live endpoints, detecting threats, mapping them to the 
MITRE ATT&CK framework, and delivering automated HTML security reports via email.

*A personal learning project documenting my journey into cybersecurity engineering, infrastructure, and security automation.*

## Screenshots

<table>
  <tr>
    <td align="center" style="background-color:#1a3a2a; padding:8px;">
      <img src="https://img.shields.io/badge/Wazuh-Dashboard-2ea44f?style=for-the-badge"/>
    </td>
    <td align="center" style="background-color:#1a3a2a; padding:8px;">
      <img src="https://img.shields.io/badge/VM-Desktop-2ea44f?style=for-the-badge"/>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="screenshots/wazuh-dashboard.png" width="480"/>
    </td>
    <td align="center">
      <img src="screenshots/vm-desktop.png" width="480"/>
    </td>
  </tr>
  <tr>
    <td align="center" style="background-color:#1a3a2a; padding:8px;">
      <img src="https://img.shields.io/badge/Neofetch-Endpoint-2ea44f?style=for-the-badge"/>
    </td>
    <td align="center" style="background-color:#1a3a2a; padding:8px;">
      <img src="https://img.shields.io/badge/Terminal-Report-2ea44f?style=for-the-badge"/>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="screenshots/neofetch.png" width="480"/>
    </td>
    <td align="center">
      <img src="screenshots/terminal-report.png" width="480"/>
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center" style="background-color:#1a3a2a; padding:8px;">
      <img src="https://img.shields.io/badge/Email-Report-2ea44f?style=for-the-badge"/>
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <img src="screenshots/email-report.png" width="480"/>
    </td>
  </tr>
</table>

## What It Does

- Collects security events from two endpoints — my MacBook Pro and 
  a Ubuntu 22.04 VM running in UTM
- Detects threats like brute force attempts, failed logins, privilege 
  escalation, and file integrity violations
- Maps every alert to a MITRE ATT&CK technique automatically
- Scans for known CVEs on monitored endpoints against the NVD database
- Runs a Python script that queries Elasticsearch directly and sends 
  a formatted HTML email report
- Monitors compliance against PCI DSS, HIPAA, NIST, and GDPR frameworks

## Stack

| Tool | Purpose |
|---|---|
| Wazuh 4.14.5 | HIDS, log collection, vulnerability detection |
| Elasticsearch | Event storage and indexing |
| Docker + Compose | Runs the whole stack in containers |
| Ubuntu 22.04 LTS ARM64 | Monitored Linux VM endpoint |
| UTM | Virtualization on Apple Silicon |
| Python 3 | Alert automation and email reporting |
| macOS (M3 Pro) | Host machine |

## How I Set It Up

### Requirements
- Docker Desktop (Apple Silicon)
- Python 3
- UTM
- Ubuntu 22.04.5 LTS ARM64 Server ISO

### Start Wazuh:
```bash
git clone https://github.com/wazuh/wazuh-docker.git -b v4.14.5
cd wazuh-docker/single-node
docker compose -f generate-indexer-certs.yml run --rm generator
docker compose up -d
```

### Dashboard:
```
https://localhost
Username: admin
Password: SecretPassword
```

### Python alerting script:
```bash
pip3 install -r requirements.txt
cp scripts/.env.example scripts/.env
# fill in your credentials
python3 scripts/alert_notifier.py
```

## Something That Actually Worked

While the system was running, Wazuh automatically flagged 
**CVE-2026-26066** on the Ubuntu VM; a medium severity ImageMagick 
vulnerability (CVSS 6.2) that causes a denial of service via a crafted 
image profile. I hadn't manually triggered anything — it just showed up 
in the dashboard.

I looked it up on NVD, confirmed it was real, patched it with 
`sudo apt upgrade`, and watched it clear from the findings. That whole 
cycle — detection, research, remediation, verification — is what made 
this project click for me.

## Project Structure
```
selfhosted-siem-system/
├── scripts/
│   ├── run.py                   # master runner — executes all three reports in sequence
│   ├── critical_alerts.py       # level 12+ severity only
│   ├── high_alerts.py           # level 7-11 severity
│   ├── all_alerts.py            # all alerts level 1+
│   ├── config.py                # centralized configuration and env variables
│   ├── elasticsearch_client.py  # Elasticsearch API queries
│   ├── formatter.py             # HTML report formatting and template building
│   ├── email_reporter.py        # HTML email construction and delivery
│   ├── utils.py                 # shared helper functions and terminal output
│   ├── .env                     # local credentials — never committed
│   └── .env.example             # credential template — safe to commit
├── templates/
│   └── email_template.html      # HTML email template (coming v2.0)
├── logs/
│   └── alert.log                # script output log
├── screenshots/
│   ├── wazuh-dashboard.png
│   ├── vm-desktop.png
│   ├── neofetch.png
│   ├── terminal-report.png
│   └── email-report.png
├── docs/                        # additional documentation
├── requirements.txt             # Python dependencies
├── .gitignore                   # protects credentials from Git
└── README.md
```

## What's Done and What's Next

Done:
- Wazuh + ELK stack running in Docker
- Ubuntu VM and MacBook Pro both monitored
- Python script querying Elasticsearch API
- HTML email reports with severity breakdown and MITRE mapping
- Real CVE detected and remediated
- Credentials protected with python-dotenv

Next:
- Cron job for automated 15 minute reporting
- SMS alerts for new devices joining the network (Twilio)
- Custom Wazuh detection rules
- Suricata for network traffic analysis
- Windows endpoint when I get a PC later this year
- Eventually tie this into a full homelab with a home server and VPN

## Versions

**v1.0 — May 2026 (current)**
- Wazuh + ELK stack deployed via Docker
- Ubuntu 22.04 LTS ARM64 VM configured as monitored endpoint
- MacBook Pro M3 connected as second live agent
- Python script querying Elasticsearch API directly
- Plain text terminal alert report
- Basic email delivery via Gmail SMTP
- Real CVE detected and remediated (CVE-2026-26066)
- Credentials secured with python-dotenv

**v2.0 — In Development**
- Branded HTML email reports with severity charts and MITRE breakdown
- Agent breakdown and MITRE ATT&CK technique summary in email
- Improved error handling and logging
- Cron job scheduling for automated 15 minute reports

## References:

**Infrastructure:**
- [Wazuh Documentation](https://documentation.wazuh.com)
- [Wazuh Docker Deployment](https://documentation.wazuh.com/current/deployment-options/docker/wazuh-container.html)
- [Wazuh GitHub](https://github.com/wazuh/wazuh-docker)
- [Docker Documentation](https://docs.docker.com)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [UTM Virtualization](https://docs.getutm.app)
- [Ubuntu Server ARM64](https://cdimage.ubuntu.com/releases/22.04/release/)

**ELK Stack:**
- [Elasticsearch REST API](https://www.elastic.co/guide/en/elasticsearch/reference/current/rest-apis.html)
- [Elasticsearch Python Client](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html)
- [Kibana Documentation](https://www.elastic.co/guide/en/kibana/current/index.html)
- [Logstash Documentation](https://www.elastic.co/guide/en/logstash/current/index.html)

**Security Frameworks:**
- [MITRE ATT&CK Framework](https://attack.mitre.org)
- [NVD — National Vulnerability Database](https://nvd.nist.gov)
- [CVE Database](https://cve.mitre.org)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [CVE-2026-26066 Advisory](https://github.com/advisories/GHSA-v994-63cg-9wj3)

**Python Libraries:**
- [Requests](https://docs.python-requests.org)
- [urllib3](https://urllib3.readthedocs.io)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [smtplib](https://docs.python.org/3/library/smtplib.html)
- [schedule](https://schedule.readthedocs.io)

**Desktop Environment:**
- [XFCE](https://www.xfce.org)
- [Oh My Zsh](https://ohmyz.sh)
- [Neofetch](https://github.com/dylanaraps/neofetch)

**README Design:**
- [Shields.io](https://shields.io)
- [GitHub Markdown Syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
- [GitHub Table Formatting](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-tables)
- [Best README Template](https://github.com/othneildrew/Best-README-Template)
- [Awesome README](https://github.com/matiassingers/awesome-readme)

**Community:**
- [r/homelab](https://reddit.com/r/homelab)
- [r/selfhosted](https://reddit.com/r/selfhosted)
- [r/cybersecurity](https://reddit.com/r/cybersecurity)
- [Wazuh Community](https://wazuh.com/community)

[@HunterBFranklin](https://github.com/HunterBFranklin) — MIT License
