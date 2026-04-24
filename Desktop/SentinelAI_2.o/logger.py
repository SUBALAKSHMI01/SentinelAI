import json
from datetime import datetime
import os

LOG_FILE = "logs.json"


# ✅ Ensure file exists
def init_log_file():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)


# ✅ Add log
def log_event(event: dict):
    init_log_file()

    event["timestamp"] = datetime.now().isoformat()

    with open(LOG_FILE, "r") as f:
        logs = json.load(f)

    logs.append(event)

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)


# ✅ Get logs (role-based)
def get_logs(role: str, user_id: str = None):
    init_log_file()

    with open(LOG_FILE, "r") as f:
        logs = json.load(f)

    if role == "admin":
        return logs

    elif role == "employee":
        return [log for log in logs if log.get("user_id") == user_id]

    return []