#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
#from ev3dev.ev3 import *
from ev3dev2.console import *
from time import sleep
import random
import sys
from ev3dev2.sound import Sound


# Olhando de Frente, o eixo da direita deve estar em cima do eixo da esquerda quando a garra astá fechada. 
# Nesse caso, para abrir a garra é utilizada uma velocidade positiva e um tempo de 0.35s
# Fechar a Garra  0.5 Ideal

# Funções ///////////////////////////////////////////////////////////////////////////////////////////////////#

def Segue_linha():

    media_direita_linha = sum(lista_ultimasLeiturasDireita[-num_amostras_segue:])/num_amostras_segue
    media_esquerda_linha = sum(lista_ultimasLeiturasEsquerda[-num_amostras_segue:])/num_amostras_segue
    if media_esquerda_linha > BrancoEq and media_direita_linha <= BrancoDr:   # Branco na esquerda e Preto na direita
        tank_drive.on(SpeedPercent(-18),SpeedPercent(33))                        # Virar pra Direita
    elif media_esquerda_linha <= BrancoEq and media_direita_linha > BrancoDr: # Preto na esquerda e Branco na direita
        tank_drive.on(SpeedPercent(33),SpeedPercent(-18))                       # Virar pra Esquerda
    elif media_esquerda_linha > BrancoEq and media_direita_linha > BrancoDr:  # Branco na esquerda e na Direita
        tank_drive.on(SpeedPercent(20), SpeedPercent(20))                       # Seguir Reto
    else:                                                                     # Preto em ambos
        if media_direita2 < MediaPretoDr and media_esquerda2 > MediaPretoEq:    # Preto na esquerda antes
            tank_drive.on(SpeedPercent(45),SpeedPercent(-25))                     # Virar para Esquerda
        elif media_esquerda2 < MediaPretoEq and media_direita2 > MediaPretoDr:  # Preto na direita antes
            tank_drive.on(SpeedPercent(-25),SpeedPercent(45))                     # Virar pra Direita
        else:                                                                   # Branco antes em ambos
            tank_drive.on(SpeedPercent(5), SpeedPercent(5))                       # Andar reto

def viu_verde():

    media_direita_verde = sum(lista_ultimasLeiturasDireita[-num_amostras_verde:])/num_amostras_verde
    media_esquerda_verde = sum(lista_ultimasLeiturasEsquerda[-num_amostras_verde:])/num_amostras_verde
    if media_direita <= 8.2:                                                                        #Foi visto verde pelo sensor direito
        tank_drive.on(SpeedPercent(0), SpeedPercent(0))
        if media_direita_verde < 35 and (len(lista_ultimasLeiturasDireita) >= num_amostras_menor):  # 35 amostras - dividindo em 35 se mostrou eficiente
            tank_drive.on_for_seconds(SpeedPercent(40), SpeedPercent(40),1)                         #Se antes do verde foi visto preto
        else:
            tank_drive.on_for_seconds(SpeedPercent(5), SpeedPercent(35),1.4)                        # Se antes do verde foi visto branco (Virar para a direita) 1.4 segundos e (5; 35) é ideal
        return True
    elif media_esquerda <= 4.8:                                                                     # Foi visto verde pelo sensor esquerdo
        tank_drive.on(SpeedPercent(0), SpeedPercent(0))
        if media_esquerda_verde < 27 and (len(lista_ultimasLeiturasEsquerda) >= num_amostras_menor):
            tank_drive.on_for_seconds(SpeedPercent(50), SpeedPercent(40),1)                         #Se antes do verde foi visto preto
        else:
            tank_drive.on_for_seconds(SpeedPercent(35), SpeedPercent(5),1.4)                        # Se antes do verde foi visto branco (Virar para a esquerda)  1.4 segundos e (35; 5) é ideal
        return True
    else:
        return False                                                                                # Não foi visto verde

