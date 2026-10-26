"""
Checkpoint 1 - Contador
Eduardo Magaldi Magno - 15448780
Lucas Garcia Pereira - 15496307
"""

import RPi.GPIO as GPIO
import time

# Configuração do pino do LED utilizando numeração BCM
pin_led = 23
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin_led, GPIO.OUT)

def executar_contagem(tempo_total):
    # Laço de repetição decrescente de tempo_total até 0 (passo -1)
    for tempo_restante in range(tempo_total, -1, -1):
        # Calcula o quociente (minutos) e o resto da divisão por 60 (segundos)
        minutos, segundos = divmod(tempo_restante, 60)
        # Formata os valores no padrão MM:SS com dois dígitos preenchidos com zero
        tempo_formatado = '{:02d}:{:02d}'.format(minutos, segundos)
        # Atualiza a exibição na mesma linha do terminal usando retorno de carro (\r)
        print(f"Tempo restante: {tempo_formatado}", end='\r')
        # Base de tempo de 1 segundo para a contagem regressiva
        time.sleep(1)

    # Ao término da contagem, exibe mensagem final e aciona a saída do LED
    print("\nContagem finalizada! LED aceso.")
    GPIO.output(pin_led, True)
    time.sleep(2)

def main():
    # Laço de validação da entrada do usuário
    while True:
        try:
            entrada = input("Digite o tempo da contagem em segundos: ")

            # Type casting da string de entrada para número inteiro
            tempo_segundos = int(entrada)
            
            # Verifica se o valor inserido é um tempo válido (não negativo)
            if tempo_segundos < 0:
                print("Erro: O número deve ser positivo. Tente novamente.")
                continue
            break
            
        except ValueError:
            # Captura erro caso o usuário digite letras, símbolos ou números de ponto flutuante
            print("Erro: O valor digitado deve ser um número inteiro. Tente novamente.")

    # Chama a função de contagem passando o parâmetro devidamente validado
    executar_contagem(tempo_segundos)

if __name__ == "__main__":
    try:
        # Garante que o LED inicie apagado antes do começo da contagem
        GPIO.output(pin_led, False)
        main()
    except KeyboardInterrupt:
        # Tratamento da interrupção via teclado (CTRL+C)
        print("\nPrograma interrompido pelo usuário.")
    finally:
        # Desconecta e limpa as configurações das portas GPIO utilizadas
        print("Limpando configurações do GPIO.")
        GPIO.cleanup()
