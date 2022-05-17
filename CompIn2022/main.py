#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
#from ev3dev.ev3 import *
from ev3dev2.console import *
from time import sleep


def calibrarGarra():
    return

def Segue_linha():
    e = coloresquerdo.value()
    d = colordireito.value()
    if e > 40 and d <= 30: 
        tank_drive.on(SpeedPercent(-25),SpeedPercent(45))
    elif e <= 20 and d > 50:
        tank_drive.on(SpeedPercent(45),SpeedPercent(-25))
    elif e > 40 and d > 50:
        tank_drive.on(SpeedPercent(30), SpeedPercent(30))
    #elif 55>e>30 and 55>d>30:
        #tank_drive.on(SpeedPercent(0), SpeedPercent(0))
    else:
        tank_drive.on(SpeedPercent(-10), SpeedPercent(10))
    #print("Esquerda", e ,"Direita", d)

def Segue_linha2():
     tank_drive.on(SpeedPercent(0), SpeedPercent(0))

def pegar_objeto():
    MotorGarra.on_for_seconds(SpeedPercent(-15),tempo_garra+tempo_adicional) # Abrir a Garra 0.67 Ideal
    time.sleep (0.5)
    MotorBraço.on_for_seconds(SpeedPercent(20),tempo_braço) # Descer a Garra
    time.sleep (0.5)
    MotorGarra.on_for_seconds(SpeedPercent(15),tempo_garra) # Fechar a Garra  0.5 Ideal
    time.sleep (0.5)
    MotorBraço.on_for_seconds(SpeedPercent(-20), tempo_braço) # Subir a Garra
    time.sleep (0.5)

def pegar_objeto_posicao():
    MotorGarra.on_to_position(SpeedPercent(20),PosicaoGarraAberta) # Abrir a Garra 
    time.sleep (0.5)
    MotorBraço.on_to_position(SpeedPercent(20),PosicaoBraçoAbaixado) # Descer a Garra
    time.sleep (0.5)
    MotorGarra.on_to_position(SpeedPercent(20),PosicaoGarraFechada) # Fechar a Garra 
    time.sleep (0.5)
    MotorBraço.on_to_position(SpeedPercent(20),PosicaoBraçoLevantado) # Subir a Garra
    MotorBraço.on_for_seconds(SpeedPercent(-20), tempo_adicional)
    time.sleep (0.5)

def checa_verde():
    n = 30 #Quantidade de medições que serão checadas para ver se o verde foi realmente visto
    lim_inferior = 30
    lim_superior = 40
    if lim_inferior<=sum(lista_ultimasLeiturasEsquerda[-n:])/n<=lim_superior or lim_inferior<=sum(lista_ultimasLeiturasEsquerda[-n:])/n<=lim_superior:
        return True
    return False


def Obstaculo():
    e = coloresquerdo.value()
    d = colordireito.value()
    #-----------------------------------------------
    tank_drive.on(SpeedPercent(-25), SpeedPercent(25))
    time.sleep(0.7)
    #-----------------------------------------------
    tempo = time.time() + 1.5
    while e > 40 and d > 40 and tempo > time.time():
        e = coloresquerdo.value()
        d = colordireito.value()
        tank_drive.on(SpeedPercent(25), SpeedPercent(25))
    if e < 40 or d < 40:
        return
    #-----------------------------------------------
    tank_drive.on(SpeedPercent(25), SpeedPercent(-25))
    time.sleep(0.75)
    #-----------------------------------------------
    tempo = time.time() + 3
    while e > 40 and d > 40 and tempo > time.time():
        e = coloresquerdo.value()
        d = colordireito.value()
        tank_drive.on(SpeedPercent(25), SpeedPercent(25))
    if e < 40 or d < 40:
        return
    #-----------------------------------------------
    tank_drive.on(SpeedPercent(25), SpeedPercent(-25))
    time.sleep(0.75)
    #-----------------------------------------------
    while e > 40 and d > 40:
        e = coloresquerdo.value()
        d = colordireito.value()
        tank_drive.on(SpeedPercent(25), SpeedPercent(25))



MotorGarra = Motor(OUTPUT_D)
dist = UltrasonicSensor(INPUT_2)
coloresquerdo = ColorSensor(INPUT_3)
colordireito = ColorSensor(INPUT_4)
MotorBraço = Motor(OUTPUT_A)
tank_drive = MoveTank(OUTPUT_C, OUTPUT_B)
tempo_braço = 1
tempo_garra = 0.35
tempo_adicional = 0
num_amostras = 100
num_amostras_menor = 2
lista_ultimasLeiturasEsquerda = []
lista_ultimasLeiturasDireita = []

# Olhando de Frente, o eixo da direita deve estar em cima do eixo da esquerda quando a garra astá fechada. Nesse caso, para abrir a garra é utilizada uma velocidade positiva e um tempo de 0.35s
#MotorBraço.on_for_seconds(SpeedPercent(-20), tempo_braço)   #Subir a Garra
# # Fechar a Garra  0.5 Ideal


