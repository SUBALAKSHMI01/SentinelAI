logs = []

def log_event(event: dict):
    logs.append(event)

def get_logs():
    return logs