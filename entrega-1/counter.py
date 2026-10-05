"""
Checkpoint 1 - Contador
Eduardo Magaldi Magno - 15448780
Lucas Garcia Pereira - 15496307
"""

import RPi.GPIO as GPIO
import time

# Configuração do pino do LED
pin_led = 23
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin_led, GPIO.OUT)

def executar_contagem(tempo_total):
    for tempo_restante in range(tempo_total, -1, -1):
        minutos, segundos = divmod(tempo_restante, 60)
        tempo_formatado = '{:02d}:{:02d}'.format(minutos, segundos)
        print(f"Tempo restante: {tempo_formatado}", end='\r')
        time.sleep(1)

    print("\nContagem finalizada! LED aceso.")
    GPIO.output(pin_led, True)
    time.sleep(2)

def main():
    while True:
        try:
            entrada = input("Digite o tempo da contagem em segundos: ")

            tempo_segundos = int(entrada)
            
            if tempo_segundos < 0:
                print("Erro: O número deve ser positivo. Tente novamente.")
                continue
            break
            
        except ValueError:
            print("Erro: O valor digitado deve ser um número inteiro. Tente novamente.")

    executar_contagem(tempo_segundos)

if __name__ == "__main__":
    try:
        GPIO.output(pin_led, False)
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário.")
    finally:
        print("Limpando configurações do GPIO.")
        GPIO.cleanup()