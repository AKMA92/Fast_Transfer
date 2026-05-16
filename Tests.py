import unittest
from SearchLogic import SearchLogic


class TestSearchLogic(unittest.TestCase):

    def setUp(self):
        self.search = SearchLogic()

    # Normal Case -> normale Zeit wird korrekt umgerechnet
    def test_time_to_minutes(self):
        result = self.search.time_to_minutes("06:30:00")
        self.assertEqual(result, 390)

    # Edge Case -> None anstelle Zeit übergeben
    def test_time_to_minutes_none(self):
        result = self.search.time_to_minutes(None)
        self.assertEqual(result, None)

    # Edge Case -> falsches Zeitformat abc wird übergene
    def test_time_to_minutes_wrong_format(self):
        result = self.search.time_to_minutes("abc")
        self.assertEqual(result, None)

    # Failure Case -> absichtlich falscher Wert erwartet
    def test_time_to_minutes_error(self):
        with self.assertRaises(AssertionError):
            result = self.search.time_to_minutes("06:30:00")
            self.assertEqual(result, 400)

    ###############################################################################

    # Normal Case -> existierende Station wird gefunden
    # 8506000 = Winterthur
    def test_find_stop_id_Winterthur(self):
        result = self.search.find_stop_id("Winterthur")
        self.assertEqual(result, "8506000")

    # Failure Case -> Station existiert nicht
    def test_find_stop_id_not_found(self):
        result = self.search.find_stop_id("ErfundeneStation")
        self.assertEqual(result, None)

    ###############################################################################

    # Failure Case -> ungültige Zeit wird übergeben
    # abc anstelle Zeit zBsp 00:30:30 übergeben
    def test_invalid_time_connection(self):
        result = self.search.find_connection_by_names(
            "Winterthur",
            "Zürich HB",
            "Bern",
            "01.01.2026",
            "abc",
            False
        )
        self.assertEqual(result, ["Ungültige Zeit. Erwartetes Format: HH:MM:SS"])

    # Failure Case -> Station existiert nicht
    # FalscheStation wird nicht gefunden da nicht existiert
    def test_station_not_found_connection(self):
        result = self.search.find_connection_by_names(
            "FalscheStation",
            "Zürich HB",
            "Bern",
            "01.01.2026",
            "06:30:00",
            False
        )
        self.assertEqual(result, ["Mindestens eine Station wurde nicht gefunden."])

if __name__ == "__main__":
    unittest.main()