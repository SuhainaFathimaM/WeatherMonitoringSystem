# Real-Time Data Processing System for Weather Monitoring

## Overview
This project implements a real-time data processing system to monitor weather conditions and provide summarized insights using rollups and aggregates. The system continuously retrieves weather data from the [OpenWeatherMap API](https://openweathermap.org/) and processes it to generate daily summaries, alerts, and visualizations.

## Features
- Fetches weather data for major Indian metros: Delhi, Mumbai, Chennai, Bangalore, Kolkata, and Hyderabad.
- Converts temperatures from Kelvin to Celsius.
- Provides daily weather summaries with:
  - Average temperature
  - Maximum temperature
  - Minimum temperature
  - Dominant weather condition
- User-configurable temperature thresholds for alerts.
- Visualizations of daily summaries and alerts.

## Technologies Used
- Python 3.9
- SQLite for data storage
- Docker for containerization
- OpenWeatherMap API for weather data

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/WeatherMonitoringSystem.git
   cd WeatherMonitoringSystem
   
2. **Set up a virtual environment (optional but recommended):**
   ```bash
   git clone https://github.com/yourusername/WeatherMonitoringSystem.git
   cd WeatherMonitoringSystem
   ```
   
3. **Clone the repository:**
   ```bash
   pip install -r requirements.txt
   ```
   
4. **Set up the database:**
   The database will be automatically created upon running the application.

## Configuration
   Before running the application, set your OpenWeatherMap API key in the weather_data.py file:
   ```bash
   API_KEY = 'your_api_key_here'
   ```

## Running the Application
**Without Docker**
   Start the application:
   ```bash
   python src/weather_data.py
   ```
**With Docker**
1. Build the Docker image:
   ```bash
   docker build -t weather-monitoring-system .
   ```
2. Run the Docker container:
   ```bash
   docker run -d -p 80:80 weather-monitoring-system
   ```
**Testing**
The following test cases should be implemented to ensure system functionality:

1. System Setup:
  - Verify successful API connection with a valid key.
2. Data Retrieval:
  - Simulate API calls and ensure data is retrieved and parsed correctly.
3. Temperature Conversion:
  - Test temperature conversions between Kelvin, Celsius, and Fahrenheit.
4. Daily Weather Summary:
  - Verify daily summaries for multiple days.
5. Alerting Thresholds:
  - Configure thresholds and test alert triggering.



   


