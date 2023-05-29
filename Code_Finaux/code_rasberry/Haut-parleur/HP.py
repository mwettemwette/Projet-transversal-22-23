import RPi.GPIO as GPIO
from pygame import mixer

# Set up the GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)

# Load the WAV file
mixer.init()
mixer.music.load("Scripts\HP\bonjour.wav")

# Play the WAV file through the GPIO pin
GPIO.output(26, GPIO.HIGH)
mixer.music.play()
while mixer.music.get_busy():
    continue
GPIO.output(26, GPIO.LOW)

# Clean up the GPIO pin and pygame
GPIO.cleanup()
mixer.quit()
