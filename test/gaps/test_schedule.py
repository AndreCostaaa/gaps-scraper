import os
import unittest

from gaps.login import login
from gaps.schedule import fetch_classes, fetch_current_schedule


@unittest.skip("This is not a unit test.")
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

    @unittest.skip("This is not a unit test.")
    def test_fetch(self):
        classes = fetch_classes(self.session_id)
        print(classes)

    @unittest.skip("This is not a unit test.")
    def test_fetch_schedule(self):
        schedule = fetch_current_schedule(self.session_id)
        print(schedule.classes)



if __name__ == "__main__":
    unittest.main()
