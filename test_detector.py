import unittest
from detector import is_suspicious


class TestDetector(unittest.TestCase):

    def test_detection_threshold(self):
        self.assertFalse(is_suspicious(2))
        self.assertTrue(is_suspicious(3))
        self.assertTrue(is_suspicious(5))


if __name__ == "__main__":
    unittest.main()