PosicaoGarraFechada = MotorGarra.position
PosicaoBraçoAbaixado = MotorBraço.position

MotorBraço.on_for_seconds(SpeedPercent(-20), tempo_braço) # Subindo a Garra
MotorGarra.on_for_seconds(SpeedPercent(15),tempo_garra) # Abrindo a Garra
time.sleep(1)

#while True:
#    tempo_adicional=0
PosicaoGarraAberta = MotorGarra.position
PosicaoBraçoLevantado = MotorBraço.position

MotorGarra.on_to_position(SpeedPercent(20),PosicaoGarraFechada) # Fechar a Garra 

while True:
    e = coloresquerdo.value()  #Valores Lidos :Branco 73-77, Preto 6-8
    d = colordireito.value()   #Valores Lidos :Branco 100, Preto 11, Verde 6
    if len(lista_ultimasLeiturasDireita) < 100:
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
    print(media_esquerda)
    print(media_direita)
    print("Esquerda: ", e, "Direita: ", d, "Distancia: ", distancia)

    if media_direita <= 10.1 and (len(lista_ultimasLeiturasDireita) >= num_amostras_menor):
        tank_drive.on(SpeedPercent(0), SpeedPercent(0))
    elif  8.5 <= media_esquerda <= 9.5 and (len(lista_ultimasLeiturasEsquerda) >= num_amostras_menor):
        tank_drive.on(SpeedPercent(0), SpeedPercent(0))
    else:
        Segue_linha()
    # if distancia <62 : 
    #     tank_drive.on(SpeedPercent(0), SpeedPercent(0))
    #     pegar_objeto_posicao()

    #if checa_verde:
    # if 30<=sum(lista_ultimasLeiturasEsquerda)/10<=40 or 30<=lista_ultimasLeiturasDireita/10<=40:#se um dos sensores identificar o verde 
    #     tank_drive.on(SpeedPercent(0), SpeedPercent(0))
    #     if(30<=sum(lista_ultimasLeiturasEsquerda)/10<=40):
    #         return
            
    #     else:
    #         return
    #Segue_linha()








# while True:
#     if t.is_pressed and etapa == 1:
#         #Subir a Garra  
#         MotorBraço.on_for_seconds(SpeedPercent(-20), tempo_braço)
#         while (t.is_pressed):
#             MotorBraço.on(SpeedPercent(0))
#         print("Etapa 1", etapa)
#         etapa +=1
#     if t.is_pressed and etapa == 2:
#         #Abrir a Garra
#         MotorGarra.on_for_seconds(SpeedPercent(-15),0.5)
#         while (t.is_pressed):
#             MotorGarra.on(SpeedPercent(0))
#         print("Etapa 2", etapa)
#         etapa +=1
#     if t.is_pressed and etapa == 3:
#         #Descer a Garra
#         MotorBraço.on_for_seconds(SpeedPercent(20),tempo_braço)
#         while (t.is_pressed):
#             MotorBraço.on(SpeedPercent(0))
#         print("Etapa 3", etapa)
#         etapa +=1
#     if t.is_pressed and etapa == 4:
#         #Fechar a Garra
#         MotorGarra.on_for_seconds(SpeedPercent(15),0.67)
#         while (t.is_pressed):
#             MotorGarra.on(SpeedPercent(0))
#         print("Etapa 4", etapa)
#         etapa = 1





# x = 100
# etapa = 1
# # MotorGarra.on_for_degrees(SpeedPercent(15), -x)
# # garra_aberta =  MotorGarra.position
# # MotorGarra.on_for_degrees(SpeedPercent(15), -x)
# # garra_fechada = MotorGarra.position
# # MotorGarra.stop_action = 'coast'
# # MotorGarra.speed_sp = 0.1 * MotorGarra.max_speed

# while True:
#     if t.is_pressed and etapa == 1:
#         #position_sp = garra_aberta
#         #MotorGarra.run_to_abs_pos
#         MotorGarra.on_for_degrees(SpeedPercent(15), x)
#         while t.is_pressed:
#             MotorGarra.on(SpeedPercent(0))
#         print('to aqui')
#         etapa += 1
#     if t.is_pressed and etapa == 2:
#         #position_sp = garra_fechada
#         #MotorGarra.run_to_abs_pos
#         MotorGarra.on_for_degrees(SpeedPercent(15), x)
#         while t.is_pressed:
#             MotorGarra.on(SpeedPercent(0))
#         print('to aqui 2')
#         etapa = 1



# x = 60
# while True:
#     MotorGarra.on_for_degrees(SpeedPercent(15), x)
#     MotorGarra.on_for_degrees(SpeedPercent(15), -x)


