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

import statistics



# Olhando de Frente, o eixo da direita deve estar em cima do eixo da esquerda quando a garra astá fechada. 
# Nesse caso, para abrir a garra é utilizada uma velocidade positiva e um tempo de 0.35s
# Fechar a Garra  0.5 Ideal

# Funções ///////////////////////////////////////////////////////////////////////////////////////////////////#

sobreviventesResgatados =0
tempo_total = 0


def Segue_linha():

    media_direita_linha = sum(lista_ultimasLeiturasDireita[-num_amostras_segue:])/num_amostras_segue
    media_esquerda_linha = sum(lista_ultimasLeiturasEsquerda[-num_amostras_segue:])/num_amostras_segue
    if media_esquerda_linha > BrancoEq and media_direita_linha <= BrancoDr:   # Branco na esquerda e Preto na direita
        tank_drive.on(SpeedPercent(-11),SpeedPercent(45))                        # Virar pra Direita
    elif media_esquerda_linha <= BrancoEq and media_direita_linha > BrancoDr: # Preto na esquerda e Branco na direita
        tank_drive.on(SpeedPercent(45),SpeedPercent(-11))                       # Virar pra Esquerda
    elif media_esquerda_linha > BrancoEq and media_direita_linha > BrancoDr:  # Branco na esquerda e na Direita
        tank_drive.on(SpeedPercent(20), SpeedPercent(20))                       # Seguir Reto
    else:
        print("Direita", media_direita2, "Esquerda", media_esquerda2, file=sys.stderr)    
        tank_drive.on(SpeedPercent(0), SpeedPercent(0))     
        e = coloresquerdo.value()
        d = colordireito.value()                                                                 # Preto em ambos
        if media_direita2 < MediaPretoDr and media_esquerda2 > MediaPretoEq:    # Preto na esquerda antes
            #while not (d >  80 and e > 50):
            e = coloresquerdo.value()
            d = colordireito.value()                                                                 
            tank_drive.on_for_seconds(SpeedPercent(45),SpeedPercent(-25),0.35)                     # Virar para Esquerda
        elif media_esquerda2 < MediaPretoEq and media_direita2 > MediaPretoDr:         # Preto na direita antes
            #while not (d > 80 and e > 50):
            e = coloresquerdo.value()
            d = colordireito.value()  
            tank_drive.on_for_seconds(SpeedPercent(-25),SpeedPercent(45),0.35)                     # Virar pra Direita
        else:                                                                   # Branco antes em ambos
            tank_drive.on(SpeedPercent(35), SpeedPercent(35))                       # Andar reto


