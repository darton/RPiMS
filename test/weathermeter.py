#!/usr/bin/env python3

import automationhat
import redis
from time import sleep, time

sleep(0.1)
start = time()

direction_mapr = {
"N": 5080,
"NNE": 5188,
"NE": 6417,
"ENE": 6253,
"E": 17419,
"SE": 11613,
"ESE": 9380,
"SSE": 6968,
"S": 8129,
"SSW": 5419,
"SW": 5542,
"W": 4781,
"NW": 4977,
"NNW": 4877,
}

Uwe = 0
Uwy = 0
R1 = 4690
R2 = 0

redis_db = redis.StrictRedis(host="localhost", port=6379, db=1, charset="utf-8", decode_responses=True)
redis_db.flushdb()

while True:
    Uwy = round(automationhat.analog.one.read(),1)
    Uwe = round(automationhat.analog.two.read(),1)
    if Uwe != Uwy:
        R2 = int (Uwe/(Uwe - Uwy) * R1)
        #print(R2,Uwe,Uwy)
    for item in direction_mapr:
        if (R2 <= direction_mapr.get(item) * 1.005) and (R2 >= direction_mapr.get(item) * 0.995):
            print(item)
            redis_db.set('wind_direction', item)
    sleep(0.1)
