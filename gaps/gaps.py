import requests


def url(endpoint: str) -> str:
    return f"https://gaps.heig-vd.ch/{endpoint}"


def fetch_html(
    endpoint: str,
    session_id: str,
    params: dict = None,
    data: dict = None,
    is_post: bool = False,
) -> str:
    full_url = url(endpoint)
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux x86_64)",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    cookies = {"GAPSSESSID": session_id}
    data = data
    params = params
    if is_post:
        req = requests.post(
            full_url, headers=headers, cookies=cookies, data=data, params=params
        )
    else:
        req = requests.get(
            full_url, headers=headers, cookies=cookies, data=data, params=params
        )
    return req.text
