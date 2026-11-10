# Security Log Analyzer

A Python-based security project that analyzes simulated login events, identifies repeated failed login attempts by IP address, and generates a security report.

This project demonstrates Python scripting, unit testing, containerization with Docker and Docker Compose, and image vulnerability scanning with Trivy.

## Features

- Reads login events from a CSV file.
- Counts failed login attempts for each IP address.
- Flags IP addresses with **3 or more** failed attempts.
- Saves alerts to a text report.
- Includes unit tests for the detection threshold.
- Runs locally or in a Docker container.
- Uses Docker Compose to save reports on the host through a bind mount.
- Runs the application as a non-root Linux user (`appuser`).

## How It Works

1. `app.py` reads `login_logs.csv`.
2. It counts rows with a `FAILED` login status, grouped by IP address.
3. `detector.py` checks whether the number of failed attempts meets the threshold (default: `3`).
4. The application prints alerts and writes them to `reports/security_report.txt`.
5. If no IP address meets the threshold, the report indicates that no suspicious login activity was detected.

### Example Alert

```text
ALERT: Suspicious IP 192.168.1.20 - 5 failed login attempts
```

The sample data is simulated and is intended for learning and testing.

## Project Structure

```text
security-log-analyzer/
├── app.py
├── detector.py
├── test_detector.py
├── login_logs.csv
├── Dockerfile
├── compose.yaml
├── .gitignore
└── README.md
```

| File | Purpose |
| --- | --- |
| `app.py` | Reads logs, counts failed attempts, and writes the report. |
| `detector.py` | Implements the failed-login threshold check. |
| `test_detector.py` | Tests the threshold logic with Python's `unittest`. |
| `login_logs.csv` | Provides simulated login events. |
| `Dockerfile` | Builds the Python application image. |
| `compose.yaml` | Builds and runs the analyzer and mounts the reports directory. |
| `.gitignore` | Excludes local-only files and generated reports from Git. |

The `reports/` directory is generated when the application runs and is not committed to Git.

## Requirements

For local execution:

- Python 3.12 (the version used in the Docker image), or another compatible Python 3 version.

For containerized execution:

- Docker with Docker Compose support (for example, Docker Desktop).

For security scanning:

- Trivy.

No additional third-party Python libraries are required by the application.

## Getting Started

Clone the repository and enter the project folder:

```powershell
git clone https://github.com/haltaf000/security-log-analyzer.git
cd security-log-analyzer
```

### Run Locally

```powershell
python app.py
```

View the generated report in PowerShell:

```powershell
Get-Content .\reports\security_report.txt
```

### Run Unit Tests

```powershell
python -m unittest -v
```

The tests check counts below, equal to, and above the detection threshold.

### Run with Docker Compose

Build the image:

```powershell
docker compose build
```

Run the analyzer as a one-off container:

```powershell
docker compose run --rm analyzer
```

Read the report on the host:

```powershell
Get-Content .\reports\security_report.txt
```

Docker Compose bind-mounts the local `./reports` folder to `/app/reports` inside the container. This keeps the report accessible after the container exits. No ports are required because the analyzer is a batch application, not a web server.

## Container Security

### Non-Root Execution

The Docker image creates a dedicated Linux user named `appuser` and runs the application as that user rather than as root.

You can verify the identity with:

```powershell
docker compose run --rm analyzer id
```

The tested image returned `uid=1000(appuser)`, confirming non-root execution. This reduces privileges but does not eliminate security risk.

### Trivy Vulnerability Scanning

Scan the image created by Docker Compose:

```powershell
trivy image security-log-analyzer-analyzer:latest
```

The following results are from development scans in **November 2026**:

| Finding | Before pip upgrade | After pip upgrade |
| --- | ---: | ---: |
| Debian OS package findings | 189 | 189 |
| pip package findings | 6 | 0 |
| Other Python package / embedded SBOM findings | 0 | 3 |
| **Total reported findings** | **195** | **192** |

The image was updated from pip `25.0.1` to `26.3`. The updated scan reported no vulnerabilities against pip itself, but it reported three Python package findings associated with embedded SBOM data. Trivy warned that third-party SBOM data may affect detection accuracy.

**Important:** The scan still reported **189 Debian OS package findings**, including **49 HIGH** findings, and **0 CRITICAL** findings for Debian. The remaining findings have not all been remediated or assessed for exploitability. The three Python findings also require verification; they should not automatically be treated as exploitable or false positives.

Scan results can change when base images, packages, or vulnerability databases are updated.

## Limitations

- The application processes a local, simulated CSV file rather than live authentication logs.
- The detection rule uses a simple failed-attempt threshold; it does not evaluate timing or account context.
- Container security work is ongoing, and known vulnerability findings remain.

## Future Improvements

- Add configurable detection thresholds.
- Support additional log formats and larger datasets.
- Add GitHub Actions to run tests and security scans automatically.
- Continue reviewing and reducing relevant container vulnerabilities.

## Technologies Used

- Python and `unittest`
- Docker and Docker Compose
- Trivy
- Git and GitHub
