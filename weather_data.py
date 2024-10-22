import requests
from datetime import datetime
import sqlite3
import logging
import time

logging.basicConfig(level=logging.INFO)

API_KEY = 'ab42b2cd580123d1b8d8dff5be95e00f'
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'
FETCH_INTERVAL = 300

def fetch_weather_data(city):
    """
    Fetch weather data for the given city from OpenWeatherMap API.

    Args:
        city (str): The name of the city to fetch weather data for.

    Returns:
        dict: JSON response containing weather data, or None if there was an error.
    """

    try:
        response = requests.get(BASE_URL, params={'q': city, 'appid': API_KEY})
        response.raise_for_status()  # Raises an error for 4xx or 5xx responses
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data for {city}: {e}")
        return None
    
def kelvin_to_celsius(kelvin):
    return kelvin - 273.15


daily_summary = {}

def update_daily_summary(city, weather_data):
    date = datetime.fromtimestamp(weather_data['dt']).date()
    temp = kelvin_to_celsius(weather_data['main']['temp'])
    condition = weather_data['weather'][0]['main']

    if date not in daily_summary:
        daily_summary[date] = {
            'total_temp': 0,
            'count': 0,
            'max_temp': temp,
            'min_temp': temp,
            'conditions': {}
        }
    # Update daily summary
    daily_summary[date]['total_temp'] += temp
    daily_summary[date]['count'] += 1
    daily_summary[date]['max_temp'] = max(daily_summary[date]['max_temp'], temp)
    daily_summary[date]['min_temp'] = min(daily_summary[date]['min_temp'], temp)
    daily_summary[date]['conditions'][condition] = daily_summary[date]['conditions'].get(condition, 0) + 1


def setup_database():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_weather (
            city TEXT,
            date TEXT,
            average_temp REAL,
            max_temp REAL,
            min_temp REAL,
            dominant_condition TEXT
        )
    ''')
    conn.commit()
    conn.close()
    

def store_daily_summary(city, date, summary, conn):
    # Use the provided date directly since it's already in string format.
    date_str = date  # Assuming date is in 'YYYY-MM-DD' format

    avg_temp = summary['total_temp'] / summary['count'] if summary['count'] > 0 else 0
    dominant_condition = max(summary['conditions'], key=summary['conditions'].get) if summary['conditions'] else 'Clear'

    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO daily_weather (city, date, average_temp, max_temp, min_temp, dominant_condition)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (city, date_str, avg_temp, summary['max_temp'], summary['min_temp'], dominant_condition))

    conn.commit()




THRESHOLD_TEMP = 35

# Track consecutive temperature breaches
breach_counter = 0


def check_alerts(current_temp):
    if current_temp > THRESHOLD_TEMP:
        print(f"Alert: Temperature exceeds {THRESHOLD_TEMP}°C!")


if __name__ == "__main__":
    setup_database()  # Set up the database
    conn = sqlite3.connect('weather_data.db')
    
    for city in CITIES:
        weather_data = fetch_weather_data(city)
    
        if weather_data:
            temp = kelvin_to_celsius(weather_data['main']['temp'])
            check_alerts(temp)
            update_daily_summary(city, weather_data)

    for date, summary in daily_summary.items():
        for city in CITIES:
            store_daily_summary(city, date, summary, conn)


    logging.info(f"Data fetched and stored. Waiting for the next fetch in {FETCH_INTERVAL // 60} minutes...")
    time.sleep(FETCH_INTERVAL) 
    conn.close()
