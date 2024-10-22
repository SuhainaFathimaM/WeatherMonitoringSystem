import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime

def fetch_daily_summaries():
    """Fetch daily weather summaries from the database."""
    try:
        conn = sqlite3.connect('weather_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM daily_weather')
        summaries = cursor.fetchall()
        return summaries
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        conn.close()

def plot_daily_summary():
    """Plot the daily average temperature from the fetched summaries."""
    summaries = fetch_daily_summaries()
    
    # Validate if summaries are not empty
    if not summaries:
        print("No data available to plot.")
        return
    
    # Adjusted indices to skip 'city' and only get 'date' and 'average_temp'
    dates = [datetime.strptime(summary[1], '%Y-%m-%d') for summary in summaries]  # Now uses the second element for the date
    avg_temps = [summary[2] for summary in summaries]  # Now uses the third element for the temperature

    # Ensure that the data is valid for plotting
    if len(dates) != len(avg_temps):
        print("Mismatch in data lengths. Cannot plot.")
        return

    # Plotting
    plt.figure(figsize=(10, 5))  # Set the figure size
    plt.plot(dates, avg_temps, marker='o', linestyle='-', color='b')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Average Temperature (°C)', fontsize=12)
    plt.title('Daily Average Temperature', fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(True)  # Add grid for better readability
    plt.tight_layout()  # Adjust layout
    plt.savefig('temperature_trend.png')  # Save the plot as a PNG file
    plt.show()

if __name__ == "__main__":
    plot_daily_summary()
