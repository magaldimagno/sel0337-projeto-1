"""
Checkpoint 2 - Controle de intensidade de um LED com PWM
Eduardo Magaldi Magno - 15448780
Lucas Garcia Pereira - 15496307
"""

import RPi.GPIO as GPIO
import time

# Configuração inicial
pin = 18
GPIO.setmode(GPIO.BCM) 
GPIO.setup(pin, GPIO.OUT)

# Configurando o PWM no pino escolhido com frequência inicial de 100 Hz
pwm_led = GPIO.PWM(pin, 100) 

# Iniciando o PWM com duty cycle em 0%
pwm_led.start(0)

try:
# Loop principal que aumenta e diminui o duty cycle do PWM, controlando a intensidade do LED. O delay de 5 segundos é para permitir a visualização da mudança de intensidade do LED.
        print("Iniciando controle de PWM.")
        while True:                                                        
                for i in range(0, 101, 10):
                        print("\nDuty Cycle: "+str(i))
                        pwm_led.ChangeDutyCycle(i)
                        time.sleep(5)
                for i in range(100, -1, -10):
                        print("\nDuty Cycle: "+str(i))
                        pwm_led.ChangeDutyCycle(i)
                        time.sleep(5)

except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário.")
finally:
        pwm_led.stop()
        GPIO.cleanup()
                                                                                                                                        