def viu_verde2():
    verde_dr = 8
    verde_eq = 4
    num_identifica_verde = 3
    media_direita_verde = sum(lista_ultimasLeiturasDireita[-num_amostras_verde:])/num_amostras_verde
    media_esquerda_verde = sum(lista_ultimasLeiturasEsquerda[-num_amostras_verde:])/num_amostras_verde
    if lista_ultimasLeiturasDireita[-num_identifica_verde:] == [verde_dr]*num_identifica_verde:      # Foi visto verde pelo sensor direito
        tank_drive.on(SpeedPercent(0), SpeedPercent(0))
        time.sleep(0.1)
        if media_direita_verde < 24 and (len(lista_ultimasLeiturasDireita) >= num_amostras_menor):   # 35 amostras - dividindo em 35 se mostrou eficiente
        #Se antes do verde foi visto preto
            e = coloresquerdo.value()              
            d = colordireito.value() 
            while not (e > BrancoEq and d > BrancoDr):
                tank_drive.on(SpeedPercent(10), SpeedPercent(15))
                e = coloresquerdo.value()              
                d = colordireito.value()   
        else:
            # Se antes do verde foi visto branco 
            tank_drive.on_for_seconds(SpeedPercent(5), SpeedPercent(35),1.2)  # (Virar para a direita) 1.4 segundos e (5; 35) é ideal
        return True

    elif lista_ultimasLeiturasEsquerda[-num_identifica_verde:] == [verde_eq]*num_identifica_verde:    # Foi visto verde pelo sensor esquerdo
        tank_drive.on(SpeedPercent(0), SpeedPercent(0))
        time.sleep(0.1)
        if media_esquerda_verde < 18 and (len(lista_ultimasLeiturasEsquerda) >= num_amostras_menor):   #Se antes do verde foi visto preto
            e = coloresquerdo.value()              
            d = colordireito.value() 
            while not (e > BrancoEq and d > BrancoDr):
                tank_drive.on(SpeedPercent(10), SpeedPercent(15))
                e = coloresquerdo.value()              
                d = colordireito.value()   
        else:
            # Se antes do verde foi visto branco 
            tank_drive.on_for_seconds(SpeedPercent(35), SpeedPercent(5),1.2)  # (Virar para a esquerda)  1.4 segundos e (35; 5) é ideal
        return True
    else:
        return False #Não foi visto verde

def pegar_objeto_posicao():
    MotorGarra.on_to_position(SpeedPercent(20),PosicaoGarraAberta) # Abrir a Garra 
    time.sleep (0.5)
    MotorBraço.on_to_position(SpeedPercent(20),PosicaoBraçoAbaixado) # Descer a Garra
    time.sleep (0.5)
    MotorGarra.on_to_position(SpeedPercent(20),PosicaoGarraFechada) # Fechar a Garra 
    time.sleep (0.5)
    MotorBraço.on_to_position(SpeedPercent(20),PosicaoBraçoLevantado) # Subir a Garra0
    time.sleep (2)

def Obstaculo():
    e = coloresquerdo.value()
    d = colordireito.value()
    # Virando -------------------------------------------------------------
    tank_drive.on_for_seconds(SpeedPercent(30), SpeedPercent(0), 1.5)
    # Andando ate ver -----------------------------------------------------
    tempo = time.time() + 1.4
    while e > 40 and d > 40 and tempo > time.time():
        e = coloresquerdo.value()
        d = colordireito.value()
        tank_drive.on(SpeedPercent(25), SpeedPercent(25))
    if e < 40 or d < 40:
        return
    # Virando --------------------------------------------------------------
    tank_drive.on_for_seconds(SpeedPercent(0), SpeedPercent(30), 1.4)
    # Andando ate ver ------------------------------------------------------
    tempo = time.time() + 3
    while e > 40 and d > 40 and tempo > time.time():
        e = coloresquerdo.value()
        d = colordireito.value()
        tank_drive.on(SpeedPercent(25), SpeedPercent(25))
    if e < 40 or d < 40:
        return
    # Virando -------------------------------------------------------------
    tank_drive.on_for_seconds(SpeedPercent(0), SpeedPercent(30), 1.5)
    # Andando ate ver -----------------------------------------------------
    while e > 40 and d > 40:
        e = coloresquerdo.value()
        d = colordireito.value()
        tank_drive.on(SpeedPercent(0), SpeedPercent(0))
        return

