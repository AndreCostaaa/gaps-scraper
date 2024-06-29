import unittest
from app_types.grades import Grade


class TestGrade(unittest.TestCase):

    def test_equals(self):

        a = Grade(
            name="te1",
            course="MAT2",
            grade="4.0",
            class_average="4.0",
            class_identifier="A",
        )
        b = Grade(
            name="te2",
            course="MAT2",
            grade="4.0",
            class_average="4.0",
            class_identifier="A",
        )
        c = Grade(
            name="te1",
            course="MAT1",
            grade="4.0",
            class_average="4.0",
            class_identifier="A",
        )
        d = Grade(
            name="te1",
            course="MAT2",
            grade="4.5",
            class_average="4.0",
            class_identifier="A",
        )
        e = Grade(
            name="te1",
            course="MAT2",
            grade="4.0",
            class_average="4.1",
            class_identifier="A",
        )
        f = Grade(
            name="te1",
            course="MAT2",
            grade="4.0",
            class_average="4.0",
            class_identifier="X",
        )

        self.assertNotEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertNotEqual(a, d)
        self.assertNotEqual(a, e)
        self.assertEqual(a, f)


if __name__ == "__main__":
    unittest.main()