def viu_verde(cond = False):          #Quando a condição é True, ele só checa se viu verde ou não, mas não realiza a ação. Para checar se foi visto verde na Sala de Resgate
    verde_dr = [7,8,9]
    verde_eq = [3,4,5,6]
    num_identifica_verde = 5
    if cond:
        num_identifica_verde = 2
        verde_eq = [3,4,5] # Menos valores para ver verde na sala de resgate já que a fita é fininha
        verde_dir = [7,8]
    media_direita_verde = sum(lista_ultimasLeiturasDireita[-num_amostras_verde:])/num_amostras_verde
    media_esquerda_verde = sum(lista_ultimasLeiturasEsquerda[-num_amostras_verde:])/num_amostras_verde
    #if lista_ultimasLeiturasDireita[-num_identifica_verde:] == [verde_dr]*num_identifica_verde:      # Foi visto verde pelo sensor direito
    contador_dr = 0
    contador_eq = 0
    for i in lista_ultimasLeiturasDireita[-num_identifica_verde:]:
        if i in verde_dr:
            contador_dr +=1
        else:
            break
    for j in lista_ultimasLeiturasEsquerda[-num_identifica_verde:]:
        if j in verde_eq:
            contador_eq +=1
        else:
            break
    if contador_dr == num_identifica_verde:
        if cond:
            return [True, 'D']   #Retorna que foi visto verde pelo sensor direito D, para a sala de resgate
        print("Direita Verde1", media_direita_verde, "Esquerda Verde1", media_esquerda_verde, "Lista", lista_ultimasLeiturasDireita[-num_identifica_verde:], file=sys.stderr) 
        tank_drive.on_for_seconds(SpeedPercent(0), SpeedPercent(0),0.01)
        time.sleep(0.01)
        spkr.tone([(450, 350, 30)])
        if media_direita_verde < 75 and media_esquerda_verde < 70: # Esse 61 é totalmente arbitrário, ainda n testei:   # 35 amostras - dividindo em 35 se mostrou eficiente
        #Se antes do verde foi visto preto
            e = coloresquerdo.value()              
            d = colordireito.value() 
            while not (e > BrancoEq and d > BrancoDr):
                tank_drive.on(SpeedPercent(11), SpeedPercent(10))
                e = coloresquerdo.value()              
                d = colordireito.value()   
        else:
            # Se antes do verde foi visto branco 
            tank_drive.on_for_seconds(SpeedPercent(10), SpeedPercent(35),0.8)  # (Virar para a direita) 1.4 segundos e (5; 35) é ideal
        return True

    #elif lista_ultimasLeiturasEsquerda[-num_identifica_verde:] == [verde_eq]*num_identifica_verde:    # Foi visto verde pelo sensor esquerdo
    elif contador_eq == num_identifica_verde:
        if cond:
            return [True,'E']   #Retorna que foi visto verde pelo sensor esquerdo E, para a sala de resgate
        print("Direita Verde2", media_direita_verde, "Esquerda Verde2", media_esquerda_verde, "Lista", lista_ultimasLeiturasEsquerda[-num_identifica_verde:],  file=sys.stderr)
        tank_drive.on_for_seconds(SpeedPercent(0), SpeedPercent(0),0.01)
        time.sleep(0.01)
        spkr.tone([(300, 350, 30)])
        if media_direita_verde < 82 and media_esquerda_verde < 60:   #Se antes do verde foi visto preto
            e = coloresquerdo.value()       
            d = colordireito.value() 
            while not (e > BrancoEq and d > BrancoDr):
                tank_drive.on(SpeedPercent(10), SpeedPercent(14))
                e = coloresquerdo.value()              
                d = colordireito.value()   
        else:
            # Se antes do verde foi visto branco 
            tank_drive.on_for_seconds(SpeedPercent(35), SpeedPercent(10),0.8)  # (Virar para a esquerda)  1.4 segundos e (35; 5) é ideal
        return True
    else:
        if cond:
            return [False, ''] #Retorna uma lista com False como primeiro termo, para manter o padrão
        return False #Não foi visto verde


def viu_vermelho():
    vermelho_eq = [48,49,50,51,52,53,54,55,56,57,58,59,60]
    vermelho_dr = [68,69,70,71,72,73,74,75,76,77,78,79,80,81,82]
    num_identifica_vermelho = 3
    contador_dr = 0
    contador_eq = 0
    for i in lista_ultimasLeiturasDireita[-num_identifica_vermelho:]:
        if i in vermelho_dr:
            contador_dr +=1
        else:
            break
    for j in lista_ultimasLeiturasEsquerda[-num_identifica_vermelho:]:
        if j in vermelho_eq:
            contador_eq +=1
        else:
            break
    
    if contador_dr == num_identifica_vermelho and contador_eq == num_identifica_vermelho:
        return [True, 'Ambos']
    elif contador_dr == num_identifica_vermelho:
        return [True, 'D'] 
    elif contador_eq == num_identifica_vermelho:
        return [True, 'E'] 
    else: 
        return [False, '']



def viu_preto():    #Função para identificar se foi visto preto na sala de resgate

    listapreto_eq = [5,6,7,8,9,10,11,12,13,14,15,16,17]
    listapreto_dr = [10,11,12,13,14,15,16,17,18,19,20]
    num_identifica_preto = 2
    contador_dr = 0
    contador_eq = 0
    for i in lista_ultimasLeiturasDireita[-num_identifica_preto:]:
        if i in listapreto_dr:
            contador_dr +=1
        else:
            break
    for j in lista_ultimasLeiturasEsquerda[-num_identifica_preto:]:
        if j in listapreto_eq:
            contador_eq +=1
        else:
            break
    
    if contador_dr == num_identifica_preto and contador_eq == num_identifica_preto:
        return [True, 'Ambos']
    elif contador_dr == num_identifica_preto:
        return [True, 'D'] 
    elif contador_eq == num_identifica_preto:
        return [True, 'E'] 
    else: 
        return [False, '']


