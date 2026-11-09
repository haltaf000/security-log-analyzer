import csv

from detector import is_suspicious

failed_attempts = {}

with open("login_logs.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        if row["status"] == "FAILED":
            ip = row["ip_address"]
            failed_attempts[ip] = failed_attempts.get(ip, 0) + 1


print(failed_attempts)

alerts = []

for ip, count in failed_attempts.items():
    if is_suspicious(count):
        message = f"ALERT: Suspicious IP {ip} - {count} failed login attempts"
        alerts.append(message)
        print(message)

from pathlib import Path

report_dir = Path("reports")
report_dir.mkdir(exist_ok=True)

with open(report_dir / "security_report.txt", "w") as file:
    if alerts:
        for alert in alerts:
            file.write(alert + "\n")
    else:
        file.write("No suspicious login activity detected.\n")