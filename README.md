# Self-Hosted Personal SIEM System
**Hunter Franklin — Started May 2026**

---

I built this project to get hands-on experience with security monitoring 
infrastructure. It's a working SIEM that collects and analyzes security 
events from real endpoints, maps them to the MITRE ATT&CK framework, and 
sends automated email reports. Everything runs locally on my MacBook Pro M3 
via Docker.

This is an ongoing project — I'm adding to it as I learn.

---

## Screenshots:

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

---

## What It Does:

- Collects security events from two endpoints — my MacBook Pro and 
  a Ubuntu 22.04 VM running in UTM
- Detects threats like brute force attempts, failed logins, privilege 
  escalation, and file integrity violations
- Maps every alert to a MITRE ATT&CK technique automatically
- Scans for known CVEs on monitored endpoints against the NVD database
- Runs a Python script that queries Elasticsearch directly and sends 
  a formatted HTML email report
- Monitors compliance against PCI DSS, HIPAA, NIST, and GDPR frameworks

---

## Stack:

| Tool | Purpose |
|---|---|
| Wazuh 4.14.5 | HIDS, log collection, vulnerability detection |
| Elasticsearch | Event storage and indexing |
| Docker + Compose | Runs the whole stack in containers |
| Ubuntu 22.04 LTS ARM64 | Monitored Linux VM endpoint |
| UTM | Virtualization on Apple Silicon |
| Python 3 | Alert automation and email reporting |
| macOS (M3 Pro) | Host machine |

---

## How I Set It Up:

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

---

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

---

## Project Structure
```
personal-siem/
├── scripts/
│   ├── alert_notifier.py    # queries Elasticsearch, sends email report
│   ├── .env.example         # credential template
│   └── .env                 # local credentials, not committed
├── screenshots/
├── docs/
├── requirements.txt
├── .gitignore
└── README.md
```
---

## What's Done and What's Next:

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

---

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

---

**v2.0 — In Development**
- Branded HTML email reports with severity charts and MITRE breakdown
- Agent breakdown and MITRE ATT&CK technique summary in email
- Improved error handling and logging
- Cron job scheduling for automated 15 minute reports

---

## References

- [Wazuh Docs](https://documentation.wazuh.com)
- [Elasticsearch API](https://www.elastic.co/guide/en/elasticsearch/reference/current/rest-apis.html)
- [MITRE ATT&CK](https://attack.mitre.org)
- [NVD](https://nvd.nist.gov)
- [CVE-2026-26066](https://github.com/advisories/GHSA-v994-63cg-9wj3)
- [Docker Docs](https://docs.docker.com)
- [UTM](https://docs.getutm.app)

---

[@HunterBFranklin](https://github.com/HunterBFranklin) — MIT License
