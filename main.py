import requests
import pyttsx3
import tkinter as tk
from tkinter import messagebox
import schedule
import time
import threading
from playsound import playsound


# Get weather alerts from NWS API
def get_weather_alerts():
    url = 'https://api.weather.gov/alerts/active/area/FL'  # Modify for your area
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Parse and process the weather alerts
def parse_alerts(data):
    if data and 'features' in data:
        for alert in data['features']:
            event = alert['properties']['event']
            severity = alert['properties']['severity']
            description = alert['properties']['description']
            headline = alert['properties']['headline']
            handle_alert(event, description)

# Show popup with the alert info
def show_popup(message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning("Weather Alert", message)

# Speak the alert using TTS
def speak_alert(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Handle alert by showing a popup and TTS
def handle_alert(event, description):
    playsound("Whoop.mp3")
    message = f"Weather Alert: {event}\nDescription: {description}"
     # Create and start threads for popup and TTS
    t1 = threading.Thread(target=show_popup, args=(message,))
    t2 = threading.Thread(target=speak_alert, args=(message,))
    
    t1.start()  # Start the popup
    t2.start()  # Start the TTS
    
    # Wait for both threads to finish
    t1.join()
    t2.join()

# Job to periodically check for alerts
def job():
    data = get_weather_alerts()
    parse_alerts(data)

# Schedule the job every 5 minutes
schedule.every(5).minutes.do(job)

# Main loop to run the scheduled jobs
while True:
    print("Checking for weather alerts...")
    data = get_weather_alerts()
    parse_alerts(data)
    print("Pausing for 5 minutes...")
    time.sleep(300)
    schedule.run_pending()
    time.sleep(1)
