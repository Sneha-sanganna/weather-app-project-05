import unittest
from unittest.mock import Mock, patch

from weather_app.main import display_forecast, display_current, fetch_json


class WeatherAppTests(unittest.TestCase):
    def test_display_current_handles_missing_fields(self):
        # The display functions should not crash when optional JSON fields are absent.
        display_current({"name": "Test City"})

    def test_display_forecast_handles_empty_list(self):
        display_forecast({"list": []})

    @patch("weather_app.main.requests.get")
    def test_fetch_json_returns_parsed_response(self, mock_get):
        response = Mock()
        response.status_code = 200
        response.json.return_value = {"name": "London"}
        response.raise_for_status.return_value = None
        mock_get.return_value = response

        result = fetch_json("weather", "London", "test-key")
        self.assertEqual(result, {"name": "London"})
        mock_get.assert_called_once()


if __name__ == "__main__":
    unittest.main()
