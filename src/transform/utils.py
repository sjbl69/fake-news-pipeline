from datetime import datetime

def normalize_date(date_str: str) -> str:
    try:
        return datetime.fromisoformat(date_str.replace("Z", "")).isoformat()
    except:
        return None