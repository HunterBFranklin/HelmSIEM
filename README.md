<div align="center">
<img src="https://img.shields.io/badge/🛡️_Self--Hosted-Personal_SIEM_System-2ea44f?style=for-the-badge&logoColor=white&labelColor=1a3a2a" width="600"/>
<br>
<img src="https://img.shields.io/badge/Current_Version_:_2.0-238636?style=for-the-badge&labelColor=1a3a2a" width="180"/>
</div>
<br>

A self-hosted Security Information and Event Management (SIEM) system built from the ground up using Docker, Wazuh, and the Elasticsearch/Logstash/Kibana (ELK) Stack. 
The system monitors live endpoints in real time, detects threats ranging from brute force attempts and privilege escalation to file integrity violations and CVE 
vulnerabilities, and maps every alert to the MITRE ATT&CK framework automatically.

Security events are collected from two active endpoints, an Apple Silicon MacBook Pro M3 and a Ubuntu 22.04 LTS virtual machine running in UTM, and 
fed into a centralized Wazuh manager running in Docker. A modular Python automation layer queries the Elasticsearch API directly to generate tiered reports 
across three severity levels (critical, high, and all alerts), delivering fully formatted HTML email reports with severity breakdowns, MITRE technique bar charts, 
and color-coded alert details.

Beyond detection, the system integrates Fail2Ban for automated threat response — automatically banning IPs that trigger repeated SSH failures — and cross-references 
installed packages against the National Vulnerability Database for continuous CVE monitoring. Compliance mapping against PCI DSS, HIPAA, NIST 800-53, and GDPR runs passively 
in the background on every monitored endpoint.

_This is an ongoing personal project documenting my journey into cybersecurity engineering, security automation, network engineering, and infrastructure. It started as a basic Wazuh deployment and 
has grown into a structured, versioned security operations platform, with a homelab, home server, and VPN integration planned as the next phase of expansion._

## Screenshots

<h3>v2.0 — Current</h3>

<table>
  <tr>
    <td colspan="2" align="center">
      <img src="https://img.shields.io/badge/Email-Report_v2-2ea44f?style=for-the-badge"/>
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <img src="screenshots/v2.0/email-report.png" width="960"/>
    </td>
  </tr>
</table>

<h3>v1.0 — Initial Release</h3>

<table>
  <tr>
    <td align="center">
      <img src="https://img.shields.io/badge/Email-Report_v1-238636?style=for-the-badge"/>
    </td>
    <td align="center">
      <img src="https://img.shields.io/badge/Terminal-Report_v1-238636?style=for-the-badge"/>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="screenshots/v1.0/email-report.png" width="480"/>
    </td>
    <td align="center">
      <img src="screenshots/v1.0/terminal-report.png" width="480"/>
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <img src="https://img.shields.io/badge/Neofetch-Endpoint-238636?style=for-the-badge"/>
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <img src="screenshots/v1.0/neofetch.png" width="480"/>
    </td>
  </tr>
</table>

## What It Does

- Collects security events from two endpoints: my MacBook Pro M3 and a Ubuntu 22.04 LTS VM running in UTM on Apple Silicon
- Detects threats, including brute force attempts, failed logins, privilege escalation, file integrity violations, and unauthorized SSH access
- Automatically bans malicious IPs via Fail2Ban integration after repeated failed SSH attempts
- Maps every alert to a MITRE ATT&CK technique and tactic automatically
- Scans monitored endpoints for known CVEs cross-referenced against the NVD database
- Runs three severity tier Python scripts (critical, high, all) that query Elasticsearch directly via REST API
- Delivers fully formatted HTML email reports with severity breakdown, MITRE bar chart, and color-coded alert details
- Converts all timestamps from UTC to local time automatically
- Monitors compliance against PCI DSS, HIPAA, NIST 800-53, and GDPR frameworks
- Master runner executes all three report tiers in sequence with a single command

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
│   ├── utility.py               # shared helper functions and terminal output
│   ├── daily_recap.py           # main daily recap orchestrator (v3.0) 
│   ├── recap_formatter.py       # builds the daily recap HTML email (v3.0)
│   ├── scheduler.py             # toggle on/off, handles 8 PM PST scheduling (v3.0)
│   ├── .env                     # local credentials — never committed
│   └── .env.example             # credential template — safe to commit
├── templates/
│   └── email_template.html      # HTML email template (v3.0)
├── logs/
│   └── alert.log                # script output log (v3.0)
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
- Fail2Ban installed with subnet whitelist for automated SSH ban detection
- Modular Python architecture — config, elasticsearch_client, formatter, email_reporter, utility
- Three severity tier runners — critical (12-15), high (7-11), all (1+)
- Master runner executing all three reports in sequence
- Fully redesigned HTML email with Gmail-compatible table layout
- Severity breakdown cards matching Wazuh rule level scale (1-3/4-6/7-11/12-15)
- CSS horizontal bar chart for MITRE ATT&CK techniques
- Color-coded severity badges and technique bubbles in alert details
- UTC to local timezone conversion on all timestamps
- Real CVE detected, researched, and remediated (CVE-2026-26066)
- Credentials protected with python-dotenv
- Versioned screenshots documenting v1.0 and v2.0 progression

