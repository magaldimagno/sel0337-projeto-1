"""
Checkpoint 2 - Aplicação de um sensor de distância com LED indicador
Eduardo Magaldi Magno - 15448780
Lucas Garcia Pereira - 15496307
"""

from gpiozero import DistanceSensor, LED
import time

# Inicialização dos componentes
sensor = DistanceSensor(echo=23, trigger=24) # Configuração do sensor de distância de acordo com a biblioteca e com os pinos utilizados
led = LED(18) # Configuração do LED de acordo com a biblioteca e com o pino utilizado

# O LED acende quando o sensor detecta um objeto a uma distância menor que a distância mínima configurada, que é de 50 cm por padrão 
sensor.when_in_range = led.on 
sensor.when_out_of_range = led.off

# Loop principal, que imprime a distância medida pelo sensor a cada segundo
try:
    while True:
        print("A distância é de ", sensor.distance*100, "cm") # Printando a distância, convertida para centímetros porque faz mais sentido dentro do contexto do sensor
        time.sleep(1)
except KeyboardInterrupt: 
# A biblioteca gpiozero já limpa o GPIO automaticamente quando o programa é interrompido, então não é necessário fazer isso manualmente, desde que o erro seja tratado com o KeyboardInterrupt.
    print("\nPrograma encerrado.")
