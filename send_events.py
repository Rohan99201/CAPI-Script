"""
POC script: send a single test event to Meta Conversions API. Please Change the JSON payload as per Platform specific format to use for Snapchat, Tiktok

Setup:
1. Create a file called `.env` in this same folder (see .env.example for the format).
2. Add your real Pixel ID and access token to that .env file.
3. Run: pip install requests python-dotenv
4. Run: python3 send_events.py
"""

import hashlib
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()  # reads variables from a local .env file

PIXEL_ID = os.getenv("META_PIXEL_ID")
ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
TEST_EVENT_CODE = os.getenv("META_TEST_EVENT_CODE")  # optional, get from Events Manager > Test Events

if not PIXEL_ID or not ACCESS_TOKEN:
    raise EnvironmentError(
        "META_PIXEL_ID and META_ACCESS_TOKEN must be set in your .env file."
    )

GRAPH_API_VERSION = "v21.0"


def sha256(value: str) -> str:
    return hashlib.sha256(value.strip().lower().encode()).hexdigest()


def send_test_event():
    payload = {
        "data": [
            {
                "event_name": "portugal_win_today",
                "event_time": int(time.time()),
                "event_id": "poc-test-001",
                "action_source": "system_generated",
                "user_data": {
                    "em": [sha256("customer@example.com")],
                    "ph": [sha256("+15551234567")],
                },
                "custom_data": {
                    "currency": "USD",
                    "value": 149.99,
                },
            }
        ]
    }

    if TEST_EVENT_CODE:
        payload["test_event_code"] = TEST_EVENT_CODE

    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{PIXEL_ID}/events"
    resp = requests.post(url, params={"access_token": ACCESS_TOKEN}, json=payload)

    print(f"Status: {resp.status_code}")
    print(resp.json())


if __name__ == "__main__":
    send_test_event()