Next:
- Cron job for automated scheduled reporting
- SMS alerts for new devices joining the network (Twilio)
- Custom Wazuh detection rules
- Suricata for network traffic analysis
- JavaScript custom dashboard
- Windows endpoint when I get a PC later this year
- Eventually tie this into a full homelab with a home server and VPN

## Roadmap
```
- [x] Wazuh + ELK stack deployed via Docker
- [x] Ubuntu VM monitored endpoint
- [x] MacBook Pro agent connected
- [x] Python alert notifier querying the Elasticsearch API
- [x] Modular Python architecture
- [x] Three severity tier runners
- [x] HTML email with severity charts and MITRE breakdown
- [x] Fail2Ban integration
- [x] Real CVE detected and remediated (CVE-2026-26066)
- [x] Credentials secured with python-dotenv
- [x] Published to GitHub
- [ ] Cron job scheduling
- [ ] SMS alerting via Twilio
- [ ] Custom Wazuh detection rules
- [ ] Suricata network traffic analysis
- [ ] JavaScript custom dashboard
- [ ] Windows endpoint agent
- [ ] Home server integration
- [ ] VPN monitoring
```
## Versions

**v3.0 — In Development**
- Daily recap email — 24-hour lookback summary sent at 8PM PST
- Dedicated recap orchestrator (daily_recap.py), separate from live alert runners
- Dedicated recap HTML formatter (recap_formatter.py) with expanded sections
- Top 10 most important alerts with full detail — rule level, MITRE technique, tactic, compliance frameworks
- Complete MITRE ATT&CK summary — total techniques detected with full breakdown and bar chart
- Fail2Ban activity section — total bans, banned IPs, affected agents, timestamps
- Network activity section — port changes, new connections, listened ports
- Active agents summary — all reporting agents with 24-hour alert counts
- Remaining alert activity — everything outside the top 10 summarized by rule and count
- Scheduler (scheduler.py) with a simple ENABLED toggle for on/off control
- 8PM PST automated scheduling via the schedule library
- Scheduler logging to logs/scheduler.log
- HTML email template extracted to templates/email_template.html
- Cron job for automated scheduled reporting
- Suricata for network traffic analysis
- Custom Wazuh detection rules

**v2.0 — May 2026**
- Modular Python architecture — config, elasticsearch_client, 
  formatter, email_reporter, utility
- Three severity tier runners — critical (12-15), high (7-11), all (1+)
- Master runner (run.py) executes all three in sequence
- Fully redesigned HTML email with Gmail-compatible table layout
- Severity breakdown cards matching the Wazuh rule level scale
- CSS horizontal bar chart for MITRE ATT&CK techniques
- Technique: color-coded bubbles in alert details
- UTC to local time conversion for all timestamps
- Active agents list with lookback window context
- Fail2Ban integration for automated SSH ban detection
- Credentials secured with python-dotenv

**v1.0 — May 2026**
- Wazuh + ELK stack deployed via Docker
- Ubuntu VM and MacBook Pro monitored
- Single Python script querying the Elasticsearch API
- Plain text email delivery via Gmail SMTP
- Real CVE detected and remediated (CVE-2026-26066)

## References

