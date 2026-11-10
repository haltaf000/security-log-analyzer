# Security Log Analyzer

Security Log Analyzer is a Python command-line application that identifies repeated failed login attempts in CSV-formatted authentication logs. It aggregates failures by IP address, flags addresses with three or more failed attempts, and writes the results to a text report.

The repository includes sample data, unit tests, a Docker image, and a Docker Compose configuration. The current implementation processes a local CSV file; it does not collect or monitor live authentication events.

## Features

- Parses login records using Python's standard `csv` library.
- Aggregates failed login attempts by source IP address.
- Generates an alert when an IP address has **three or more** failed attempts.
- Writes detection results to `reports/security_report.txt`.
- Provides unit tests for the detection threshold.
- Supports local execution and containerized execution with Docker Compose.

## Detection logic

The application reads `login_logs.csv`, filters records with a `FAILED` status, and counts those events by IP address. The detection rule in `detector.py` determines whether each count meets the alert threshold.

For the included sample data, the report contains:

```text
ALERT: Suspicious IP 192.168.1.20 - 5 failed login attempts
```

If no IP address meets the threshold, the report states that no suspicious login activity was detected.

## Repository contents

| Path | Description |
| --- | --- |
| `app.py` | CSV processing, alert generation, and report output |
| `detector.py` | Failed-login threshold evaluation |
| `test_detector.py` | Unit tests for the detection rule |
| `login_logs.csv` | Simulated authentication events |
| `Dockerfile` | Container image definition and runtime user configuration |
| `compose.yaml` | Analyzer service and report bind mount |
| `.gitignore` | Exclusions for local files and generated artifacts |

Generated reports are stored in `reports/`, which is excluded from version control.

## Getting started

### Local execution

**Requirements:** Python 3 and Git. The Docker image uses Python 3.12. No third-party Python dependencies are required.

```powershell
git clone https://github.com/haltaf000/security-log-analyzer.git
cd security-log-analyzer
python app.py
```

Run the unit tests:

```powershell
python -m unittest -v
```

### Docker Compose

**Requirements:** Docker with Compose support.

```powershell
docker compose build
docker compose run --rm analyzer
```

The Compose service mounts the local `./reports` directory at `/app/reports`. Generated reports therefore remain available on the host after the container exits.

To view the report in PowerShell:

```powershell
Get-Content .\reports\security_report.txt
```

The analyzer is a single-run process and does not expose any network ports.

## Container security

The Dockerfile applies two runtime and dependency measures:

- **Dependency update:** Upgrades `pip` during the image build.
- **Least privilege:** Creates an `appuser` account and runs the application as a non-root user. The account was verified with UID `1000` in the built container.

### Trivy vulnerability assessment

Scan the Compose-built image with:

```powershell
trivy image security-log-analyzer-analyzer:latest
```

The following results were recorded in **November 2026**:

| Scan category | Initial image | After pip upgrade |
| --- | ---: | ---: |
| Debian packages | 189 | 189 |
| pip | 6 | 0 |
| Additional Python-package findings | 0 | 3 |
| **Total findings** | **195** | **192** |

The updated image contained `pip 26.3`, with no vulnerabilities reported against pip itself. Trivy also reported three Python-package findings and warned that third-party SBOM data may affect vulnerability detection. Those findings require separate validation; they have not been established as either exploitable issues or false positives.

The Debian scan continued to report **189 findings**, including **49 HIGH** and **0 CRITICAL**. These issues remain open for assessment and remediation. Non-root execution limits process privileges but does not eliminate vulnerabilities in installed packages.

Scan results are a point-in-time record and may change as the base image and vulnerability databases are updated.

## Scope and next steps

The current implementation uses simulated CSV data and a fixed threshold in the application workflow. It does not provide real-time log ingestion, correlation across systems, or automatic incident response.

Planned enhancements include configurable detection settings, support for additional log formats, automated tests and image scans in GitHub Actions, and continued review of base-image vulnerabilities.

