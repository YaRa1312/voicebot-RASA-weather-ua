import speech_recognition as sr
import requests
import time
import pyttsx3
from gtts import gTTS
from playsound import playsound
import pygame
import os


RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook"
SENDER_ID = "user"

pygame.mixer.init()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Слухаю... Скажіть ваш запит (наприклад, 'Яка погода в Києві сьогодні?')")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="uk-UA")
        print(f"Ви сказали: {text}")
        return text
    except sr.UnknownValueError:
        print("Не вдалося розпізнати мову.")
        return None
    except sr.RequestError as e:
        print(f"Помилка сервісу розпізнавання: {e}")
        return None

def send_to_rasa(message, file_counter):
    payload = {
        "sender": SENDER_ID,
        "message": message
    }
    response = requests.post(RASA_API_URL, json=payload)
    if response.status_code == 200:
        for msg in response.json():
            text = msg['text']
            print(f"Бот: {text}")
            if "°C" in text:
                audio_file = f"response_{file_counter}.mp3"
                tts = gTTS(text=text, lang='uk', slow=False)
                tts.save(audio_file)
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                pygame.mixer.music.stop()
                try:
                    os.remove(audio_file)
                except PermissionError:
                    pass
    else:
        print("Помилка зв’язку з Rasa.")


def main():
    print("Переконайтеся, що Rasa сервер запущено командою 'rasa run'!")
    file_counter = 0
    while True:
        message = recognize_speech()
        if message:
            send_to_rasa(message, file_counter)
            file_counter += 1
        time.sleep(1)
        