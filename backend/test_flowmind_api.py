import requests
import time


BASE_URL = "http://127.0.0.1:8000"


def print_response(title, response):

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    print("Status:", response.status_code)

    try:
        print(response.json())

    except Exception:
        print(response.text)


# ================================================================
# 1. STATUS
# ================================================================

response = requests.get(
    f"{BASE_URL}/api/traffic/status"
)

print_response(
    "INITIAL STATUS",
    response
)


# ================================================================
# 2. START VIDEO
# ================================================================

response = requests.post(
    f"{BASE_URL}/api/traffic/start",
    params={
        "source":
            "data/videos/traffic.mp4"
    }
)

print_response(
    "START TRAFFIC",
    response
)


# ================================================================
# 3. WAIT FOR PROCESSING
# ================================================================

print(
    "\nWaiting for FlowMind to process video..."
)

time.sleep(15)


# ================================================================
# 4. STATE
# ================================================================

response = requests.get(
    f"{BASE_URL}/api/traffic/state"
)

print_response(
    "CURRENT TRAFFIC STATE",
    response
)


# ================================================================
# 5. FORECAST
# ================================================================

response = requests.get(
    f"{BASE_URL}/api/traffic/forecast"
)

print_response(
    "TRAFFIC FORECAST",
    response
)


# ================================================================
# 6. RECOMMENDATION
# ================================================================

response = requests.get(
    f"{BASE_URL}/api/traffic/recommendation"
)

print_response(
    "SIGNAL RECOMMENDATION",
    response
)


# ================================================================
# 7. STATUS AGAIN
# ================================================================

response = requests.get(
    f"{BASE_URL}/api/traffic/status"
)

print_response(
    "FINAL STATUS",
    response
)