# Projeto 1 (Prática 3): GPIO, Python e Computação Paralela
**Disciplina:** SEL0337 - Projetos em Sistemas Embarcados
**Autores:**
- Eduardo Magaldi Magno - 15448780
- Lucas Garcia Pereira - 15496307

## Objetivo do Projeto

Este projeto tem como objetivo introduzir o desenvolvimento de software de alto nível em Python aplicado a sistemas Linux embarcados utilizando a plataforma Raspberry Pi. Ao longo das três etapas práticas, são explorados os fundamentos da linguagem (estruturas condicionais, laços de repetição, funções, *type casting*, formatação de strings e tratamento de exceções) integrados ao controle de hardware por meio do barramento GPIO (*General Purpose Input/Output*).

Em sistemas operacionais embarcados baseados em Linux, o acesso aos pinos físicos é gerenciado pelo kernel por meio de subsistemas como `sysfs` (`/sys/class/gpio`) ou `libgpiod` (`/dev/gpiochip*`), cuja complexidade é abstraída em Python pelas bibliotecas `RPi.GPIO` (controle direto de baixo nível) e `gpiozero` (interface orientada a objetos de alto nível). O escopo do projeto divide-se em três etapas principais:
- **Parte 1 (Checkpoint 1):** Configuração de ambientes virtuais (`venv`) para isolamento de dependências, leitura de entradas digitais com detecção de borda/eventos (interrupções via software) e acionamento de saídas digitais com temporização e validação de dados de entrada.
- **Parte 2 (Checkpoint 2):** Controle de saídas moduladas por largura de pulso (PWM) com análise de sinal via osciloscópio e integração prática de sensores e atuadores ao barramento GPIO.
- **Parte 3 (Checkpoint 3):** Implementação de computação concorrente e paralela em sistemas multicore utilizando processos (`multiprocessing`) e *threads* (`threading`), abordando escalonamento de tarefas, exclusão mútua (*mutex*), semáforos e prevenção de *deadlocks*.

---

## Parte 1 - Introdução à GPIO, Ambiente Virtual e Tratamento de Eventos

Nesta primeira etapa, foi configurado um ambiente virtual Python isolado (`venv`) nomeado `8007` (composto pelos dois últimos dígitos do NUSP de cada integrante da dupla) para a instalação restrita das bibliotecas `RPi.GPIO` e `gpiozero`. Em seguida, foram desenvolvidos dois scripts utilizando o esquema de numeração `GPIO.BCM` (canais do System-on-Chip da Broadcom):
1. **`blink.py`:** Acionamento de um LED a partir do estado de um botão (*push button*) configurado com resistor de *pull-up* interno e detecção assíncrona de eventos de borda (`GPIO.add_event_detect`), evitando o uso de *polling* contínuo na CPU.
2. **`counter.py`:** Temporizador de contagem regressiva via terminal com validação de entrada do usuário (*type casting* e tratamento de exceções com `try-except ValueError`), formatação dinâmica na mesma linha (`MM:SS`) e acionamento de saída digital ao final da contagem.

### Mapeamento de Hardware

| Componente                | Pino RASP                       | Função                                                                                     |
|---------------------------|---------------------------------|--------------------------------------------------------------------------------------------|
| LED Vermelho (+ Resistor) | `GPIO 23` (Pino Físico 16)      | Saída digital (`GPIO.OUT`) acionada pelo botão ou pelo término da contagem regressiva.     |
| Botão (*Push Button*)     | `GPIO 24` (Pino Físico 18)      | Entrada digital (`GPIO.IN`) configurada com resistor de *pull-up* interno (`GPIO.PUD_UP`). |
| GND (Terra)               | `Ground` (Pinos Físicos 6 e 14) | Referência comum (0 V) para o cátodo do LED e para o terminal do botão.                    |

### Códigos

#### 1. Acionamento de LED por Botão (`blink.py`)

```python
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
    # Com Pull-Up ativo: nível ALTO (True) = solto | nível BAIXO (False) = pressionado
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
    # Mantém o programa principal ativo aguardando os eventos de borda
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    # Trata a interrupção por teclado (CTRL+C) de forma segura
    print("\nPrograma interrompido pelo usuário.")
finally:
    # Libera e reseta os pinos GPIO antes de encerrar o script
    print("Limpando configurações do GPIO.")
    GPIO.cleanup()
```

#### 2. Contagem Regressiva com Validação de Entrada (`counter.py`)

```python
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
            
            # Verifica se o valor inserido é positivo
            if tempo_segundos < 0:
                print("Erro: O número deve ser positivo. Tente novamente.")
                continue
            break
            
        except ValueError:
            # Captura erro caso o usuário digite caracteres não numéricos ou valores não inteiros
            print("Erro: O valor digitado deve ser um número inteiro. Tente novamente.")

    # Executa a contagem regressiva passando o parâmetro validado
    executar_contagem(tempo_segundos)

if __name__ == "__main__":
    try:
        # Garante que o LED inicie apagado
        GPIO.output(pin_led, False)
        main()
    except KeyboardInterrupt:
        # Tratamento da interrupção via teclado (CTRL+C)
        print("\nPrograma interrompido pelo usuário.")
    finally:
        # Desconecta e limpa as configurações das portas GPIO utilizadas
        print("Limpando configurações do GPIO.")
        GPIO.cleanup()
```

### Evidências - Histórico de Comandos

```bash
HISTÓRICO DE COMANDOS - CHECKPOINT 1
Eduardo Magaldi Magno - 15448780
Lucas Garcia Pereira - 15496307

===========================================

python --version
sudo apt install python3-venv -y
python3 -m venv 8007
source 8007/bin/activate
cd 8007
pip freeze
pip3 install gpiozero RPi.GPIO
pip freeze
python
quit()
nano blink.py
python blink.py
nano counter.py
python counter.py
deactivate
history | tail -n 20 > historico.txt
```

---

## Parte 2 - 

### Mapeamento de Hardware
| Componente        | Pino RASP | Função                                                  |
|-------------------|-----------|---------------------------------------------------------|

### Códigos

### Evidências - Fotos do Osciloscópio

---

## Parte 3 - 

### Mapeamento de Hardware
| Componente        | Pino RASP | Função                                                  |
|-------------------|-----------|---------------------------------------------------------|

### Códigos

### Evidência - Vídeo do Funcionamento
