#!/usr/bin/env python3

import automationhat
from time import sleep, time
import redis
import math

sleep(0.1) # Delay for automationhat


def get_average(angles):
    sin_sum = 0.0
    cos_sum = 0.0

    for angle in angles:
        r = math.radians(angle)
        sin_sum += math.sin(r)
        cos_sum += math.cos(r)

    flen = float(len(angles))
    s = sin_sum / flen
    c = cos_sum / flen
    arc = math.degrees(math.atan(s / c))
    average = 0.0

    if s > 0 and c > 0:
        average = arc
    elif c < 0:
        average = arc + 180
    elif s < 0 and c > 0:
        average = arc + 360

    return 0.0 if average == 360 else average


def read_adc(adc_type):
    if adc_type == 'automationhat':
        adc_inputs_values = []
        adc_inputs_values.append(automationhat.analog.one.read())
        adc_inputs_values.append(automationhat.analog.two.read())
        adc_inputs_values.append(automationhat.analog.three.read())
        return adc_inputs_values


direction_mapr = {
"N": 5080,
"NNE": 5188,
"NE": 6417,
"ENE": 6253,
"E": 17419,
"ESE": 9380,
"SE": 11613,
"SSE": 6968,
"S": 8129,
"SSW": 5419,
"SW": 5542,
"W": 4781,
"NW": 4977,
"NNW": 4877,
}

direction_mapa = {
"N": 0,
"NNE": 22.5,
"NE": 45,
"ENE": 67.5,
"E": 90,
"ESE": 112.5,
"SE": 135,
"SSE": 157.5,
"S": 180,
"SSW": 202.5,
"SW": 225,
"W": 270,
"NW": 315,
"NNW": 337.5
}

Uwe = 5.2
Uwy = 0
R1 = 4690
R2 = 0
wind_direction_acquisition_time = 6
angles = []

redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)

while True:
    start_time = time()
    angles.clear()
    while time() - start_time <= wind_direction_acquisition_time:
        adc_values = read_adc('automationhat')
        Uwy = round(adc_values[0],1)
        Uwe = round(adc_values[1],1)
        if Uwe != Uwy:
            R2 = int (R1/(1 - Uwy/Uwe))
            #print(R2,Uwe,Uwy)
        for item in direction_mapr:
            if (R2 <= direction_mapr.get(item) * 1.005) and (R2 >= direction_mapr.get(item) * 0.995):
                angles.append(direction_mapa.get(item))
                average_wind_direction = int(round(get_average(angles),0))
                #print(direction_mapa.get(item), item)
    print("Average direction of wind: " + str(average_wind_direction))
    redis_db.mset({'average_wind_direction': average_wind_direction, 'wind_direction': item})
