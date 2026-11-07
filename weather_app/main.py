"""Command-line weather app powered by the OpenWeather API."""

from __future__ import annotations

import os
import sys
import time
from datetime import datetime
from typing import Any

import requests
from dotenv import load_dotenv

BASE_URL = "https://api.openweathermap.org/data/2.5"
REQUEST_TIMEOUT = 10
CACHE_SECONDS = 600

# Small in-memory cache to avoid repeatedly using the free API allowance.
_cache: dict[tuple[str, str], tuple[float, dict[str, Any]]] = {}


def load_api_key() -> str | None:
    """Load the API key from .env / environment variables."""
    load_dotenv()
    key = os.getenv("OPENWEATHER_KEY", "").strip()
    return key or None


def fetch_json(endpoint: str, city: str, api_key: str) -> dict[str, Any] | None:
    """Request an OpenWeather endpoint and return JSON, or None on failure."""
    cache_key = (endpoint, city.casefold())
    cached = _cache.get(cache_key)
    now = time.time()
    if cached and now - cached[0] < CACHE_SECONDS:
        return cached[1]

    url = f"{BASE_URL}/{endpoint}"
    params = {"q": city, "appid": api_key, "units": "metric"}

    try:
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        if response.status_code == 404:
            print(f"City not found: {city}. Check the spelling and try again.")
            return None
        if response.status_code == 401:
            print("OpenWeather rejected the API key (401). Check your .env key.")
            print("A newly created key can take a little time to become active.")
            return None
        if response.status_code == 429:
            print("API request limit reached. Please wait before trying again.")
            return None
        response.raise_for_status()
        data = response.json()
        _cache[cache_key] = (now, data)
        return data
    except requests.exceptions.Timeout:
        print("The weather service took too long to respond. Try again.")
    except requests.exceptions.ConnectionError:
        print("Could not connect. Check your internet connection.")
    except requests.exceptions.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else "unknown"
        print(f"OpenWeather API error (HTTP {status}).")
    except requests.exceptions.RequestException as exc:
        print(f"Network/request error: {exc}")
    except ValueError:
        print("The weather service returned invalid JSON.")
    return None


def get_current_weather(city: str, api_key: str) -> dict[str, Any] | None:
    return fetch_json("weather", city, api_key)


def get_forecast(city: str, api_key: str) -> dict[str, Any] | None:
    return fetch_json("forecast", city, api_key)


def display_current(data: dict[str, Any]) -> None:
    """Print the current conditions, using safe lookups for JSON fields."""
    main = data.get("main") or {}
    weather_items = data.get("weather") or [{}]
    weather = weather_items[0] if weather_items else {}
    wind = data.get("wind") or {}

    print("\n" + "=" * 48)
    print(f" WEATHER IN {data.get('name', 'Unknown').upper()}")
    print("=" * 48)
    temp = main.get("temp")
    feels_like = main.get("feels_like")
    humidity = main.get("humidity")
    print(f"Temperature : {temp if temp is not None else 'N/A'} °C")
    print(f"Feels like  : {feels_like if feels_like is not None else 'N/A'} °C")
    print(f"Humidity    : {humidity if humidity is not None else 'N/A'}%")
    print(f"Conditions  : {weather.get('description', 'N/A').title()}")
    print(f"Wind speed  : {wind.get('speed', 'N/A')} m/s")
    print("=" * 48)


def display_forecast(data: dict[str, Any]) -> None:
    """Display one forecast item per date, choosing the item nearest noon."""
    entries = data.get("list") or []
    by_date: dict[str, tuple[float, dict[str, Any]]] = {}

    for item in entries:
        timestamp = item.get("dt")
        if not timestamp:
            continue
        date_time = datetime.fromtimestamp(timestamp)
        date_key = date_time.strftime("%Y-%m-%d")
        distance_from_noon = abs(
            date_time.hour * 60 + date_time.minute - (12 * 60)
        )
        current = by_date.get(date_key)
        if current is None or distance_from_noon < current[0]:
            by_date[date_key] = (distance_from_noon, item)

    print("\n5-DAY FORECAST")
    print("-" * 68)
    print(f"{'DATE':<14} {'TEMP':<12} {'CONDITION'}")
    print("-" * 68)
    for date_key in sorted(by_date)[:5]:
        item = by_date[date_key][1]
        main = item.get("main") or {}
        weather_items = item.get("weather") or [{}]
        weather = weather_items[0] if weather_items else {}
        temp = main.get("temp", "N/A")
        description = weather.get("description", "N/A").title()
        print(f"{date_key:<14} {str(temp) + ' °C':<12} {description}")
    if not by_date:
        print("Forecast information is unavailable.")
    print("-" * 68)


def run() -> None:
    api_key = load_api_key()
    if not api_key:
        print("API key not found.")
        print("Create a .env file from .env.example and add your OpenWeather key.")
        return

    print("Welcome to the Live Weather App!")
    print("Enter a city name to see current weather and a 5-day forecast.")
    print("Press Enter on an empty city name to exit.\n")

    while True:
        try:
            city = input("City: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not city:
            print("Goodbye!")
            break

        current = get_current_weather(city, api_key)
        if current is None:
            continue
        display_current(current)

        forecast = get_forecast(city, api_key)
        if forecast is not None:
            display_forecast(forecast)


if __name__ == "__main__":
    run()
