# ConsentShield

ConsentShield is a privacy-first image protection prototype that helps detect possible non-consensual sharing of protected images using perceptual hashing.

## Why This Project Matters

Non-consensual sharing of personal or sensitive images can seriously harm a person's privacy, safety, and reputation. ConsentShield explores a privacy-focused way to detect whether an uploaded image is visually similar to a protected image without storing the original protected image.

## Current Features

- Protect images by generating perceptual hashes
- Store only image hashes, not original images
- Scan uploaded images against protected image hashes
- Detect strong and possible matches
- Save risky upload attempts as alerts
- View alert history

## Tech Stack

- Python
- Pillow
- ImageHash
- JSON file storage

## Project Structure

```text
ConsentShield/
├── protected_images/
├── uploads/
├── protected_hashes.json
├── alerts.json
├── protect.py
├── scan.py
├── view_alerts.py
├── .gitignore
└── README.md

## How It Works
Add images to protected_images/
Run:
python protect.py
Add test uploads to uploads/
Run:
python scan.py
View alerts:
python view_alerts.py
Privacy Approach

ConsentShield does not store the original protected images. It stores only perceptual hashes, which act like visual fingerprints.

Limitations
Hashing cannot perfectly detect heavily edited images.
Hashing cannot reliably detect fully AI-generated lookalikes.
Current version is a local prototype, not a deployed application.
Future Scope
Web dashboard
Browser extension
Email notifications
Stronger crop-resistant matching
Optional consent-based identity protection