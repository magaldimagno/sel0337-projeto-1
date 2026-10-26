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

### Códigos - Arquitetura e Lógica de Implementação

#### 1. Acionamento de LED por Botão (`blink.py`)
Para evitar o uso bloqueante de *polling* contínuo na CPU, a leitura do botão e o acionamento do LED foram implementados por meio de interrupções de borda gerenciadas via software.

- **Configuração em *Pull-Up* e Lógica Invertida:** O pino `GPIO 24` foi configurado com o resistor de *pull-up* interno habilitado (`GPIO.PUD_UP`), mantendo nível lógico alto (`True`) com a chave aberta e caindo para nível lógico baixo (`False`) quando pressionada ao GND. Na função de *callback*, essa leitura é avaliada de forma complementar para acender o LED (`GPIO 23`) no pressionamento e apagá-lo na soltura.
- **Detecção Assíncrona e Filtro de *Debounce*:** A função `GPIO.add_event_detect` monitora ambas as bordas de transição (`GPIO.BOTH`) e dispara a rotina `button(pin)` apenas quando há mudança de estado físico. Foi aplicado um parâmetro `bouncetime=200` (200 ms) para filtrar trepidações mecânicas do contato (*bouncing*).
- **Liberação Segura de Recursos (*Cleanup*):** O laço principal é protegido por uma estrutura `try-except KeyboardInterrupt` associada ao bloco `finally`. Ao encerrar o programa via `CTRL+C`, o método `GPIO.cleanup()` reseta os pinos utilizados para alta impedância, prevenindo curtos-circuitos em execuções futuras.

#### 2. Contagem Regressiva com Validação de Entrada (`counter.py`)
O sistema solicita ao usuário um tempo em segundos via terminal, realiza a validação de integridade da entrada e executa um cronômetro regressivo antes de acionar a saída digital do LED.

- **Validação de Entrada e *Type Casting*:** Como a leitura via `input()` retorna uma string, o dado é convertido para inteiro (`int()`) dentro de um bloco `try-except ValueError`. Entradas alfanuméricas ou valores de ponto flutuante são interceptados sem interromper a execução do script, enquanto uma estrutura condicional rejeita números negativos.
- **Decomposição de Tempo e Sobrescrita em Linha:** Na função modularizada `executar_contagem()`, o tempo restante é dividido em minutos e segundos em uma única operação via `divmod(tempo_restante, 60)` e formatado na máscara `{:02d}:{:02d}`. Para evitar o empilhamento de linhas no terminal a cada ciclo de `time.sleep(1)`, utilizou-se o retorno de carro (`end='\r'`) na função `print()`, sobrescrevendo dinamicamente a mesma linha até o disparo final do LED em `00:00`.

### Evidências - Histórico de Comandos
Abaixo está o registro dos comandos utilizados para criação e ativação do ambiente virtual isolado `8007` (formado pelos dígitos finais dos NUSPs da dupla), instalação local dos pacotes `gpiozero` e `RPi.GPIO` e execução dos scripts:

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
