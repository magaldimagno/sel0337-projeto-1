"""
Checkpoint 3 - Mutex
Eduardo Magaldi Magno - 15448780
Lucas Garcia Pereira - 15496307
"""

import RPi.GPIO as GPIO
import threading
import time

PINO_LED = 23
PINO_BOTAO = 24
PINO_BUZZER = 25

frequencia_rapida = False
mutex = threading.Lock()

def callback_fim_contagem():
    print("\n[Callback] A contagem de tempo foi finalizada!\n")

def thread_contagem():
    """Loop contínuo que pede o input, realiza a contagem e recomeça."""
    while True:
        # Loop de validação de entrada isolado na thread
        while True:
            try:
                entrada = input("Digite o tempo da contagem em segundos: ")
                tempo_total = int(entrada)
                if tempo_total < 0:
                    print("Erro: O número deve ser positivo. Tente novamente.")
                    continue
                break
            except ValueError:
                print("Erro: O valor digitado deve ser um número inteiro. Tente novamente.")

        # Executa a contagem regressiva
        for tempo_restante in range(tempo_total, -1, -1):
            minutos, segundos = divmod(tempo_restante, 60)
            tempo_formatado = '{:02d}:{:02d}'.format(minutos, segundos)
            print(f"Tempo restante: {tempo_formatado}    ", end='\r')
            time.sleep(1)
        
        GPIO.output(PINO_BUZZER, True)
        time.sleep(2)
        GPIO.output(PINO_BUZZER, False)
        callback_fim_contagem()

def thread_botao():
    """Monitora o botão via software na thread, contornando o bug de interrupção."""
    global frequencia_rapida
    estado_anterior = GPIO.input(PINO_BOTAO)
    
    while True:
        estado_atual = GPIO.input(PINO_BOTAO)
        
        if estado_anterior == GPIO.HIGH and estado_atual == GPIO.LOW:
            with mutex:
                frequencia_rapida = not frequencia_rapida
                
            estado = "Rápida" if frequencia_rapida else "Lenta"
            print(f"\n[Interrupção] Frequência alterada para: {estado}\n")
            time.sleep(0.3)
            
        estado_anterior = estado_atual
        time.sleep(0.05)

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(PINO_LED, GPIO.OUT)
    GPIO.setup(PINO_BUZZER, GPIO.OUT)
    GPIO.setup(PINO_BOTAO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # Inicia a thread do botão
    t_botao = threading.Thread(target=thread_botao)
    t_botao.daemon = True
    t_botao.start()

    # Inicia a thread da contagem (agora independente de argumentos iniciais)
    t_contagem = threading.Thread(target=thread_contagem)
    t_contagem.daemon = True
    t_contagem.start()
    
    try:
        print("\nBlink iniciado. Pressione o botão para alterar a frequência. CTRL+C para sair.\n")
        
        # O programa principal fica apenas responsável por manter o LED piscando
        while True:
            with mutex:
                delay = 0.1 if frequencia_rapida else 0.5
            
            GPIO.output(PINO_LED, True)
            time.sleep(delay)
            GPIO.output(PINO_LED, False)
            time.sleep(delay)
            
    except KeyboardInterrupt:
        print("\nEncerrando o programa...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()