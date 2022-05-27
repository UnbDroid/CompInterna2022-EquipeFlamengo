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
    if media_esquerda_linha > BrancoEq and media_direita_linha <= BrancoDr:   # Branco na esquerda e Preto na direita
        tank_drive.on(SpeedPercent(-18),SpeedPercent(33))                     # Virar pra Direita
    elif media_esquerda_linha <= BrancoEq and media_direita_linha > BrancoDr: # Preto na esquerda e Branco na direita
        tank_drive.on(SpeedPercent(33),SpeedPercent(-18))                     # Virar pra Esquerda
    elif media_esquerda_linha > BrancoEq and media_direita_linha > BrancoDr:  # Branco na esquerda e na Direita
        tank_drive.on(SpeedPercent(20), SpeedPercent(20))                     # Seguir Reto
    else:  # Preto em ambos
        if media_direita2 < MediaPretoDr and media_esquerda2 > MediaPretoEq:            # Preto na esquerda antes
            tank_drive.on(SpeedPercent(45),SpeedPercent(-25))                 # Virar para Esquerda
        elif media_esquerda2 < MediaPretoEq and media_direita2 > MediaPretoDr:         # Preto na direita antes
            tank_drive.on(SpeedPercent(-25),SpeedPercent(45))                 # Virar pra Direita
        else:                                                                 # Branco antes em ambos
            tank_drive.on(SpeedPercent(5), SpeedPercent(5))                   # Andar reto

def viu_verde():
    media_direita_verde = sum(lista_ultimasLeiturasDireita[-num_amostras_verde:])/num_amostras_verde
    media_esquerda_verde = sum(lista_ultimasLeiturasEsquerda[-num_amostras_verde:])/num_amostras_verde
    if media_direita <= 8.2:         #Foi visto verde pelo sensor direito
        tank_drive.on(SpeedPercent(0), SpeedPercent(0))
        if media_direita_verde < 35 and (len(lista_ultimasLeiturasDireita) >= num_amostras_menor):   # 35 amostras - dividindo em 35 se mostrou eficiente
            tank_drive.on_for_seconds(SpeedPercent(40), SpeedPercent(40),1) #Se antes do verde foi visto preto
        else:
            tank_drive.on_for_seconds(SpeedPercent(5), SpeedPercent(35),1.4)  # Se antes do verde foi visto branco (Virar para a direita) 1.4 segundos e (5; 35) é ideal
        return True
    elif media_esquerda <= 4.8:    # Foi visto verde pelo sensor esquerdo
        tank_drive.on(SpeedPercent(0), SpeedPercent(0))
        if media_esquerda_verde < 27 and (len(lista_ultimasLeiturasEsquerda) >= num_amostras_menor):
            tank_drive.on_for_seconds(SpeedPercent(50), SpeedPercent(40),1) #Se antes do verde foi visto preto
        else:
            tank_drive.on_for_seconds(SpeedPercent(35), SpeedPercent(5),1.4)  # Se antes do verde foi visto branco (Virar para a esquerda)  1.4 segundos e (35; 5) é ideal
        return True
    else:
        return False #Não foi visto verde

def viu_verde2():              # Testar a detecção de verde por valores seguidos de verde, e não por uma média dos últimos valores
    verde_dr = 8
    verde_eq = 4
    num_identifica_verde = 3
    media_direita_verde = sum(lista_ultimasLeiturasDireita[-num_amostras_verde:])/num_amostras_verde
    media_esquerda_verde = sum(lista_ultimasLeiturasEsquerda[-num_amostras_verde:])/num_amostras_verde
    if lista_ultimasLeiturasDireita[-num_identifica_verde:] == [verde_dr]*num_identifica_verde:         #Foi visto verde pelo sensor direito
        if media_direita_verde < 35 and (len(lista_ultimasLeiturasDireita) >= num_amostras_menor):   # 35 amostras - dividindo em 35 se mostrou eficiente
        #Se antes do verde foi visto preto
            e = coloresquerdo.value()              
            d = colordireito.value() 
            while not (e > BrancoEq and d > BrancoDr):
                tank_drive.on(SpeedPercent(10), SpeedPercent(15))
                e = coloresquerdo.value()              
                d = colordireito.value()   

        else:
            tank_drive.on_for_seconds(SpeedPercent(5), SpeedPercent(35),1.2)  # Se antes do verde foi visto branco (Virar para a direita) 1.4 segundos e (5; 35) é ideal
        return True
    elif lista_ultimasLeiturasEsquerda[-num_identifica_verde:] == [verde_eq]*num_identifica_verde:    # Foi visto verde pelo sensor esquerdo
        if media_esquerda_verde < 27 and (len(lista_ultimasLeiturasEsquerda) >= num_amostras_menor):   #Se antes do verde foi visto preto
            e = coloresquerdo.value()              
            d = colordireito.value() 
            while not (e > BrancoEq and d > BrancoDr):
                tank_drive.on(SpeedPercent(10), SpeedPercent(15))
                e = coloresquerdo.value()              
                d = colordireito.value()   
        else:
            tank_drive.on_for_seconds(SpeedPercent(35), SpeedPercent(5),1.2)  # Se antes do verde foi visto branco (Virar para a esquerda)  1.4 segundos e (35; 5) é ideal
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
    while(d > BrancoDr):
        d = colordireito.value()  
        tank_drive.on(SpeedPercent(25), SpeedPercent(25))    
    