def pegou_a_bolinha(): #Função feita para retornar a bolinha para a área de resgate depois de pegá-la
    distancia = dist.value()
    d = colordireito.value()
    e = coloresquerdo.value()
    while not (e <= 10 or d <= 15):
        distancia = dist.value()
        d = colordireito.value()
        e = coloresquerdo.value()

        lista_distancia_cima.pop(0)
        lista_distancia_cima.append(distancia)

        tank_drive.on(SpeedPercent(30), SpeedPercent(30))
        if distancia < 140: 
            tank_drive.on_for_seconds(SpeedPercent(25), SpeedPercent(-25),0.8)

    tank_drive.on(SpeedPercent(0), SpeedPercent(0))      
    tank_drive.on_for_seconds(SpeedPercent(25), SpeedPercent(25),0.6)
    tank_drive.on(SpeedPercent(0), SpeedPercent(0))     
    MotorBraço.on_for_seconds(SpeedPercent(20), tempo_braço/3) # Descendo o Braço
    MotorGarra.on_to_position(SpeedPercent(20),PosicaoGarraAberta) # Abrir a Garra 
    time.sleep(0.3)
    MotorGarra.on_to_position(SpeedPercent(20),PosicaoGarraFechada) # Fechar a Garra 
    MotorBraço.on_for_seconds(SpeedPercent(-20), tempo_braço/3) # Subindo o Braço
    tank_drive.on(SpeedPercent(-25), SpeedPercent(-25))
    tank_drive.on_for_seconds(SpeedPercent(-25), SpeedPercent(-25),1.8)
    tank_drive.on_for_seconds(SpeedPercent(25), SpeedPercent(-25),0.8)

def on_for_seconds(v1, v2, t, cond = True, random2 = False):  #Função implementada para fazer um on_for_seconds em que há a checagem durante o movimento. A condição 'cond' define se é necessária a checagem de paredes, que não é necessária na manobra do robô imediatamente depois de ver uma parede.
    aux = 0
    tentativaPegarBolinha = 0
    if random2:
        if random.randint(0, 1):
            aux = v1
            v1 = v2
            v2 = aux        
    tempo = time.time()+t
    while time.time() < tempo:
        tank_drive.on(SpeedPercent(v1), SpeedPercent(v2))
        distancia = dist.value()
        c = sensor_cor.value()
        d = colordireito.value()
        e = coloresquerdo.value()

        lista_distancia_baixo.pop(0)
        lista_distancia_cima.pop(0)
        lista_distancia_baixo.append(c)
        lista_distancia_cima.append(distancia)

        if (distancia < 140 and cond):              #Girar se ver uma parede ou se ver o chão da sala
            time.sleep(0.2)
            tank_drive.on(SpeedPercent(0), SpeedPercent(0))
            time.sleep(0.2)
            on_for_seconds(-25,-25,0.6, False)
            on_for_seconds(25,-5,2.1, False, True)
            break


        #AQUI ELE ESTÁ IDENTIFICANDO QUALQUER BOLA PARA PEGAR, IMPLEMENTAR A LÓGICA DE ESCOLHER
        #PRIMEIRO AS BOLINHAS BRANCAS
        elif 230 < c < 350 or 1050 < c < 2000 :                                                  #17:40          30 No AMbiente      35   Branco  
            tank_drive.on(SpeedPercent(0), SpeedPercent(0))
            pegar_objeto_posicao()
            print(c)
            c = sensor_cor.value()
            if c < 230:
                pegou_a_bolinha()
            else: 
                while 230 < c < 350 or 1050 < c < 2000:
                    tentativaPegarBolinha += 1
                    pegar_objeto_posicao()
                    c = sensor_cor.value()
                    if tentativaPegarBolinha >= 4:
                        tank_drive.on(SpeedPercent(0), SpeedPercent(0))
                        tank_drive.on_for_seconds(SpeedPercent(-25),SpeedPercent(-25), 0.8)
            break
        
        elif  d <50 or e <30:                                 #Se ele viu Preto
            tank_drive.on(SpeedPercent(0), SpeedPercent(0))
            tank_drive.on_for_seconds(SpeedPercent(-25),SpeedPercent(-25), 1.6)
            on_for_seconds(25,-5,2.1,True, True)
    
