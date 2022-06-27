#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.sensor import*
from ev3dev2.sensor.lego import *
from ev3dev2.console import *
from time import sleep
import random
import sys
from ev3dev2.sound import Sound


#Funcoes//////////////////////////////////////////////////////////////////////////////////////////////////////#
def leituras():
    global dist_up
    global dist_down
    global cor_left
    global cor_right

    global distancias_cima
    global distancias_baixo
    global cores_esq
    global cores_dir
    global memoria_movel
    global media_down
    global media_up
    global diferenca_valores
    global diferenca_medias

    dist_up = int(Ultrassom_cima.distance_centimeters)
    time.sleep(0.1)
    dist_down = int(Ultrassom_baixo.distance_centimeters)
    cor_left = coloresquerdo.value()
    cor_right = colordireito.value()

    if len(distancias_cima) <= 400:
        distancias_cima.append(dist_up)
        distancias_baixo.append(dist_down)
        cores_esq.append(cor_left)
        cores_dir.append(cor_right)
    else:
        distancias_cima.pop(0)
        distancias_cima.append(dist_up)
        distancias_baixo.pop(0)
        distancias_baixo.append(dist_down)
        cores_esq.pop(0)
        cores_esq.append(cor_left)
        cores_dir.pop(0)
        cores_dir.append(cor_right)
    media_down = int(sum(distancias_baixo[-memoria_movel:])/memoria_movel)
    media_up = int(sum(distancias_cima[-memoria_movel:])/memoria_movel)
    diferenca_valores = dist_up - dist_down
    diferenca_medias = int(media_up - media_down)
    print("Valores: Cima= ", dist_up," Baixo= ",  dist_down, "/ Medias: Cima= ", media_up," Baixo= ", media_down, "/ Diferencas: Valores= ", diferenca_valores, "Medias= ", diferenca_medias, "/ Cores: Esquerda= ", cor_left, "Direita= ", cor_right,file=sys.stderr)

def pegar_objeto_posicao():
    global tentativas
    tentando = True
    while tentando:
        MotorGarra.on_to_position(SpeedPercent(20),PosicaoGarraAberta) # Abrir a Garra 
        time.sleep (0.5)
        MotorBraço.on_to_position(SpeedPercent(20),PosicaoBraçoAbaixado) # Descer a Garra
        time.sleep (0.5)
        MotorGarra.on_to_position(SpeedPercent(20),PosicaoGarraFechada) # Fechar a Garra 
        time.sleep (0.5)
        MotorBraço.on_to_position(SpeedPercent(20),PosicaoBraçoLevantado) # Subir a Garra
        time.sleep (2)
        leituras()
        if dist_down > 5:
            tentando = False
            tentativas = 0
        elif tentativas > 4:
            tentando = False
        else:
            tentativas += 1
            pegar_objeto_posicao()

def checkando_cor(cor):
    if cor == "vermelho":
        lista_eq = [48,49,50,51,52,53,54,55,56]
        lista_dr = [68,69,70,71,72,73,74,75,76,77,78]
        num_identifica_cor = 3
    elif cor == "verde":
        lista_eq = [3,4,5,6]
        lista_dr = [7,8,9]
        num_identifica_cor = 3
    elif cor == "preto":
        lista_eq = [5,6,7,8,9,10,11,12,13,14,15,16,17]
        lista_dr = [10,11,12,13,14,15,16,17,18,19,20]
        num_identifica_cor = 3
    contador_cor_dr = 0
    contador_cor_eq = 0
    for i in cores_dir[-num_identifica_cor:]:
        if i in lista_dr:
            contador_cor_dr +=1
        else:
            break
    for j in cores_esq[-num_identifica_cor:]:
        if j in lista_eq:
            contador_cor_eq +=1
        else:
            break
    if contador_cor_dr == num_identifica_cor and contador_cor_eq == num_identifica_cor:
        return [True, 'Ambos']
    elif contador_cor_dr == num_identifica_cor:
        return [True, 'D'] 
    elif contador_cor_eq == num_identifica_cor:
        return [True, 'E'] 
    else: 
        return [False, '']

