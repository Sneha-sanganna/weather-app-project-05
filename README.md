# Weather App with Live OpenWeather API

A Python command-line application that retrieves live weather conditions and a
5-day forecast for a city using the OpenWeather API.

## Features

- Current temperature in Celsius, feels-like temperature, humidity, weather
  description, and wind speed.
- 5-day forecast, showing one forecast entry per date (the entry closest to noon).
- Handles unknown cities, invalid API keys, rate limits, HTTP errors, timeouts,
  connection failures, and invalid JSON.
- Reads the API key from a `.env` file rather than hard-coding it.
- Keeps successful responses in a small 10-minute in-memory cache.

## Requirements

- Python 3.10 or newer
- A free OpenWeather account and API key
- Internet connection

## Setup

1. Download or clone this project and open a terminal in its folder.
2. (Recommended) Create and activate a virtual environment:

   **Windows**
   ```powershell
   py -m venv .venv
   .venv\Scripts\activate
   ```

   **macOS / Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Create a free account at https://openweathermap.org/ and generate an API key.
5. Copy `.env.example` to a new file named `.env`.
6. Open `.env` and replace the example value:

   ```env
   OPENWEATHER_KEY=your_real_api_key_here
   ```

   Do not add quotes unless required by your environment. Never share or commit
   this key. A newly generated OpenWeather key may take some time to activate.

## Run the app

From the project root:

```bash
python -m weather_app.main
```

Enter a city name such as `London`, `Mumbai`, or `Hubballi`. Press Enter on
an empty prompt to exit.

## Project structure

```text
weather_app_project/
├── weather_app/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_weather_app.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## API endpoints used

- Current conditions: `https://api.openweathermap.org/data/2.5/weather`
- 5-day forecast: `https://api.openweathermap.org/data/2.5/forecast`

Both requests send `q` (city), `appid` (API key), and `units=metric` as query
parameters. The application uses a 10-second request timeout.

## API key security

- The real key belongs only in `.env`.
- `.env` is listed in `.gitignore`.
- `.env.example` contains a placeholder, not a working key.
- Do not upload screenshots that reveal your key, and do not paste the key into
  source code or a public repository.
- If a key is accidentally published, revoke it in your OpenWeather account
  and create a replacement.

Before pushing to GitHub, run:

```bash
git status
```

Confirm that `.env` is not listed among files to be committed.

## Troubleshooting

- **401:** Check the key in `.env`. A new key may need time to activate.
- **404:** Check the city spelling. Try adding a country code, e.g. `London,GB`.
- **429:** You may have reached the API request limit; wait and retry.
- **Network error:** Check your internet connection and try again.
- **API key not found:** Make sure the file is named exactly `.env` and is in
  the project root, beside `requirements.txt`.

## Testing checklist

Try at least five different cities, as required by the project guide. Also test
an intentionally misspelled city and verify that the app responds without
crashing.

## Submission checklist

- [ ] Upload the source code and this README to GitHub or Google Drive.
- [ ] Keep `.env` private and out of the uploaded source.
- [ ] Run the app with a real API key.
- [ ] Capture a screenshot showing real weather output.
- [ ] Include a short note explaining that the key is stored in `.env` and
      excluded through `.gitignore`.
- [ ] Share a viewable project link in the internship dashboard.

## Note

This project is a learning implementation based on the Project 05 learner guide.
The API key is not included. You must create your own key and add it to `.env`
before live requests can work.
