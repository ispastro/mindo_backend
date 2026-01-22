"""
Ping Script to Keep Render Service Awake

This script pings your deployed API every 10 minutes to prevent it from sleeping.
Run this on your local machine or use a cron job service like cron-job.org

Usage:
    python ping_service.py
"""

import requests
import time
from datetime import datetime

# Replace with your actual Render URL
API_URL = "https://your-app-name.onrender.com/ping"

# Ping interval in seconds (10 minutes = 600 seconds)
PING_INTERVAL = 600

def ping_server():
    """Ping the server and print the response"""
    try:
        response = requests.get(API_URL, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ [{datetime.now()}] Ping successful: {data}")
        else:
            print(f"⚠️ [{datetime.now()}] Ping failed with status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ [{datetime.now()}] Error pinging server: {e}")

if __name__ == "__main__":
    print(f"🚀 Starting ping service for {API_URL}")
    print(f"⏰ Pinging every {PING_INTERVAL // 60} minutes")
    print("Press Ctrl+C to stop\n")
    
    while True:
        ping_server()
        time.sleep(PING_INTERVAL)
