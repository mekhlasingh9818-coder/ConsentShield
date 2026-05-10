from PIL import Image
import imagehash
import json
import os

PROTECTED_FOLDER = "protected_images"
JSON_FILE = "protected_hashes.json"

def generate_hashes(image_path):
    image = Image.open(image_path)

    return {
        "phash": str(imagehash.phash(image)),
        "dhash": str(imagehash.dhash(image)),
        "whash": str(imagehash.whash(image)),
        "ahash": str(imagehash.average_hash(image))
    }

# Load existing hashes
with open(JSON_FILE, "r") as file:
    hashes = json.load(file)

saved_images = [item["image_name"] for item in hashes]

# Protect new images
for filename in os.listdir(PROTECTED_FOLDER):

    image_path = os.path.join(PROTECTED_FOLDER, filename)

    if filename.lower().endswith((".jpg", ".jpeg", ".png")):

        if filename in saved_images:
            print(f"{filename} already protected.")
            continue

        image_hashes = generate_hashes(image_path)

        data = {
            "image_name": filename,
            "hashes": image_hashes
        }

        hashes.append(data)

        print(f"{filename} protected successfully.")

# Save updated hashes
with open(JSON_FILE, "w") as file:
    json.dump(hashes, file, indent=4)

print("\nProtection database updated.")