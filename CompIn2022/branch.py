#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
#from ev3dev.ev3 import *
from ev3dev2.console import *
from time import sleep


# Olhando de Frente, o eixo da direita deve estar em cima do eixo da esquerda quando a garra astá fechada. Nesse caso, para abrir a garra é utilizada uma velocidade positiva e um tempo de 0.35s
#MotorBraço.on_for_seconds(SpeedPercent(-20), tempo_braço)   #Subir a Garra
# # Fechar a Garra  0.5 Ideal


# Funções ///////////////////////////////////////////////////////////////////////////////////////////////////#
def Segue_linha():
    media_direita_linha = sum(lista_ultimasLeiturasDireita[-num_amostras_segue:])/num_amostras_segue
    media_esquerda_linha = sum(lista_ultimasLeiturasEsquerda[-num_amostras_segue:])/num_amostras_segue
    if media_esquerda_linha > 53 and media_direita_linha <= 70:   #Branco na esquerda e Preto na direita
        tank_drive.on(SpeedPercent(-18),SpeedPercent(33))         #Virar pra Direita
    elif media_esquerda_linha <= 53 and media_direita_linha > 70: #Preto na esquerda e Branco na direita
        tank_drive.on(SpeedPercent(33),SpeedPercent(-18))         #Virar pra Esquerda
    elif media_esquerda_linha > 53 and media_direita_linha > 70:  #Branco na esquerda e na Direita
        tank_drive.on(SpeedPercent(20), SpeedPercent(20))         #Seguir Reto
    elif media_esquerda2 < 15 and media_direita2 > 15:            #Preto nas duas com preto na esquerda antes
        tank_drive.on(SpeedPercent(45),SpeedPercent(-25))         #Virar para Esquerda
    elif media_direita2 < 15 and media_esquerda2 > 15:            #Preto nas duas com preto na direita antes
        tank_drive.on(SpeedPercent(-25),SpeedPercent(45))         #Virar pra Direita
    else:                                                         #Preto em ambos com branco antes em ambos
        tank_drive.on(SpeedPercent(5), SpeedPercent(5))           #Andar reto

def pegar_objeto_posicao():
    MotorGarra.on_to_position(SpeedPercent(20),PosicaoGarraAberta) # Abrir a Garra 
    time.sleep (0.5)
    MotorBraço.on_to_position(SpeedPercent(20),PosicaoBraçoAbaixado) # Descer a Garra
    time.sleep (0.5)
    MotorGarra.on_to_position(SpeedPercent(20),PosicaoGarraFechada) # Fechar a Garra 
    time.sleep (0.5)
    MotorBraço.on_to_position(SpeedPercent(20),PosicaoBraçoLevantado) # Subir a Garra0
    time.sleep (0.5)

def Obstaculo():
    # Vendo e virando -----------------------------------------------
    distancia = dist.value()
    distanciaesq = dist_esquerda.value()
    time.sleep(1)
    while(distanciaesq>150):
        distancia = dist.value()
        distanciaesq = dist_esquerda.value()
        tank_drive.on(SpeedPercent(-25), SpeedPercent(25))
    # Virando ate ver -----------------------------------------------
    tank_drive.on(SpeedPercent(0), SpeedPercent(0))
    time.sleep(1)
    while(distanciaesq<240):
        distancia = dist.value()
        distanciaesq = dist_esquerda.value()
        tank_drive.on(SpeedPercent(25), SpeedPercent(25))
    tank_drive.on(SpeedPercent(0), SpeedPercent(0))
    time.sleep(1)
    tank_drive.on_for_seconds(SpeedPercent(25), SpeedPercent(25),1)
    tank_drive.on(SpeedPercent(0), SpeedPercent(0))
    time.sleep(1)
    # Andando ate ver ------------------------------------------------------
    tank_drive.on_for_seconds(SpeedPercent(25), SpeedPercent(-25),0.9)
    time.sleep(1)
    while(distanciaesq>100):
        distancia = dist.value()
        distanciaesq = dist_esquerda.value()
        tank_drive.on(SpeedPercent(25), SpeedPercent(25))
    # Andando ate parar de ver ---------------------------------------------
    tank_drive.on(SpeedPercent(0), SpeedPercent(0))
    time.sleep(1)
    while(distanciaesq<100):
        distancia = dist.value()
        distanciaesq = dist_esquerda.value()
        tank_drive.on(SpeedPercent(25), SpeedPercent(25))
    tank_drive.on(SpeedPercent(0), SpeedPercent(0))
    # Andando de volta até a linha -----------------------------------------
    time.sleep(1)
    tank_drive.on_for_seconds(SpeedPercent(25), SpeedPercent(-25),0.6)
    time.sleep(1)
    d = colordireito.value()
    while(d > 90):
        d = colordireito.value()  
        tank_drive.on(SpeedPercent(25), SpeedPercent(25))    

#///////////////////////////////////////////////////////////////////////////////////////////////////////////#


