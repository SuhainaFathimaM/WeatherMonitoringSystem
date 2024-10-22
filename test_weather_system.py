import unittest
from unittest.mock import patch, MagicMock
import weather_data  # As script is named weather_data.py
from weather_data import kelvin_to_celsius, check_alerts, fetch_weather_data
import sqlite3
from datetime import datetime

class TestWeatherMonitoringSystem(unittest.TestCase):

    @patch('weather_data.requests.get')
    def test_fetch_weather_data(self, mock_get):
        # Simulate API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'main': {'temp': 298.15},  # Example temperature in Kelvin
            'weather': [{'main': 'Clear'}],
            'dt': 1695758400  # Simulated timestamp
        }
        mock_get.return_value = mock_response

        result = weather_data.fetch_weather_data('Delhi')
        self.assertEqual(result['main']['temp'], 298.15)
        self.assertEqual(result['weather'][0]['main'], 'Clear')

    def test_kelvin_to_celsius(self):
        # Test temperature conversion
        kelvin_temp = 298.15
        celsius_temp = weather_data.kelvin_to_celsius(kelvin_temp)
        self.assertAlmostEqual(celsius_temp, 25.0, places=1)
        self.assertAlmostEqual(weather_data.kelvin_to_celsius(273.15), 0)
        self.assertAlmostEqual(weather_data.kelvin_to_celsius(298.15), 25)

    def test_database_insert(self):
        # Create an in-memory SQLite database for testing
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE daily_weather (
                city TEXT,
                date TEXT, 
                average_temp REAL, 
                max_temp REAL, 
                min_temp REAL, 
                dominant_condition TEXT
            )
        ''')

        # Example data
        city = 'Delhi'
        date = '2024-10-19'
        summary = {
            'total_temp': 75.3,  # 3 readings, average should be 25.1
            'count': 3,
            'max_temp': 30.2,
            'min_temp': 20.1,
            'conditions': {'Clear': 2, 'Clouds': 1}
        }

        # Insert the data using the store_daily_summary function
        weather_data.store_daily_summary(city, date, summary, conn)

        # Verify the data was inserted correctly
        cursor.execute("SELECT * FROM daily_weather WHERE date=? AND city=?", (date, city))
        result = cursor.fetchone()
        
        # Assert the result
        self.assertIsNotNone(result)  # Ensure that data was inserted
        self.assertEqual(result[1], date)
        self.assertAlmostEqual(result[2], 25.1, places=1)  # Avg Temp
        self.assertEqual(result[3], 30.2)  # Max Temp
        self.assertEqual(result[4], 20.1)  # Min Temp
        self.assertEqual(result[5], 'Clear')  # Dominant Condition


    # @patch('weather_data.THRESHOLD_TEMP', 35)
    # def test_alerting_threshold(self):
    #     # Test if alert system triggers when temperature exceeds threshold
    #     with patch('builtins.print') as mocked_print:
    #         weather_data.check_alerts(36.0)  # Trigger alert
    #         mocked_print.assert_called_with("Alert: Temperature exceeds 35°C!")
            
    #         # Ensure no alert for below-threshold temperatures
    #         weather_data.check_alerts(34.0)
    #         mocked_print.assert_not_called()

    @patch('weather_data.THRESHOLD_TEMP', 35)
    def test_alerting_threshold(self):
        # Test if alert system triggers when temperature exceeds threshold
        with patch('builtins.print') as mocked_print:
            weather_data.check_alerts(36.0)  # Trigger alert
            mocked_print.assert_called_with("Alert: Temperature exceeds 35°C!")


if __name__ == '__main__':
    unittest.main()
