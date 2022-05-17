#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
#from ev3dev.ev3 import *
from ev3dev2.console import *


MotorGarra = Motor(OUTPUT_D)
t = TouchSensor(INPUT_4)
MotorBraço = Motor(OUTPUT_A)
tank_drive = MoveTank(OUTPUT_C, OUTPUT_B)
tempo_braço = 1
etapa = 1 # 1 - Subir a Garra         2 - Abrir a Garra              3 - Descer a Garra             4 - Fechar a Garra



MotorBraço.on_for_seconds(SpeedPercent(-20), tempo_braço)

while True:
    if t.is_pressed and etapa == 1:
        #Subir a Garra  
        MotorBraço.on_for_seconds(SpeedPercent(-20), tempo_braço)
        while (t.is_pressed):
            MotorBraço.on(SpeedPercent(0))
        print("Etapa 1", etapa)
        etapa +=1
    if t.is_pressed and etapa == 2:
        #Abrir a Garra
        MotorGarra.on_for_seconds(SpeedPercent(-15),0.5)
        while (t.is_pressed):
            MotorGarra.on(SpeedPercent(0))
        print("Etapa 2", etapa)
        etapa +=1
    if t.is_pressed and etapa == 3:
        #Descer a Garra
        MotorBraço.on_for_seconds(SpeedPercent(20),tempo_braço)
        while (t.is_pressed):
            MotorBraço.on(SpeedPercent(0))
        print("Etapa 3", etapa)
        etapa +=1
    if t.is_pressed and etapa == 4:
        #Fechar a Garra
        MotorGarra.on_for_seconds(SpeedPercent(15),0.67)
        while (t.is_pressed):
            MotorGarra.on(SpeedPercent(0))
        print("Etapa 4", etapa)
        etapa = 1


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


