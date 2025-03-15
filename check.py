# import pyttsx3

# engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# for voice in voices:
#     print(voice.id)

import pygame

pygame.mixer.init()
sound = pygame.mixer.Sound("audio.mp3")
sound.play()
while pygame.mixer.get_busy():
    pygame.time.wait(100)
sound.stop()