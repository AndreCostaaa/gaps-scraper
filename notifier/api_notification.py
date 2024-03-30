import requests


def send_api_notification(url: str, access_token: str, data: dict) -> int:
    req = requests.post(
        url,
        json=data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    return req.status_code