def pegar_objeto_posicao():
    MotorGarra.on_to_position(SpeedPercent(20),PosicaoGarraAberta) # Abrir a Garra 
    time.sleep (0.5)
    MotorBraço.on_to_position(SpeedPercent(20),PosicaoBraçoAbaixado) # Descer a Garra
    time.sleep (0.5)
    MotorGarra.on_to_position(SpeedPercent(20),PosicaoGarraFechada) # Fechar a Garra 
    time.sleep (0.5)
    MotorBraço.on_to_position(SpeedPercent(20),PosicaoBraçoLevantado) # Subir a Garra
    time.sleep (2)

def Obstaculo():
    e = coloresquerdo.value()
    d = colordireito.value()
    # Virando -------------------------------------------------------------
    tank_drive.on_for_seconds(SpeedPercent(30), SpeedPercent(0), 1.4)
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
    tempo = time.time() + 3.3
    while e > 40 and d > 40 and tempo > time.time():
        e = coloresquerdo.value()
        d = colordireito.value()
        tank_drive.on(SpeedPercent(25), SpeedPercent(25))
    if e < 40 or d < 40:
        return
    # Virando -------------------------------------------------------------
    tank_drive.on_for_seconds(SpeedPercent(0), SpeedPercent(30), 1.2)
    # Andando ate ver -----------------------------------------------------
    while not e < 20:
        e = coloresquerdo.value()
        d = colordireito.value()
        tank_drive.on(SpeedPercent(20), SpeedPercent(20))
    while not e > 40 and d > 40:
        tank_drive.on(SpeedPercent(5), SpeedPercent(-5))
        return

