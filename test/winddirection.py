#!/usr/bin/env python3

import automationhat
from time import sleep
import redis

sleep(0.1)

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
"W": 280,
"NW": 315,
"NNW": 337.5
}


Uwe = 5.2
Uwy = 0
R1 = 4690
R2 = 0
angles = []

redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)


while True:
    Uwy = round(automationhat.analog.one.read(),1)
    Uwe = round(automationhat.analog.two.read(),1)
    if Uwe != Uwy:
        R2 = int (Uwe/(Uwe - Uwy) * R1)
        print(R2,Uwe,Uwy)
    for item in direction_mapr:
        if (R2 <= direction_mapr.get(item) * 1.005) and (R2 >= direction_mapr.get(item) * 0.995):
            angles.append(direction_mapa.get(item))
            print(item)
            print(str(direction_mapa.get(item)))
            print(angles)
            redis_db.set('wind_direction', item)
    sleep(0.1)
