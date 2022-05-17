#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from ev3dev.ev3 import *
coloresquerdo = ColorSensor(INPUT_3)
colordireito = ColorSensor(INPUT_4)
tank_drive = MoveTank(OUTPUT_C, OUTPUT_B)
dist = UltrasonicSensor(INPUT_2)
bot = TouchSensor(INPUT_1)

def botao():
    apertos = 0
    while True: 
        if bot.is_pressed():
            apertos += 1
        print(apertos)

def Segue_linha2():
    e = coloresquerdo.value()
    d = colordireito.value()
    if e > 80 and d <= 30: 
        tank_drive.on(SpeedPercent(-23),SpeedPercent(43))
    elif e <= 30 and d > 80:
        tank_drive.on(SpeedPercent(43),SpeedPercent(-23))
    elif e > 80 and d > 80:
        tank_drive.on(SpeedPercent(25), SpeedPercent(25))
    else:
        tank_drive.on(SpeedPercent(15), SpeedPercent(-15))
    print("Esquerda", e ,"Direita", d)



def Segue_linha():
    e = coloresquerdo.value()
    d = colordireito.value()
    if e > 80 and d <= 30: 
        tank_drive.on(SpeedPercent(-25),SpeedPercent(45))
    elif e <= 30 and d > 80:
        tank_drive.on(SpeedPercent(45),SpeedPercent(-25))
    elif e > 80 and d > 80:
        tank_drive.on(SpeedPercent(30), SpeedPercent(30))
    elif 55>e>30 and 55>d>30:
        tank_drive.on(SpeedPercent(0), SpeedPercent(0))
        if bot.value():
            tank_drive.on_for_seconds(SpeedPercent(25), SpeedPercent(25),0.5)
            while True:
                Segue_linha2()
    else:
        tank_drive.on(SpeedPercent(-10), SpeedPercent(10))
    print("Esquerda", e ,"Direita", d)

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

while True:
    e = coloresquerdo.value()
    d = colordireito.value()
    distancia = dist.value()
    print("Esquerda: ", e, "Direita: ", d, "Distancia: ", distancia)

    if distancia < 60:
        Obstaculo()
    Segue_linha()