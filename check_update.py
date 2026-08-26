import hashlib
import json
import os
from datetime import datetime, timezone


HASH_FILE = "profiles_hash.json"
UPDATE_FILE = "update.json"

FILES = {
    "noads": "noads.txt",
    "stable": "stable.txt",
    "gaming": "gaming.txt",
    "other": "other.txt"
}


def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def load_json(path, default):
    if not os.path.exists(path):
        return default

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# Load old data
old_hashes = load_json(
    HASH_FILE,
    {
        "noads": "",
        "stable": "",
        "gaming": "",
        "other": ""
    }
)

update_data = load_json(
    UPDATE_FILE,
    {
        "version": 1,
        "updated": False,
        "message": "",
        "time": ""
    }
)


# Calculate new hashes
new_hashes = {}

changed = False

for name, file in FILES.items():
    if not os.path.exists(file):
        print(f"Missing file: {file}")
        continue

    new_hash = sha256_file(file)
    new_hashes[name] = new_hash

    if old_hashes.get(name) != new_hash:
        changed = True
        print(f"Changed: {name}")


# Update version if something changed
if changed:

    update_data["version"] = update_data.get("version", 1) + 1
    update_data["updated"] = True
    update_data["message"] = "New configs update available"
    update_data["time"] = datetime.now(
        timezone.utc
    ).isoformat()

    print(
        "New update detected. Version:",
        update_data["version"]
    )

else:
    update_data["updated"] = False
    update_data["message"] = "No updates"

    print("No changes detected")


# Save new state
save_json(HASH_FILE, new_hashes)
save_json(UPDATE_FILE, update_data)
