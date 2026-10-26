"""
Checkpoint 1 - Botão
Eduardo Magaldi Magno - 15448780
Lucas Garcia Pereira - 15496307
"""

import RPi.GPIO as GPIO
import time

# Define o padrão de numeração dos pinos como Broadcom SOC (BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # Desabilita avisos de pinos já configurados

# Configura o pino GPIO 23 como saída digital para controlar o LED
GPIO.setup(23, GPIO.OUT)

# Função de callback executada automaticamente ao detectar mudança de estado no botão
def button(pin):
    # Como o botão está em Pull-Up: nível ALTO (True) = solto | nível BAIXO (False) = pressionado
    if GPIO.input(pin):
        print("released")
        GPIO.output(23, False)  # Apaga o LED ao soltar o botão
    else:
        print("pressed")
        GPIO.output(23, True)   # Acende o LED ao pressionar o botão

# Configura o pino GPIO 24 como entrada digital ativando o resistor de Pull-Up interno
GPIO.setup(24, GPIO.IN, GPIO.PUD_UP)

# Registra a detecção de eventos em ambas as bordas (subida e descida) com debounce de 200 ms
GPIO.add_event_detect(24, GPIO.BOTH, callback=button, bouncetime=200)

try:
    # Mantém o programa principal ativo aguardando interrupções de hardware/eventos
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    # Trata a interrupção por teclado (CTRL+C) de forma segura
    print("\nPrograma interrompido pelo usuário.")
finally:
    # Libera e reseta os pinos GPIO para o estado seguro padrão antes de encerrar
    print("Limpando configurações do GPIO.")
    GPIO.cleanup()