def procurando(vl, vr, t, cond = True, rand = False):
    tempo_de_leitura = time.time() + t
    while tempo_de_leitura > time.time():
        tank_drive.on(SpeedPercent(vl), SpeedPercent(vr))
        leituras()
        viu_verde = checkando_cor("verde")
        viu_vermelho = checkando_cor("vermelho")
        viu_preto = checkando_cor("preto")
        if media_down >= 45:
            diferenca_da_bolinha = 30
        elif media_down < 45:
            diferenca_da_bolinha = 5
        if diferenca_medias > diferenca_da_bolinha:
            spkr.tone([(450, 350, 30)])
            tank_drive.on(SpeedPercent(0), SpeedPercent(0))
            tempo_de_leitura += 2.5
            time.sleep(0.5)
            for i in range(20):
                leituras()
            if diferenca_medias > diferenca_da_bolinha:
                while dist_down > 5:
                    tank_drive.on(SpeedPercent(25), SpeedPercent(25))
                    leituras()
                tank_drive.on(SpeedPercent(0), SpeedPercent(0))
                pegar_objeto_posicao()
        elif dist_up < 11:
            tank_drive.on(SpeedPercent(0), SpeedPercent(0))
            for i in range(20):
                leituras()
            if media_up > 11:
                break
            if diferenca_medias >= 2:
                pegar_objeto_posicao()
            tank_drive.on_for_seconds(SpeedPercent(-25), SpeedPercent(-25), 0.8)
            tank_drive.on_for_seconds(SpeedPercent(-25), SpeedPercent(25), 0.8)
            return
        elif viu_verde[0] or (viu_vermelho == [True, "Ambos"]) or viu_preto[0]:
            tank_drive.on_for_seconds(SpeedPercent(-25), SpeedPercent(-25), 0.8)
            tank_drive.on_for_seconds(SpeedPercent(-25), SpeedPercent(25), 0.8)
        

        


#Funcoes//////////////////////////////////////////////////////////////////////////////////////////////////////#


#Variaveis////////////////////////////////////////////////////////////////////////////////////////////////////#
MotorGarra = Motor(OUTPUT_D)
Ultrassom_baixo = UltrasonicSensor(INPUT_1)
Ultrassom_cima = UltrasonicSensor(INPUT_2)
coloresquerdo = ColorSensor(INPUT_3)
colordireito = ColorSensor(INPUT_4)
MotorBraço = Motor(OUTPUT_A)
tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)
spkr = Sound()

dist_up = int(Ultrassom_cima.distance_centimeters)
time.sleep(0.1)
dist_down = int(Ultrassom_baixo.distance_centimeters)
diferenca_valores = dist_up - dist_down
cor_left = coloresquerdo.value()
cor_right = colordireito.value()
distancias_cima = []
distancias_baixo = []
cores_esq = []
cores_dir = []
tentativas = 0
memoria_movel = 5
media_down = 0
media_up = 0
diferenca_valores = 0
diferenca_medias = 0
#Variaveis////////////////////////////////////////////////////////////////////////////////////////////////////#


#Programa_principal///////////////////////////////////////////////////////////////////////////////////////////#
#Preparação ------------------------------------------------------------#
tempo_subida, tempo_garra = 1, 0.25
PosicaoGarraFechada = MotorGarra.position
MotorBraço.on_for_seconds(SpeedPercent(-20), tempo_subida) #Subindo o Braço até a posição abaixada
PosicaoBraçoAbaixado = MotorBraço.position
MotorBraço.on_for_seconds(SpeedPercent(-20), tempo_subida) #Subindo o Braço mais ainda
MotorGarra.on_for_seconds(SpeedPercent(15),tempo_garra)   #Abrindo a Garra
PosicaoGarraAberta = MotorGarra.position
PosicaoBraçoLevantado = MotorBraço.position
MotorGarra.on_to_position(SpeedPercent(20),PosicaoGarraFechada) #Fechar a Garra
#Preparação ------------------------------------------------------------#

#Programa --------------------------------------------------------------#
for i in range(50):
    leituras()
time.sleep(1)
tempo = time.time() + 1
while True:
    leituras()
    procurando(25,25,5)
#Programa_principal///////////////////////////////////////////////////////////////////////////////////////////#