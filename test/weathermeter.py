#!/usr/bin/env python3

import automationhat
from time import sleep, time

sleep(0.1)
start = time()

direction_mapr = {
"N": 5127,
"NNE": 5041,
"NE": 6421,
"ENE": 6240,
"E": 17786,
"ESE": 9267,
"SE": 11701,
"SSE": 7067,
"S": 8274,
"SSW": 5411,
"SW": 5589,
"W": 4820,
"WNW": 4776,
"NW" :4944,
"NNW": 4866
}


Uwe = 5.42
Uwy = 0
R1 = 4690
R2 = 0

while True:
    Uwy = automationhat.analog.one.read()
    Uwe = automationhat.analog.two.read()
    if Uwe != Uwy:
        R2 = int (Uwe/(Uwe - Uwy) * R1)
        print(R2,Uwe,Uwy)
    for item in direction_mapr:
        if (R2 <= direction_mapr.get(item) * 1.009) and (R2 >= direction_mapr.get(item) * 0.991):
            print(item)
    sleep(0.25)
