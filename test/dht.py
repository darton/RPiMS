#!/usr/bin/python3

# based on Robert Lucian source code: https://forum.dexterindustries.com/t/solved-dht-sensor-occasionally-returning-spurious-values/2939/4
# https://forum.dexterindustries.com/t/noise-removal-algorithm-for-grove-dht-pro-sensor/2989?source_topic_id=3662

import math
import numpy
import redis
import threading
import adafruit_dht
from time import sleep
from datetime import datetime

pin = 17
dhtDevice = adafruit_dht.DHT22(pin)

#verbose yes/no - if yes, print Temperature and Humidity
verbose = "yes"
debug = "no"
redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)

filtered_temperature = [] # here we keep the temperature values after removing outliers
filtered_humidity = [] # here we keep the filtered humidity values after removing the outliers

lock = threading.Lock() # we are using locks so we don't have conflicts while accessing the shared variables
event = threading.Event() # we are using an event so we can close the thread as soon as KeyboardInterrupt is raised

# function which eliminates the noise by using a statistical model
# we determine the standard normal deviation and we exclude anything that goes beyond a threshold
# think of a probability distribution plot - we remove the extremes
# the greater the std_factor, the more "forgiving" is the algorithm with the extreme values
def eliminateNoise(values, std_factor = 1):
    mean = round(numpy.mean(values),3)
    standard_deviation = round(numpy.std(values),3)
    #print(standard_deviation)
    #print(mean)
    if standard_deviation == 0:
        return values

    final_values = [element for element in values if element > mean - std_factor * standard_deviation]
    final_values = [element for element in final_values if element < mean + std_factor * standard_deviation]

    return final_values

# function for processing the data
# filtering, periods of time, yada yada
def readingValues():
    number_of_measurements = 10
    values = []

    while not event.is_set():
        counter = 0
        while counter < number_of_measurements and not event.is_set():
            temp = None
            humidity = None
            try:
                temp = dhtDevice.temperature
                humidity = dhtDevice.humidity
            except RuntimeError as error:
                if debug is 'yes':
                    print(error.args[0])
                pass
            if (temp is not None and humidity is not None):
                values.append({"temp" : temp, "hum" : humidity})
                counter += 1
            sleep(3) # pause between measurements
        lock.acquire()
        #print(values)
        temp_value = numpy.mean(eliminateNoise([x["temp"] for x in values]))
        #print(temp_value)
        #filtered_temperature.append(numpy.mean(eliminateNoise([x["temp"] for x in values])))
        filtered_temperature.append(temp_value)
        hum_value = numpy.mean(eliminateNoise([x["hum"] for x in values]))
        #print(hum_value)
        #filtered_humidity.append(numpy.mean(eliminateNoise([x["hum"] for x in values])))
        filtered_humidity.append(hum_value)
        #print(filtered_temperature)
        #print("---")
        #print(filtered_humidity)
        lock.release()
        values = []

def Main():
    # here we start the thread
    # we use a thread in order to gather/process the data separately from the printing proceess
    data_collector = threading.Thread(target = readingValues)
    data_collector.start()
    while not event.is_set():
        if len(filtered_temperature) > 0 :
            lock.acquire()
            temperature = filtered_temperature.pop()
            humidity = filtered_humidity.pop()
            if temperature < 100.0 and humidity < 100:
                redis_db.mset({'DHT22_Humidity' : humidity,'DHT22_Temperature' : temperature})
                if verbose is 'yes' :
                    print('{}, Temperature: {:.02f}°C, Humidity: {:.02f}%' .format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), temperature, humidity))
            lock.release()
        sleep(1)
    data_collector.join()

if __name__ == "__main__":
    try:
        Main()

    except KeyboardInterrupt:
        event.set()