def Sala_Resgate():
    num_identifica_vermelho = 1
    vermelho_dr = 54
    if lista_ultimasLeiturasDireita[-num_identifica_vermelho:] == [vermelho_dr]*num_identifica_vermelho:
        tank_drive.on(SpeedPercent(0), SpeedPercent(0))
        return True
    else:
        return False


#///////////////////////////////////////////////////////////////////////////////////////////////////////////#


# Variaveis ////////////////////////////////////////////////////////////////////////////////////////////////#
# Módulos e suas portas -------------------------------------------------
MotorGarra = Motor(OUTPUT_D)
dist = UltrasonicSensor(INPUT_1)
coloresquerdo = ColorSensor(INPUT_3)
colordireito = ColorSensor(INPUT_4)
MotorBraço = Motor(OUTPUT_A)
tank_drive = MoveTank(OUTPUT_C, OUTPUT_B)  #C - Direita    B - Esquerda
sensor_cor = LightSensor(INPUT_2)

# Parametros ------------------------------------------------------------
tempo_braço = 0.8                    # Tempo de subida/descida do braço
tempo_garra = 0.35                   # Tempo de abertura/fechamento da garra

num_amostras = 250                  # Número total de amostras que são guardadas na lista
num_amostras_seguemaior = 171        # Ao ver 2 pretos, quantas amostras são vistas antes para determinar se antes foi visto preto ou branco
num_amostras_menor = 10              # Quantas amostas são necessárias para identificar se foi visto um verde
num_amostras_segue = 1               # Quantas amostras são utilizadas para a execução do segue linha
num_amostras_verde = 35              # Ao ver verde, quantas amostras são vistas antes para determinar se antes foi visto preto ou branco

BrancoEq = 53                 # O que diferencia o Preto do Branco no Segue Linha para o sensor direito
MediaPretoEq = 65
BrancoDr = 70                 # O que diferencia o Preto do Branco no Segue Linha para o sensor esquerdo
MediaPretoDr = 90

# Listas ----------------------------------------------------------------
lista_ultimasLeiturasEsquerda = []
lista_ultimasLeiturasDireita = []

# Garra -----------------------------------------------------------------  Garra deve começar fechada e abaixada, na altura em que ela pega a vítima
PosicaoGarraFechada = MotorGarra.position
PosicaoBraçoAbaixado = MotorBraço.position
# Preparação ------------------------------------------------------------
# MotorBraço.on_for_seconds(SpeedPercent(-20), tempo_braço) # Subindo o Braço
#MotorGarra.on_for_seconds(SpeedPercent(15),tempo_garra) # Abrindo a Garra
# time.sleep(1)
PosicaoGarraAberta = MotorGarra.position
PosicaoBraçoLevantado = MotorBraço.position
#MotorGarra.on_to_position(SpeedPercent(20),PosicaoGarraFechada) # Fechar a Garra 
#///////////////////////////////////////////////////////////////////////////////////////////////////////////#
x = 0
a = time.time() + 30000
while a > time.time():
# Programa principal ///////////////////////////////////////////////////////////////////////////////////////#
#while True:

    # Variaveis -----------------------------------------------------------------
    e = coloresquerdo.value()  #Valores Lidos :Branco 73-77, Preto 6-8, Verde 4, Verm 42           
    d = colordireito.value()   #Valores Lidos :Branco 100, Preto 11, Verde 6-7,  Verm 72
    x+=1

    if len(lista_ultimasLeiturasDireita) < num_amostras:  # Mantendo o tamanho da lista em no máximo 'num_amostras' valores
        lista_ultimasLeiturasEsquerda.append(e)
        lista_ultimasLeiturasDireita.append(d)
    else:
        lista_ultimasLeiturasDireita.pop(0)
        lista_ultimasLeiturasEsquerda.pop(0)
        lista_ultimasLeiturasEsquerda.append(e)
        lista_ultimasLeiturasDireita.append(d)
    distancia = dist.value()                            # Distância detectada pelo sensor ultrassom frontal
    # distanciaesq = dist_esquerda.value()                # Distância detectada pelo sensor ultrassom esquerdo

    media_direita = sum(lista_ultimasLeiturasDireita[-num_amostras_menor:])/num_amostras_menor
    media_esquerda = sum(lista_ultimasLeiturasEsquerda[-num_amostras_menor:])/num_amostras_menor
    media_direita2 = sum(lista_ultimasLeiturasDireita[-num_amostras_seguemaior:])/num_amostras_seguemaior
    media_esquerda2 = sum(lista_ultimasLeiturasEsquerda[-num_amostras_seguemaior:])/num_amostras_seguemaior
    #----------------------------------------------------------------------------

    print("Esquerda: ", e, "Direita: ", d)
    # print("Media esquerda: ", media_esquerda, "Media direita: ", media_direita)
    # print("Distancia frente: ", distancia, "Distancia esquerda: ", distanciaesq)

    if (e == 0 and d == 0) or False:
        tank_drive.on(SpeedPercent(0),SpeedPercent(0)) 
    elif viu_verde2() :
        pass
    elif Sala_Resgate():
        pass
    else:
        Segue_linha()

    
    # if distancia <135 :                                    #Se foi visto um obstáculo
    #     tank_drive.on(SpeedPercent(0), SpeedPercent(0))
    #     Obstaculo()

#///////////////////////////////////////////////////////////////////////////////////////////////////////////#

print(x)
tank_drive.on(SpeedPercent(0), SpeedPercent(0))


while True:
    pass