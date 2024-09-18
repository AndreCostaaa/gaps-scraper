import os
import requests

from app_types.grades import Grade
from notifier.api_notification import send_api_notification


class GapsNotifierHandler:
    def __init__(self):
        self.url = os.environ.get("GAPS_NOTIFIER_URL", "")
        if not self.url:
            return
        if self.url[-1] == "/":
            self.url = self.url[:-1]
        self.user_id = None
        try:
            self.user_id = int(os.environ.get("GAPS_NOTIFIER_USER_ID", ""))
        except ValueError:
            pass

        self.access_token = os.environ.get("GAPS_NOTIFIER_TOKEN", None)
        if self.access_token is None:
            self.access_token = self.fetch_gaps_notifier_access_token()
        else:
            self.access_token = self.access_token.replace("Bearer ", "")

    def build_url(self, path: str) -> str:
        return f"{self.url}/api/{path}"

    def fetch_gaps_notifier_access_token(self) -> str:
        req = requests.post(self.build_url("token"), json={"user_id": self.user_id})
        if req.status_code != 200:
            return ""
        return req.json()["access_token"]

    def send_notification_to_gaps_notifier(self, grade: Grade) -> bool:
        if not self.url or not self.access_token:
            return False

        data = grade.to_dict()
        data["class_average"] = float(data["class_average"])
        status_code = send_api_notification(
            self.build_url("grade"), self.access_token, data
        )

        return status_code == 201 or status_code == 409
