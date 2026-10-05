"""
Checkpoint 1 - Botão
Eduardo Magaldi Magno - 15448780
Lucas Garcia Pereira - 15496307
"""

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) # desabilita avisos
GPIO.setup(23, GPIO.OUT)
def button(pin):
    if GPIO.input(pin):
        print("released")
        GPIO.output(23, False)
    else:
        print("pressed")
        GPIO.output(23, True)
GPIO.setup(24, GPIO.IN, GPIO.PUD_UP)
GPIO.add_event_detect(24, GPIO.BOTH, callback=button, bouncetime=200)
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário.")
    finally:
        print("Limpando configurações do GPIO.")
        GPIO.cleanup()