def pegou_a_bolinha(): #Função feita para retornar a bolinha para a área de resgate depois de pegá-la

    global tempo_total
    distancia = dist.value()
    d = colordireito.value()
    e = coloresquerdo.value()

    lista_ultimasLeiturasDireita.pop(0)
    lista_ultimasLeiturasEsquerda.pop(0)
    lista_ultimasLeiturasEsquerda.append(e)
    lista_ultimasLeiturasDireita.append(d)

    
    aux_verde = viu_verde(True)
    aux_vermelho = viu_vermelho()
    aux_preto = viu_preto()

    
    tempo_total = time.time()
    while not aux_preto[0]:     #Se foi visto preto por algum dos sensores
    
        distancia = dist.value()
        d = colordireito.value()
        e = coloresquerdo.value()

        lista_ultimasLeiturasDireita.pop(0)
        lista_ultimasLeiturasEsquerda.pop(0)
        lista_ultimasLeiturasEsquerda.append(e)
        lista_ultimasLeiturasDireita.append(d)


        lista_distancia_cima.pop(0)
        lista_distancia_cima.append(distancia)

        variancia =statistics.variance(lista_distancia_baixo)

        
        aux_verde = viu_verde(True)
        aux_vermelho = viu_vermelho()
        aux_preto = viu_preto()

        tank_drive.on(SpeedPercent(35), SpeedPercent(35))
        if distancia < 140:
            tempo_total = time.time() 
            #tank_drive.on_for_seconds(SpeedPercent(-25), SpeedPercent(-25),0.65)
            while not distancia > 140:
                distancia = dist.value()
                tank_drive.on(SpeedPercent(-25), SpeedPercent(-25))
            tank_drive.on_for_seconds(SpeedPercent(25), SpeedPercent(-25),0.9)
        elif aux_verde[0] or aux_vermelho[0]:
            tempo_total = time.time()
            tank_drive.on_for_seconds(SpeedPercent(0), SpeedPercent(0),0.01)
            spkr.tone([(200, 350, 30)])
            print(aux_verde, aux_vermelho, file=sys.stderr)
            tank_drive.on_for_seconds(SpeedPercent(-25),SpeedPercent(-25), 2.5)
            tank_drive.on_for_seconds(SpeedPercent(25),SpeedPercent(-25), 0.9)
        elif variancia < 2:
            tempo_total = time.time()
            print(variancia, file=sys.stderr)
            tank_drive.on_for_seconds(SpeedPercent(-50),SpeedPercent(-50), 1.6)
        elif time.time() - 13 >= tempo_total:
            spkr.tone([(523.5, 200),(587.33, 400)])
            tank_drive.on_for_seconds(SpeedPercent(-25),SpeedPercent(-25), 2)
            tank_drive.on_for_seconds(SpeedPercent(25), SpeedPercent(-25),0.9)
            tempo_total = time.time()

    if aux_preto[1] == 'E':     #Se foi visto preto apenas no sensor esquerdo, girar pra direita até ver preto nos dois
        while not aux_preto == [True, "Ambos"]:
            aux_preto = viu_preto()
            e = coloresquerdo.value()
            d = colordireito.value()

            lista_ultimasLeiturasDireita.pop(0)
            lista_ultimasLeiturasEsquerda.pop(0)
            lista_ultimasLeiturasEsquerda.append(e)
            lista_ultimasLeiturasDireita.append(d)

            tank_drive.on(SpeedPercent(45), SpeedPercent(-25))

    elif aux_preto[1] == 'D':   #Se foi visto preto apenas no sensor direito, girar pra esquerda até ver preto nos dois 
        while not aux_preto == [True, "Ambos"]:
            aux_preto = viu_preto()
            e = coloresquerdo.value()
            d = colordireito.value()

            lista_ultimasLeiturasDireita.pop(0)
            lista_ultimasLeiturasEsquerda.pop(0)
            lista_ultimasLeiturasEsquerda.append(e)
            lista_ultimasLeiturasDireita.append(d)

            tank_drive.on(SpeedPercent(-25), SpeedPercent(45))

    tank_drive.on_for_seconds(SpeedPercent(0),SpeedPercent(0),0.01)
    tank_drive.on(SpeedPercent(0), SpeedPercent(0))      
    tank_drive.on_for_seconds(SpeedPercent(25), SpeedPercent(25),0.6)
    tank_drive.on(SpeedPercent(0), SpeedPercent(0))     
    MotorBraço.on_for_seconds(SpeedPercent(20), tempo_braço/3) # Descendo o Braço
    MotorGarra.on_to_position(SpeedPercent(20),PosicaoGarraAberta) # Abrir a Garra 
    time.sleep(0.3)
    MotorGarra.on_to_position(SpeedPercent(20),PosicaoGarraFechada) # Fechar a Garra 
    MotorBraço.on_for_seconds(SpeedPercent(-20), tempo_braço/3) # Subindo o Braço
    tank_drive.on_for_seconds(SpeedPercent(-25), SpeedPercent(-25),0.01)
    tank_drive.on_for_seconds(SpeedPercent(-25), SpeedPercent(-25),2.5)
    tank_drive.on_for_seconds(SpeedPercent(25), SpeedPercent(-25),0.8)
    tank_drive.on_for_seconds(SpeedPercent(25), SpeedPercent(25),0.8)