def Sala_Resgate():

    # num_identifica_vermelho = 3
    # vermelho_dr = 54
    # if lista_ultimasLeiturasDireita[-num_identifica_vermelho:] == [vermelho_dr]*num_identifica_vermelho:
    #     tank_drive.on(SpeedPercent(0), SpeedPercent(0))
    #     return True
    # else:
    #     return False

    while True:
        c = sensor_cor.value()
        distancia = dist.value()

        lista_distancia_baixo.pop(0)
        lista_distancia_cima.pop(0)
        lista_distancia_baixo.append(c)
        lista_distancia_cima.append(distancia)
        
        on_for_seconds(15,-15,0.9)
        on_for_seconds(-15,15,1.8)
        on_for_seconds(15,-15,0.9)
        on_for_seconds(20,20,2)

def observando_valores():
    if time.time() > tempo_do_print:
        e = coloresquerdo.value()
        d = colordireito.value()
        distancia = dist.value()
        c = sensor_cor.value()
        print("          Valores frontais:", file=sys.stderr)
        print("-------------------------------------", file=sys.stderr)
        print("Sensor Ultrassom: ", distancia, file=sys.stderr)
        print("Sensor de cor:    ", c, file=sys.stderr)
        print("-------------------------------------", file=sys.stderr)
        print(" ", file=sys.stderr)
        print("   Valores de cor do segue linha:", file=sys.stderr)
        print("-------------------------------------", file=sys.stderr)
        print("Esquerda: ", e, file=sys.stderr)
        print("Direita:  ", d, file=sys.stderr)
        print("-------------------------------------", file=sys.stderr)
        print(" ", file=sys.stderr)
        print(" ", file=sys.stderr)
        tempo_do_print = time.time() + 1

#///////////////////////////////////////////////////////////////////////////////////////////////////////////#


# Variaveis ////////////////////////////////////////////////////////////////////////////////////////////////#

# Módulos e suas portas -------------------------------------------------
MotorGarra = Motor(OUTPUT_D)
dist = UltrasonicSensor(INPUT_1)
coloresquerdo = ColorSensor(INPUT_3)
colordireito = ColorSensor(INPUT_4)
MotorBraço = Motor(OUTPUT_A)
tank_drive = MoveTank(OUTPUT_C, OUTPUT_B)  #C - Direita    B - Esquerda
sensor_cor = Sensor(INPUT_2)


# Parâmetros ------------------------------------------------------------
tempo_braço = 1                      #Tempo de subida da posição relaxada da garra para a posição abaixada
tempo_braço2 = 0.8                   # Tempo de subida/descida do braço
tempo_garra = 0.3                   # Tempo de abertura/fechamento da garra

num_amostras = 250                  # Número total de amostras que são guardadas na lista
num_amostras_seguemaior = 171        # Ao ver 2 pretos, quantas amostras são vistas antes para determinar se antes foi visto preto ou branco
num_amostras_menor = 10              # Quantas amostas são necessárias para identificar se foi visto um verde
num_amostras_segue = 1               # Quantas amostras são utilizadas para a execução do segue linha
num_amostras_verde = 35              # Ao ver verde, quantas amostras são vistas antes para determinar se antes foi visto preto ou branco
num_distancia = 40

BrancoEq = 53                 # O que diferencia o Preto do Branco no Segue Linha para o sensor direito
MediaPretoEq = 65             # Valor que diferencia Preto do Branco na média dos valores utilizados após ver dois pretos pelo sensor esquerdo
BrancoDr = 70                 # O que diferencia o Preto do Branco no Segue Linha para o sensor esquerdo
MediaPretoDr = 90             # Valor que diferencia Preto do Branco na média dos valores utilizados após ver dois pretos pelo sensor direito

