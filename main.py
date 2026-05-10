from PIL import Image
import imagehash
import json
import os

IMAGE_FOLDER = "protected_images"
JSON_FILE = "protected_hashes.json"

# Load existing hashes
with open(JSON_FILE, "r") as file:
    hashes = json.load(file)

# Get names of already saved images
saved_images = [item["image_name"] for item in hashes]

# Go through every file in protected_images folder
for filename in os.listdir(IMAGE_FOLDER):
    image_path = os.path.join(IMAGE_FOLDER, filename)

    # Only process image files
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):

        # Avoid saving same image again and again
        if filename in saved_images:
            print(f"{filename} already protected. Skipping.")
            continue

        image = Image.open(image_path)
        hash_value = str(imagehash.phash(image))

        data = {
            "image_name": filename,
            "hash": hash_value
        }

        hashes.append(data)
        print(f"{filename} protected successfully.")

# Save updated hashes
with open(JSON_FILE, "w") as file:
    json.dump(hashes, file, indent=4)

print("Protection database updated.")