def on_for_seconds(v1, v2, t, cond = True, random2 = False):  #Função implementada para fazer um on_for_seconds em que há a checagem durante o movimento. A condição 'cond' define se é necessária a checagem de paredes, que não é necessária na manobra do robô imediatamente depois de ver uma parede.
    aux = 0
    #cond = True
    
    tentativaPegarBolinha = 0
    global sobreviventesResgatados
    global tempo_total
    

    if random2:
        if random.randint(0, 1):      # 50% de chance dele inverter o movimento, ou seja de girar pra esquerda ou para a direita
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

        lista_ultimasLeiturasDireita.pop(0)
        lista_ultimasLeiturasEsquerda.pop(0)
        lista_ultimasLeiturasEsquerda.append(e)
        lista_ultimasLeiturasDireita.append(d)

        lista_distancia_baixo.pop(0)
        lista_distancia_cima.pop(0)
        lista_distancia_baixo.append(c)
        lista_distancia_cima.append(distancia)

        variancia =statistics.variance(lista_distancia_baixo)
        print(variancia, file=sys.stderr)
        #print(sobreviventesResgatados, file=sys.stderr)
        


        #AQUI ELE ESTÁ IDENTIFICANDO QUALQUER BOLA PARA PEGAR, IMPLEMENTAR A LÓGICA DE ESCOLHER
        #PRIMEIRO AS BOLINHAS BRANCAS
        if sobreviventesResgatados<3:
            if 853.4<c<2700:
                tempo_total = time.time()
                tank_drive.on_for_seconds(SpeedPercent(0),SpeedPercent(0),0.01)
                tank_drive.on(SpeedPercent(0),SpeedPercent(0))
                time.sleep(2)
                c = sensor_cor.value()
                if 853.4<c<2700:
                    pegar_objeto_posicao()
                    c = sensor_cor.value()
                    if c < 853.4:
                        pegou_a_bolinha()
                        sobreviventesResgatados+=1
                        return
                    else: 
                        while 853.4 < c < 2700:
                            pegar_objeto_posicao()
                            c = sensor_cor.value()
                            tentativaPegarBolinha += 1
                            if c < 853.4:
                                pegou_a_bolinha()
                                sobreviventesResgatados+=1
                                tentativaPegarBolinha += 1
                                return
                            if tentativaPegarBolinha >= 1:
                                tank_drive.on(SpeedPercent(0), SpeedPercent(0))
                                tank_drive.on_for_seconds(SpeedPercent(0),SpeedPercent(0),0.01)
                                tank_drive.on_for_seconds(SpeedPercent(-25),SpeedPercent(-25), 1.6)
                                c = sensor_cor.value()
                                break
                else:
                    tempo_total2 = time.time() + 2.25
                    while time.time() < tempo_total2:
                        c = sensor_cor.value()
                        tank_drive.on(SpeedPercent(5), SpeedPercent(-5)) 
                        if 853.4<c<2700:
                            tank_drive.on(SpeedPercent(0), SpeedPercent(0))
                            pegar_objeto_posicao()
                            c = sensor_cor.value()
                            if c < 853.4:
                                pegou_a_bolinha()
                                sobreviventesResgatados+=1
                                return
                        else: 
                            while 853.4 < c < 2700:
                                pegar_objeto_posicao()
                                c = sensor_cor.value()
                                tentativaPegarBolinha += 1
                                if c < 853.4:
                                    pegou_a_bolinha()
                                    sobreviventesResgatados+=1
                                    tentativaPegarBolinha += 1
                                    return
                                if tentativaPegarBolinha >= 1:
                                    tank_drive.on(SpeedPercent(0), SpeedPercent(0))
                                    tank_drive.on_for_seconds(SpeedPercent(0),SpeedPercent(0),0.01)
                                    tank_drive.on_for_seconds(SpeedPercent(-25),SpeedPercent(-25), 1.6)
                                    c = sensor_cor.value()
                                    break
                    tempo_total2 = time.time() + 4.5
                    while time.time() < tempo_total2:
                        c = sensor_cor.value()
                        tank_drive.on(SpeedPercent(-5), SpeedPercent(5)) 
                        if 853.4<c<2700:
                            tank_drive.on(SpeedPercent(0), SpeedPercent(0))
                            pegar_objeto_posicao()
                            c = sensor_cor.value()
                            if c < 853.4:
                                pegou_a_bolinha()
                                sobreviventesResgatados+=1
                                return
                        else: 
                            while 853.4 < c < 2700:
                                pegar_objeto_posicao()
                                c = sensor_cor.value()
                                tentativaPegarBolinha += 1
                                if c < 853.4:
                                    pegou_a_bolinha()
                                    sobreviventesResgatados+=1
                                    tentativaPegarBolinha += 1
                                    return
                                if tentativaPegarBolinha >= 1:
                                    tank_drive.on(SpeedPercent(0), SpeedPercent(0))
                                    tank_drive.on_for_seconds(SpeedPercent(0),SpeedPercent(0),0.01)
                                    tank_drive.on_for_seconds(SpeedPercent(-25),SpeedPercent(-25), 1.6)
                                    c = sensor_cor.value()
                                    break


        if sobreviventesResgatados<3:
             if 230<c<350:
                tempo_total = time.time()
                tank_drive.on(SpeedPercent(0), SpeedPercent(0))
                tank_drive.on_for_seconds(SpeedPercent(0),SpeedPercent(0),0.01)
                tank_drive.on(SpeedPercent(0), SpeedPercent(0))
                time.sleep(2)
                c = sensor_cor.value()
                if 230<c<350:
                    pegar_objeto_posicao()
                    c = sensor_cor.value()
                    if c < 230:
                        pegou_a_bolinha()
                        sobreviventesResgatados+=1
                        return
                    else: 
                        while 230 < c < 350:
                            pegar_objeto_posicao()
                            c = sensor_cor.value()
                            tentativaPegarBolinha += 1
                            if c < 230:
                                pegou_a_bolinha()
                                sobreviventesResgatados+=1
                                return
                            if tentativaPegarBolinha >= 1:
                                tank_drive.on(SpeedPercent(0), SpeedPercent(0))
                                tank_drive.on_for_seconds(SpeedPercent(0),SpeedPercent(0),0.01)
                                tank_drive.on_for_seconds(SpeedPercent(-25),SpeedPercent(-25), 1.6)
                                c = sensor_cor.value()
                                break
                else:
                    tempo_total2 = time.time() + 2.25
                    while time.time() < tempo_total2:
                        c = sensor_cor.value()
                        tank_drive.on(SpeedPercent(5), SpeedPercent(-5)) 
                        if 230<c<350:
                            tank_drive.on(SpeedPercent(0), SpeedPercent(0))
                            pegar_objeto_posicao()
                            c = sensor_cor.value()
                            if c < 230:
                                pegou_a_bolinha()
                                sobreviventesResgatados+=1
                                return
                        else: 
                            while 230 < c < 350:
                                pegar_objeto_posicao()
                                c = sensor_cor.value()
                                tentativaPegarBolinha += 1
                                if c < 230:
                                    pegou_a_bolinha()
                                    sobreviventesResgatados+=1
                                    tentativaPegarBolinha += 1
                                    return
                                if tentativaPegarBolinha >= 1:
                                    tank_drive.on(SpeedPercent(0), SpeedPercent(0))
                                    tank_drive.on_for_seconds(SpeedPercent(0),SpeedPercent(0),0.01)
                                    tank_drive.on_for_seconds(SpeedPercent(-25),SpeedPercent(-25), 1.6)
                                    c = sensor_cor.value()
                                    break
                    tempo_total2 = time.time() + 4.5
                    while time.time() < tempo_total2:
                        c = sensor_cor.value()
                        tank_drive.on(SpeedPercent(-5), SpeedPercent(5)) 
                        if 230<c<350:
                            tank_drive.on(SpeedPercent(0), SpeedPercent(0))
                            pegar_objeto_posicao()
                            c = sensor_cor.value()
                            if c < 230:
                                pegou_a_bolinha()
                                sobreviventesResgatados+=1
                                return
                        else: 
                            while 230 < c < 350:
                                pegar_objeto_posicao()
                                c = sensor_cor.value()
                                tentativaPegarBolinha += 1
                                if c < 230:
                                    pegou_a_bolinha()
                                    sobreviventesResgatados+=1
                                    tentativaPegarBolinha += 1
                                    return
                                if tentativaPegarBolinha >= 1:
                                    tank_drive.on(SpeedPercent(0), SpeedPercent(0))
                                    tank_drive.on_for_seconds(SpeedPercent(0),SpeedPercent(0),0.01)
                                    tank_drive.on_for_seconds(SpeedPercent(-25),SpeedPercent(-25), 1.6)
                                    c = sensor_cor.value()
                                    break

        elif sobreviventesResgatados>2:
            print("sai da salaaaaaaaaaaaaaaaaaaaaaa", file=sys.stderr)
            while True:
                tank_drive.on(SpeedPercent(30), SpeedPercent(-30))
                spkr.tone([(523.5, 200),(587.33, 400),(698.46, 200),(587.33, 200),(659.25, 400),(783.99, 200),(659.25, 200),(698.25, 400,800),])
        # elif 230 < c < 350 or 1050 < c < 2000 :                                                  #17:40          30 No AMbiente      35   Branco  
        #     tank_drive.on(SpeedPercent(0), SpeedPercent(0))
            # pegar_objeto_posicao()
            # print(c)
            # c = sensor_cor.value()
            # if c < 230:
            #     pegou_a_bolinha()
            # else: 
            #     while 230 < c < 350 or 1050 < c < 2000:
            #         tentativaPegarBolinha += 1
            #         pegar_objeto_posicao()
            #         c = sensor_cor.value()
            #         if tentativaPegarBolinha >= 4:
            #             tank_drive.on(SpeedPercent(0), SpeedPercent(0))
            #             tank_drive.on_for_seconds(SpeedPercent(-25),SpeedPercent(-25), 0.8)
            # break



        aux_verde = viu_verde(True)
        aux_vermelho = viu_vermelho()
        aux_preto = viu_preto()

        if (distancia < 140 and cond):              #Girar se ver uma parede ou se ver o chão da sala
            time.sleep(0.2)
            tempo_total = time.time()
            tank_drive.on(SpeedPercent(0), SpeedPercent(0))
            time.sleep(0.2)
            #if c > 400:
                #pegar_objeto_posicao()
                #pegou_a_bolinha()
            on_for_seconds(-25,-25,2.1, False)
            on_for_seconds(25,-25,0.95, False, True)
            break

        elif aux_preto[0] or aux_verde[0] or aux_vermelho[0]:
            tempo_total = time.time()             # Se ele viu preto
            tank_drive.on_for_seconds(SpeedPercent(0), SpeedPercent(0),0.01)
            #spkr.tone([(200, 350, 30)])
            tank_drive.on_for_seconds(SpeedPercent(-25),SpeedPercent(-25), 2)
            on_for_seconds(25,-5,2,True, True)
        

        #elif variancia < 2:
            #print(variancia, file=sys.stderr)
            #tank_drive.on_for_seconds(SpeedPercent(-50),SpeedPercent(-50), 0.8)
