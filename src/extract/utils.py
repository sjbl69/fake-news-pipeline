import requests


def is_valid_image(url):
    """
    Vérifie si une URL pointe vers une image valide
    """
    try:
        response = requests.head(url, timeout=5)
        content_type = response.headers.get("Content-Type", "")
        return response.status_code == 200 and "image" in content_type
    except Exception:
        return False