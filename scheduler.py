import schedule
import time
import sqlite3
from weather_data import fetch_weather_data, kelvin_to_celsius, check_alerts, update_daily_summary, store_daily_summary, CITIES, daily_summary

def schedule_weather_fetching():
    schedule.every(5).minutes.do(fetch_weather_updates)

    while True:
        schedule.run_pending()
        time.sleep(1)

def fetch_weather_updates():
    # Open a new connection to the SQLite database
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

    # Close the database connection after storing data
    conn.close()

if __name__ == "__main__":
    # Start scheduling the weather data fetching every 5 minutes
    schedule_weather_fetching()
