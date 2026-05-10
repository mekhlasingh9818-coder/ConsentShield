from PIL import Image
import imagehash
import json
import os
from datetime import datetime

UPLOAD_FOLDER = "uploads"
JSON_FILE = "protected_hashes.json"
ALERT_FILE = "alerts.json"

def generate_hashes(image_path):
    image = Image.open(image_path)

    return {
        "phash": str(imagehash.phash(image)),
        "dhash": str(imagehash.dhash(image)),
        "whash": str(imagehash.whash(image)),
        "ahash": str(imagehash.average_hash(image))
    }

def compare_hashes(upload_hashes, protected_hashes):
    scores = {}

    for hash_type in ["phash", "dhash", "whash", "ahash"]:
        upload_hash = imagehash.hex_to_hash(upload_hashes[hash_type])
        protected_hash = imagehash.hex_to_hash(protected_hashes[hash_type])

        difference = upload_hash - protected_hash
        scores[hash_type] = int(difference)

    return scores

def save_alert(upload_file, result):
    with open(ALERT_FILE, "r") as file:
        alerts = json.load(file)

    alert = {
        "upload_file": upload_file,
        "risk": result["risk"],
        "matched_with": result["matched_with"],
        "strong_count": result["strong_count"],
        "possible_count": result["possible_count"],
        "scores": result["scores"],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    alerts.append(alert)

    with open(ALERT_FILE, "w") as file:
        json.dump(alerts, file, indent=4)

with open(JSON_FILE, "r") as file:
    hashes = json.load(file)

print("\nScanning uploads...\n")

for upload_file in os.listdir(UPLOAD_FOLDER):
    upload_path = os.path.join(UPLOAD_FOLDER, upload_file)

    if upload_file.lower().endswith((".jpg", ".jpeg", ".png")):

        upload_hashes = generate_hashes(upload_path)

        print("=" * 50)
        print(f"Upload Checked: {upload_file}")

        best_result = {
            "risk": "SAFE",
            "matched_with": None,
            "strong_count": 0,
            "possible_count": 0,
            "scores": {}
        }

        for protected in hashes:
            scores = compare_hashes(upload_hashes, protected["hashes"])

            strong_matches = 0
            possible_matches = 0

            for score in scores.values():
                if score <= 8:
                    strong_matches += 1
                elif score <= 20:
                    possible_matches += 1

            if strong_matches >= 2:
                risk = "STRONG MATCH"
            elif strong_matches >= 1 and possible_matches >= 1:
                risk = "POSSIBLE MATCH"
            elif possible_matches >= 2:
                risk = "POSSIBLE MATCH"
            else:
                risk = "SAFE"

            if risk == "STRONG MATCH":
                best_result = {
                    "risk": risk,
                    "matched_with": protected["image_name"],
                    "strong_count": strong_matches,
                    "possible_count": possible_matches,
                    "scores": scores
                }
                break

            elif risk == "POSSIBLE MATCH" and best_result["risk"] == "SAFE":
                best_result = {
                    "risk": risk,
                    "matched_with": protected["image_name"],
                    "strong_count": strong_matches,
                    "possible_count": possible_matches,
                    "scores": scores
                }

        print(f"Risk Level: {best_result['risk']}")

        if best_result["matched_with"]:
            print(f"Matched With: {best_result['matched_with']}")
            print(f"Strong Hash Matches: {best_result['strong_count']}")
            print(f"Possible Hash Matches: {best_result['possible_count']}")
            print(f"Hash Scores: {best_result['scores']}")
        else:
            print("No protected image match found.")

        if best_result["risk"] != "SAFE":
            save_alert(upload_file, best_result)
            print("Alert saved.")

        print("=" * 50)