def Sala_Resgate():
    global tempo_total

    tempo_total = time.time()
    tempo_virada = 1
    velocidade_girada = 16
    while True:
        c = sensor_cor.value()
        distancia = dist.value()

        lista_distancia_baixo.pop(0)
        lista_distancia_cima.pop(0)
        lista_distancia_baixo.append(c)
        lista_distancia_cima.append(distancia)
        
        on_for_seconds(23,23,1.8)
        on_for_seconds(velocidade_girada,-velocidade_girada, tempo_virada,False)
        on_for_seconds(-velocidade_girada,velocidade_girada,tempo_virada*2,False)
        on_for_seconds(velocidade_girada,-velocidade_girada,tempo_virada,False)
        if time.time()-36 >= tempo_total:
            spkr.tone([(523.5, 200),(587.33, 400)])
            tank_drive.on_for_seconds(SpeedPercent(-25),SpeedPercent(-25), 1.5)
            on_for_seconds(25,-5,2,True, True)
            tempo_total = time.time()


def Sala_Resgate_2():                    #Implementação da sala de resgate com matriz
    sala = [[[],[],[]], [[],[],[]], [[],[],[]]]  #Primeiro quadrado é o da esquerda cima (a área de resgate padrão)
    tentativa = 0
    
    d = colordireito.value()
    e = coloresquerdo.value()
    distancia = dist.value()
    tank_drive.on_for_seconds(SpeedPercent(25),SpeedPercent(-25), 0.97)
    tentativa += 1
    while d > 30 and e > 30:
        d = colordireito.value()
        e = coloresquerdo.value()
        distancia = dist.value()
        tank_drive.on(SpeedPercent(20),SpeedPercent(20))
        if distancia < 130:
            tentativa+=1
            tank_drive.on_for_seconds(SpeedPercent(-25),SpeedPercent(25), 0.97)
    print(tentativa)
    tank_drive.on(SpeedPercent(0),(0))

    while True:
        pass
    


    
