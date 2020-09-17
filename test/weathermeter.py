#!/usr/bin/env python3

import time
import automationhat

direction_mapr = {
"N": 5127,
"NE": 6437,
"E": 17692,
"SE": 11701,
"S": 8263,
"SW": 5589,
"W": 4820,
"NW": 4949
}


Uwe = 5.42
Uwy = 0
R1 = 4690
R2 = 0

while True:

    Uwy = automationhat.analog.one.read()
    Uwe = automationhat.analog.two.read()
    R2 = int (Uwe/(Uwe - Uwy) * R1)
    #print(R2,Uwe,Uwy)
    for item in direction_mapr:
        if (R2 <= direction_mapr.get(item) * 1.02) and (R2 >= direction_mapr.get(item) * 0.98):
            print(item)

    time.sleep(0.5)
