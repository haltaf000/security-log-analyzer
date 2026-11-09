import csv
failed_attempts = {}

with open("login_logs.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        if row["status"] == "FAILED":
            ip = row["ip_address"]
            failed_attempts[ip] = failed_attempts.get(ip, 0) + 1


print(failed_attempts)

for ip, count in failed_attempts.items():
    if count >= 3:
        print(f"ALERT: Suspicious IP {ip} - {count} failed login attempts")