**Infrastructure:**
- [Wazuh Documentation](https://documentation.wazuh.com)
- [Wazuh Docker Deployment](https://documentation.wazuh.com/current/deployment-options/docker/wazuh-container.html)
- [Wazuh GitHub](https://github.com/wazuh/wazuh-docker)
- [Wazuh Agent Enrollment](https://documentation.wazuh.com/current/user-manual/agent/agent-enrollment/index.html)
- [Docker Documentation](https://docs.docker.com)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [UTM Virtualization](https://docs.getutm.app)
- [Ubuntu Server ARM64](https://cdimage.ubuntu.com/releases/22.04/release/)
- [Fail2Ban Documentation](https://www.fail2ban.org/wiki/index.php/Main_Page)
- [Fail2Ban GitHub](https://github.com/fail2ban/fail2ban)
- [Fail2Ban — Wazuh Integration](https://documentation.wazuh.com/current/user-manual/capabilities/active-response/default-active-response-scripts.html)
- [LightDM Display Manager](https://wiki.ubuntu.com/LightDM)
- [XFCE Desktop Environment](https://www.xfce.org)

**ELK Stack:**
- [Elasticsearch REST API](https://www.elastic.co/guide/en/elasticsearch/reference/current/rest-apis.html)
- [Elasticsearch Query DSL](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html)
- [Elasticsearch Range Query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-range-query.html)
- [Elasticsearch Python Client](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html)
- [Kibana Documentation](https://www.elastic.co/guide/en/kibana/current/index.html)
- [Logstash Documentation](https://www.elastic.co/guide/en/logstash/current/index.html)

**Security Frameworks:**
- [MITRE ATT&CK Framework](https://attack.mitre.org)
- [MITRE ATT&CK — Brute Force T1110](https://attack.mitre.org/techniques/T1110/)
- [MITRE ATT&CK — Sudo Caching T1548.003](https://attack.mitre.org/techniques/T1548/003/)
- [MITRE ATT&CK — Password Guessing T1110.001](https://attack.mitre.org/techniques/T1110/001/)
- [NVD — National Vulnerability Database](https://nvd.nist.gov)
- [CVE Database](https://cve.mitre.org)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [NIST 800-53 Controls](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
- [CVE-2026-26066 Advisory](https://github.com/advisories/GHSA-v994-63cg-9wj3)
- [PCI DSS Standards](https://www.pcisecuritystandards.org)
- [HIPAA Security Rule](https://www.hhs.gov/hipaa/for-professionals/security/index.html)
- [GDPR Official Text](https://gdpr-info.eu)

**Python Libraries:**
- [Requests](https://docs.python-requests.org)
- [urllib3](https://urllib3.readthedocs.io)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [smtplib](https://docs.python.org/3/library/smtplib.html)
- [email.mime](https://docs.python.org/3/library/email.mime.html)
- [datetime](https://docs.python.org/3/library/datetime.html)
- [json](https://docs.python.org/3/library/json.html)
- [schedule](https://schedule.readthedocs.io)

**Email Development:**
- [Gmail SMTP Settings](https://support.google.com/mail/answer/7126229)
- [Gmail App Passwords](https://support.google.com/accounts/answer/185833)
- [HTML Email Compatibility — Can I Email](https://www.caniemail.com)
- [HTML Email Best Practices](https://www.litmus.com/blog/html-email-best-practices)
- [Gmail CSS Support](https://developers.google.com/gmail/design/css)

**Desktop Environment:**
- [XFCE](https://www.xfce.org)
- [LightDM GTK Greeter](https://github.com/Xubuntu/lightdm-gtk-greeter)
- [Oh My Zsh](https://ohmyz.sh)
- [Neofetch](https://github.com/dylanaraps/neofetch)
- [Terminator Terminal](https://gnome-terminator.org)
- [Firefox for Linux](https://www.mozilla.org/en-US/firefox/linux/)

**Git & GitHub:**
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- [Git Stash](https://git-scm.com/docs/git-stash)
- [Git Rebase](https://git-scm.com/docs/git-rebase)

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
- [r/netsec](https://reddit.com/r/netsec)
- [Wazuh Community](https://wazuh.com/community)
- [ServeTheHome](https://www.servethehome.com)

[@HunterBFranklin](https://github.com/HunterBFranklin) — MIT License
