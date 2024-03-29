import requests


def url(endpoint: str) -> str:
    return f"https://gaps.heig-vd.ch/{endpoint}"


def fetch_html(
    endpoint: str, session_id: str, params: dict = None, data: dict = None
) -> str:

    req = requests.get(
        url(endpoint),
        headers={
            "User-Agent": "Mozilla/5.0 (Linux x86_64)",
            "Accept": "*/*",
        },
        cookies={"GAPSSESSID": session_id},
        #    data=data,
        #    params=params,
    )

    return req.text
