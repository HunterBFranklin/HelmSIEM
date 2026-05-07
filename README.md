# Personal SIEM System
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

### Wazuh Dashboard:
![Wazuh Dashboard](screenshots/wazuh-dashboard.png)

### Ubuntu VM (XFCE Desktop):
![VM Desktop](screenshots/vm-desktop.png)

### Monitored Endpoint — Neofetch:
![Neofetch](screenshots/neofetch.png)

### Python Alert Script — Terminal Output:
![Terminal Report](screenshots/terminal-report.png)

### Automated Email Report:
![Email Report](screenshots/email-report.png)

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
| Kibana | Dashboard and visualization |
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
- UTM — free at mac.getutm.app
- Ubuntu 22.04.5 LTS ARM64 Server ISO

### Start Wazuh:
```bash
git clone https://github.com/wazuh/wazuh-docker.git -b v4.14.5
cd wazuh-docker/single-node
docker compose -f generate-indexer-certs.yml run --rm generator
docker compose up -d
```

### Dashboard:
https://localhost
Username: admin
Password: SecretPassword

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
**CVE-2026-26066** on the Ubuntu VM — a medium severity ImageMagick 
vulnerability (CVSS 6.2) that causes a denial of service via a crafted 
image profile. I hadn't manually triggered anything — it just showed up 
in the dashboard.

I looked it up on NVD, confirmed it was real, patched it with 
`sudo apt upgrade`, and watched it clear from the findings. That whole 
cycle — detection, research, remediation, verification — is what made 
this project click for me.

---

## Project Structure

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

**v3.0 — Planned**
- SMS alerting for new devices joining the network (Twilio)
- Slack webhook integration
- Custom Wazuh detection rules
- Suricata network traffic analysis

---

**v4.0 — Planned**
- Windows endpoint agent (when PC arrives)
- JavaScript custom dashboard
- Home server and VPN integration
- Honeypot deployment
- Full homelab network monitoring

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