#///////////////////////////////////////////////////////////////////////////////////////////////////////////#



# Variaveis ////////////////////////////////////////////////////////////////////////////////////////////////#

# Módulos e suas portas -------------------------------------------------
MotorGarra = Motor(OUTPUT_D)
dist = UltrasonicSensor(INPUT_2)
coloresquerdo = ColorSensor(INPUT_3)
colordireito = ColorSensor(INPUT_4)
MotorBraço = Motor(OUTPUT_A)
tank_drive = MoveTank(OUTPUT_C, OUTPUT_B)  #C - Direita    B - Esquerda
sensor_cor = Sensor(INPUT_1)


# Parâmetros ------------------------------------------------------------
tempo_braço = 1                      #Tempo de subida da posição relaxada da garra para a posição abaixada
tempo_braço2 = 0.8                   # Tempo de subida/descida do braço
tempo_garra = 0.25                   # Tempo de abertura/fechamento da garra

num_amostras = 250                  # Número total de amostras que são guardadas na lista
num_amostras_seguemaior = 150        # Ao ver 2 pretos, quantas amostras são vistas antes para determinar se antes foi visto preto ou branco
num_amostras_menor = 10              # Quantas amostas são necessárias para identificar se foi visto um verde
num_amostras_segue = 1               # Quantas amostras são utilizadas para a execução do segue linha
num_amostras_verde = 35              # Ao ver verde, quantas amostras são vistas antes para determinar se antes foi visto preto ou branco
num_distancia = 40

