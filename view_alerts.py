import json

ALERT_FILE = "alerts.json"

with open(ALERT_FILE, "r") as file:
    alerts = json.load(file)

if not alerts:
    print("No alerts found.")
else:
    print("\nConsentShield Alert History\n")
    print("=" * 50)

    for index, alert in enumerate(alerts, start=1):
        print(f"Alert #{index}")
        print(f"Upload File: {alert['upload_file']}")
        print(f"Risk Level: {alert['risk']}")
        print(f"Matched With: {alert['matched_with']}")
        print(f"Strong Hash Matches: {alert['strong_count']}")
        print(f"Possible Hash Matches: {alert['possible_count']}")
        print(f"Timestamp: {alert['timestamp']}")
        print("-" * 50)