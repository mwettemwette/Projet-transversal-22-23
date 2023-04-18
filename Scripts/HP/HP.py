import RPi.GPIO as GPIO
import pygame

# Set up the GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)

# Load the WAV file
pygame.mixer.init()
pygame.mixer.music.load("Scripts\HP\test.wav")

# Play the WAV file through the GPIO pin
GPIO.output(26, GPIO.HIGH)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    continue
GPIO.output(26, GPIO.LOW)

# Clean up the GPIO pin and pygame
GPIO.cleanup()
pygame.mixer.quit()
