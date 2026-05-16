import unittest
from SearchLogic import SearchLogic


class TestSearchLogic(unittest.TestCase):

    def setUp(self):
        self.search = SearchLogic()

    def test_time_to_minutes(self):
        result = self.search.time_to_minutes("06:30:00")
        self.assertEqual(result, 390)

    def test_time_to_minutes_none(self):
        result = self.search.time_to_minutes(None)
        self.assertEqual(result, None)

    def test_time_to_minutes_wrong_format(self):
        result = self.search.time_to_minutes("abc")
        self.assertEqual(result, None)

    # 8506000 = Winterthur
    def test_find_stop_id_Winterthur(self):
        result = self.search.find_stop_id("Winterthur")
        self.assertEqual(result, "8506000")

    def test_find_stop_id_not_found(self):
        result = self.search.find_stop_id("ErfundeneStation")
        self.assertEqual(result, None)

    def test_time_to_minutes_error(self):
        with self.assertRaises(AssertionError):
            result = self.search.time_to_minutes("06:30:00")
            self.assertEqual(result, 400)




if __name__ == "__main__":
    unittest.main()