import unittest
import os


from gaps.schedule import fetch_schedule
from gaps.login import login


class TestScheduleFetching(unittest.TestCase):

    session_id: str
    user_id: str

    @classmethod
    def setUpClass(cls) -> None:
        session_id, cls.user_id = login(
            os.getenv("GAPS_USERNAME"), os.getenv("GAPS_PASSWORD")
        )
        if not session_id:
            raise Exception("Couldn't login")
        cls.session_id = session_id

    def test_fetch(self):
        classes = fetch_schedule(self.session_id)
        print(classes)


if __name__ == "__main__":
    unittest.main()
