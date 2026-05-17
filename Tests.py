import unittest
from SearchLogic import SearchLogic


class TestSearchLogic(unittest.TestCase):

    def setUp(self):
        self.search = SearchLogic()
        self.search.load_csv()

    # Normal Case
    def test_time_to_minutes(self):
        result = self.search.time_to_minutes("06:30:00")
        self.assertEqual(result, 390)

    # Edge Case
    def test_time_to_minutes_none(self):
        result = self.search.time_to_minutes(None)
        self.assertIsNone(result)

    # Edge Case
    def test_time_to_minutes_wrong_format(self):
        result = self.search.time_to_minutes("abc")
        self.assertIsNone(result)

    # Failure Case
    def test_time_to_minutes_error(self):
        result = self.search.time_to_minutes("06:30:00")
        self.assertNotEqual(result, 400)

    # Normal Case
    def test_find_stop_ids_winterthur(self):
        result = self.search.find_stop_ids("Winterthur")
        self.assertIsNotNone(result)
        self.assertIn("8506000", result)

    # Edge Case mit Leerzeichen
    def test_find_stop_ids_with_spaces(self):
        result = self.search.find_stop_ids(" Winterthur ")
        self.assertIsNotNone(result)
        self.assertIn("8506000", result)

    # Failure Case
    def test_find_stop_ids_not_found(self):
        result = self.search.find_stop_ids("ErfundeneStation")
        self.assertIsNone(result)

    # Failure Case ungültige Zeit
    def test_invalid_time_connection(self):
        result = self.search.find_connection_by_names(
            "Winterthur",
            "Zürich HB",
            "Bern",
            "01.01.2026",
            "abc",
            False
        )
        self.assertEqual(
            result,
            ["Ungültige Zeit. Erwartetes Format: HH:MM:SS"]
        )

    # Failure Case Station existiert nicht
    def test_station_not_found_connection(self):
        result = self.search.find_connection_by_names(
            "FalscheStation",
            "Zürich HB",
            "Bern",
            "01.01.2026",
            "06:30:00",
            False
        )
        self.assertEqual(
            result,
            ["Mindestens eine Station wurde nicht gefunden."]
        )

    # Normal Case Verbindungssuche gibt Liste zurück
    def test_connection_returns_list(self):
        result = self.search.find_connection_by_names(
            "Winterthur",
            "Zürich HB",
            "Bern",
            "01.01.2026",
            "06:30:00",
            False
        )
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)


if __name__ == "__main__":
    unittest.main()