BrancoEq = 53                 # O que diferencia o Preto do Branco no Segue Linha para o sensor direito
MediaPretoEq = 70.2 #69             # Valor que diferencia Preto do Branco na média dos valores utilizados após ver dois pretos pelo sensor esquerdo
BrancoDr = 70                 # O que diferencia o Preto do Branco no Segue Linha para o sensor esquerdo
MediaPretoDr = 90.5           # Valor que diferencia Preto do Branco na média dos valores utilizados após ver dois pretos pelo sensor direito



sobreviventesResgatados =0

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

spkr = Sound()

#///////////////////////////////////////////////////////////////////////////////////////////////////////////#


# Programa principal ///////////////////////////////////////////////////////////////////////////////////////#


a = time.time() + 30000

while a > time.time():

    # Variaveis -----------------------------------------------------------------
    e = coloresquerdo.value()  #Valores Lidos :Branco 73-77, Preto 6-8, Verde 4, Verm 55-57, Azul 5         
    d = colordireito.value()   #Valores Lidos :Branco 100, Preto 11, Verde 6-7,  Verm 73-75, Azul 8
    x+=1
    #print("Direita Verde3", d, "Esquerda Verde3", e, file=sys.stderr)
    

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
    #print("Cima", e, "Baixo", d, file=sys.stderr)
    if (e == 0 and d == 0) or False:
        tank_drive.on(SpeedPercent(0), SpeedPercent(0))
        c = sensor_cor.value()
        distancia = dist.value()
        e = coloresquerdo.value()
        d = colordireito.value()
        time.sleep(0.5)
        print("Cima", e, "Baixo", d, file=sys.stderr)

    elif viu_vermelho() == [True, 'Ambos']:
        tank_drive.on_for_seconds(SpeedPercent(0), SpeedPercent(0),0.01)
        spkr.tone([(900, 350, 30)])
        tank_drive.on_for_seconds(SpeedPercent(20), SpeedPercent(20),2)
        Sala_Resgate()
        c = sensor_cor.value()
        distancia = dist.value()
        tank_drive.on(SpeedPercent(0), SpeedPercent(0))
        print("Cima", distancia, "Baixo", c, file=sys.stderr)

    elif viu_verde():
        pass

    elif distancia <130:    #Se foi visto um obstáculo
        tank_drive.on(SpeedPercent(0), SpeedPercent(0))
        Obstaculo()

    else:
        Segue_linha()

print("----------------------------")
print("-   Expediente encerrado   -")
print("-     Leituras: ", x, "    -")
print("----------------------------")
tank_drive.on(SpeedPercent(0), SpeedPercent(0))

while True:
    pass

#///////////////////////////////////////////////////////////////////////////////////////////////////////////#