# Listas ----------------------------------------------------------------
lista_ultimasLeiturasEsquerda = []
lista_ultimasLeiturasDireita = []
lista_distancia_cima = num_distancia * [200]
lista_distancia_baixo = num_distancia * [200]

# Garra -----------------------------------------------------------------  Garra deve começar fechada e abaixada, na altura em que ela pega a vítima
PosicaoGarraFechada = MotorGarra.position

# Preparação ------------------------------------------------------------
MotorBraço.on_for_seconds(SpeedPercent(-20), tempo_braço) # Subindo o Braço até a posição abaixada
PosicaoBraçoAbaixado = MotorBraço.position
MotorBraço.on_for_seconds(SpeedPercent(-20), tempo_braço) # Subindo o Braço mais ainda
MotorGarra.on_for_seconds(SpeedPercent(15),tempo_garra) # Abrindo a Garra
# time.sleep(1)
PosicaoGarraAberta = MotorGarra.position
PosicaoBraçoLevantado = MotorBraço.position
MotorGarra.on_to_position(SpeedPercent(20),PosicaoGarraFechada) # Fechar a Garra
x = 0
time.sleep(1)

#///////////////////////////////////////////////////////////////////////////////////////////////////////////#


# Programa principal ///////////////////////////////////////////////////////////////////////////////////////#

a = time.time() + 300
tempo_do_print = time.time() + 1

while a > time.time():

    # Variaveis -----------------------------------------------------------------
    e = coloresquerdo.value()  #Valores Lidos :Branco 73-77, Preto 6-8, Verde 4, Verm 42, Azul 5         
    d = colordireito.value()   #Valores Lidos :Branco 100, Preto 11, Verde 6-7,  Verm 72, Azul 8
    x+=1

    if len(lista_ultimasLeiturasDireita) < num_amostras:  # Mantendo o tamanho da lista em no máximo 'num_amostras' valores
        lista_ultimasLeiturasEsquerda.append(e)
        lista_ultimasLeiturasDireita.append(d)
    else:
        lista_ultimasLeiturasDireita.pop(0)
        lista_ultimasLeiturasEsquerda.pop(0)
        lista_ultimasLeiturasEsquerda.append(e)
        lista_ultimasLeiturasDireita.append(d)
    distancia = dist.value()
    
    media_direita = sum(lista_ultimasLeiturasDireita[-num_amostras_menor:])/num_amostras_menor
    media_esquerda = sum(lista_ultimasLeiturasEsquerda[-num_amostras_menor:])/num_amostras_menor
    media_direita2 = sum(lista_ultimasLeiturasDireita[-num_amostras_seguemaior:])/num_amostras_seguemaior
    media_esquerda2 = sum(lista_ultimasLeiturasEsquerda[-num_amostras_seguemaior:])/num_amostras_seguemaior
    #----------------------------------------------------------------------------
    
    if (e == 0 and d == 0):
        tank_drive.on(SpeedPercent(0), SpeedPercent(0))

    
    elif False:
        Sala_Resgate()
        c = sensor_cor.value()
        distancia = dist.value()
        tank_drive.on(SpeedPercent(0), SpeedPercent(0))
        print("Cima", distancia, "Baixo", c, file=sys.stderr)

    elif viu_verde2() :
        pass

    elif distancia < 120:    #Se foi visto um obstáculo
        tank_drive.on(SpeedPercent(0), SpeedPercent(0))
        print("Obstaculo!", distancia, file=sys.stderr)
        Obstaculo()

    else:
        Segue_linha()
        

print("----------------------------")
print("-   Expediente encerrado   -")
print("-     Leituras: ", x, "    -")
print("----------------------------")
tank_drive.on(SpeedPercent(0), SpeedPercent(0))

#///////////////////////////////////////////////////////////////////////////////////////////////////////////#