# Variaveis ////////////////////////////////////////////////////////////////////////////////////////////////#
# Módulos e suas portas -------------------------------------------------
MotorGarra = Motor(OUTPUT_D)
dist = UltrasonicSensor(INPUT_2)
coloresquerdo = ColorSensor(INPUT_3)
colordireito = ColorSensor(INPUT_4)
MotorBraço = Motor(OUTPUT_A)
tank_drive = MoveTank(OUTPUT_C, OUTPUT_B)  #C - Direita    B - Esquerda
dist_esquerda = UltrasonicSensor(INPUT_1)

# Parametros ------------------------------------------------------------
tempo_braço = 0.8
tempo_garra = 0.35
tempo_adicional = 0
num_amostras = 100
num_amostras_seguemaior = 25
num_amostras_menor = 10
num_amostras_segue = 1

# Listas ----------------------------------------------------------------
lista_ultimasLeiturasEsquerda = []
lista_ultimasLeiturasDireita = []

# Garra -----------------------------------------------------------------
PosicaoGarraFechada = MotorGarra.position
PosicaoBraçoAbaixado = MotorBraço.position
PosicaoGarraAberta = MotorGarra.position
PosicaoBraçoLevantado = MotorBraço.position
# Preparação ------------------------------------------------------------
# MotorBraço.on_for_seconds(SpeedPercent(-20), tempo_braço) # Subindo a Garra
# MotorGarra.on_for_seconds(SpeedPercent(15),tempo_garra) # Abrindo a Garra
# time.sleep(1)
PosicaoGarraAberta = MotorGarra.position
PosicaoBraçoLevantado = MotorBraço.position
# MotorGarra.on_to_position(SpeedPercent(20),PosicaoGarraFechada) # Fechar a Garra 
#///////////////////////////////////////////////////////////////////////////////////////////////////////////#


# Programa principal ///////////////////////////////////////////////////////////////////////////////////////#
while True:

    # Variaveis -----------------------------------------------------------------
    e = coloresquerdo.value()  #Valores Lidos :Branco 73-77, Preto 6-8, Verde 4                
    d = colordireito.value()   #Valores Lidos :Branco 100, Preto 11, Verde 6-7 
    if len(lista_ultimasLeiturasDireita) < num_amostras:
        lista_ultimasLeiturasEsquerda.append(e)
        lista_ultimasLeiturasDireita.append(d)
    else:
        lista_ultimasLeiturasDireita.pop(0)
        lista_ultimasLeiturasEsquerda.pop(0)
        lista_ultimasLeiturasEsquerda.append(e)
        lista_ultimasLeiturasDireita.append(d)
    distancia = dist.value()
    distanciaesq = dist_esquerda.value()
    media_direita = sum(lista_ultimasLeiturasDireita[-num_amostras_menor:])/num_amostras_menor
    media_esquerda = sum(lista_ultimasLeiturasEsquerda[-num_amostras_menor:])/num_amostras_menor
    media_direita2 = sum(lista_ultimasLeiturasDireita[-num_amostras_seguemaior:])/num_amostras_seguemaior
    media_esquerda2 = sum(lista_ultimasLeiturasEsquerda[-num_amostras_seguemaior:])/num_amostras_seguemaior
    #----------------------------------------------------------------------------

    print("Esquerda: ", e, "Direita: ", d)
    print("Media esquerda: ", media_esquerda, "Media direita: ", media_direita)
    print("Distancia frente: ", distancia, "Distancia esquerda: ", distanciaesq)

    if e == 0 and d == 0 or False:
        tank_drive.on(SpeedPercent(0),SpeedPercent(0)) 
    elif media_direita <= 8 and (len(lista_ultimasLeiturasDireita) >= num_amostras_menor): #Checa se vê verde do lado direito Valor <= 9
        if sum(lista_ultimasLeiturasDireita)/num_amostras < 30 and sum(lista_ultimasLeiturasEsquerda)/num_amostras < 100:
            tank_drive.on_for_seconds(SpeedPercent(40), SpeedPercent(50),1) #Se antes do verde foi visto preto
        else:
            tank_drive.on_for_seconds(SpeedPercent(5), SpeedPercent(35),1.4)  # Se antes do verde foi visto branco (Virar para a direita)

    elif  media_esquerda <= 4.5 and (len(lista_ultimasLeiturasEsquerda) >= num_amostras_menor): #Checa se vê verde do lado esquerdo Valor <= 4
        if sum(lista_ultimasLeiturasEsquerda)/num_amostras < 30 and sum(lista_ultimasLeiturasDireita)/num_amostras < 100:
            tank_drive.on_for_seconds(SpeedPercent(50), SpeedPercent(40),1) #Se antes do verde foi visto preto
        else:
            tank_drive.on_for_seconds(SpeedPercent(35), SpeedPercent(5),1.4)  # Se antes do verde foi visto branco (Virar para a esquerda)
    else:
        Segue_linha()
#///////////////////////////////////////////////////////////////////////////////////////////////////////////#