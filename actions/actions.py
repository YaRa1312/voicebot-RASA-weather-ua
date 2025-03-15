from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os


load_dotenv()
API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

WEATHER_DESCRIPTION_TRANSLATIONS = {
    # Thunderstorm (Гроза)
    "thunderstorm with light rain": "гроза з легким дощем",
    "thunderstorm with rain": "гроза з дощем",
    "thunderstorm with heavy rain": "гроза з сильним дощем",
    "light thunderstorm": "легка гроза",
    "thunderstorm": "гроза",
    "heavy thunderstorm": "сильна гроза",
    "ragged thunderstorm": "нерівна гроза",
    "thunderstorm with light drizzle": "гроза з легкою мрякою",
    "thunderstorm with drizzle": "гроза з мрякою",
    "thunderstorm with heavy drizzle": "гроза з сильною мрякою",

    # Drizzle (Мряка)
    "light intensity drizzle": "легка мряка",
    "drizzle": "мряка",
    "heavy intensity drizzle": "сильна мряка",
    "light intensity drizzle rain": "легка мряка з дощем",
    "drizzle rain": "мряка з дощем",
    "heavy intensity drizzle rain": "сильна мряка з дощем",
    "shower rain and drizzle": "злива з мрякою",
    "heavy shower rain and drizzle": "сильна злива з мрякою",
    "shower drizzle": "коротка мряка",

    # Rain (Дощ)
    "light rain": "легкий дощ",
    "moderate rain": "помірний дощ",
    "heavy intensity rain": "сильний дощ",
    "very heavy rain": "дуже сильний дощ",
    "extreme rain": "екстремальний дощ",
    "freezing rain": "крижаний дощ",
    "light intensity shower rain": "легка злива",
    "shower rain": "злива",
    "heavy intensity shower rain": "сильна злива",
    "ragged shower rain": "нерівна злива",

    # Snow (Сніг)
    "light snow": "легкий сніг",
    "snow": "сніг",
    "heavy snow": "сильний сніг",
    "sleet": "мокрий сніг",
    "light rain and snow": "легкий дощ зі снігом",
    "rain and snow": "дощ зі снігом",
    "light shower snow": "легкий снігопад",
    "shower snow": "снігопад",
    "heavy shower snow": "сильний снігопад",

    # Atmosphere (Атмосферні явища)
    "mist": "туман",
    "smoke": "дим",
    "haze": "серпанок",
    "sand/dust whirls": "піщані/пилові вихори",
    "fog": "густий туман",
    "sand": "пісок",
    "dust": "пил",
    "volcanic ash": "вулканічний попіл",
    "squalls": "шквали",
    "tornado": "торнадо",

    # Clouds (Хмари)
    "clear sky": "ясно",
    "few clouds": "мало хмар",
    "scattered clouds": "розсіяні хмари",
    "broken clouds": "хмарно з проясненнями",
    "overcast clouds": "хмарно"
}


def get_city_names(city: str) -> str:
    """Отримує англійську назву та українську назву в називному відмінку з Geocoding API."""
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200 and response.json():
        data = response.json()[0]
        english_city = data["name"]
        nominative_city = data.get("local_names", {}).get("uk", city.capitalize())
        return english_city, nominative_city
    return city, city.capitalize()


def translate_weather_description(description: str) -> str:
    """Перекладає англійський опис погоди на українську."""
    return WEATHER_DESCRIPTION_TRANSLATIONS.get(description.lower(), description)


class ActionCurrentWeather(Action):
    def name(self) -> Text:
        return "action_current_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        original_city = tracker.get_slot("city")
        if not original_city:
            dispatcher.utter_message(text="Будь ласка, вкажіть населений пункт.")
            return []
        
        english_city, nominative_city = get_city_names(original_city)

        url = f"http://api.openweathermap.org/data/2.5/weather?q={english_city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            translated_description = translate_weather_description(description)
            message =f"{nominative_city}: {temp}°C, {translated_description}."
        else:
            message = "Не вдалося знайти погоду для цього населеного пункту. Перевірте назву."
        dispatcher.utter_message(text=message)
        return []


class ActionForecastWeather(Action):
    def name(self) -> Text:
        return "action_forecast_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        original_city = tracker.get_slot("city")
        day = tracker.get_slot("day")
        if not original_city:
            dispatcher.utter_message(text="Будь ласка, вкажіть населений пункт.")
            return []
        
        english_city, nominative_city = get_city_names(original_city)

        url = f"http://api.openweathermap.org/data/2.5/forecast?q={english_city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            forecasts = data["list"]
            target_date = self._parse_day(day)
            for forecast in forecasts:
                forecast_time = datetime.fromtimestamp(forecast["dt"])
                if forecast_time.date() == target_date:
                    temp = forecast["main"]["temp"]
                    description = forecast["weather"][0]["description"]
                    translated_description = translate_weather_description(description)
                    message = f"{nominative_city}: {temp}°C, {translated_description}."
                    dispatcher.utter_message(text=message)
                    return []
            message = f"Прогноз для цього населеного пункту на {day} недоступний."
        else:
            message = "Не вдалося знайти прогноз для цього населеного пункту."
        dispatcher.utter_message(text=message)
        return []

    def _parse_day(self, day: Text) -> datetime.date:
        today = datetime.now().date()
        day = day.lower() if day else "сьогодні"
        if "сьогодні" in day:
            return today
        elif "завтра" in day:
            return today + timedelta(days=1)
        elif "післязавтра" in day:
            return today + timedelta(days=2)
        else:
            return today
        