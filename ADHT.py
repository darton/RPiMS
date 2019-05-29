#!/usr/bin/python3

import redis
import Adafruit_DHT
import math
import numpy
import threading
from time import sleep

sensor = Adafruit_DHT.AM2302
gpiopin = 17

redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)

filtered_temperature = [] # here we keep the temperature values after removing outliers
filtered_humidity = [] # here we keep the filtered humidity values after removing the outliers

lock = threading.Lock() # we are using locks so we don't have conflicts while accessing the shared variables
event = threading.Event() # we are using an event so we can close the thread as soon as KeyboardInterrupt is raised

# function which eliminates the noise
# by using a statistical model
# we determine the standard normal deviation and we exclude anything that goes beyond a threshold
# think of a probability distribution plot - we remove the extremes
# the greater the std_factor, the more "forgiving" is the algorithm with the extreme values
def eliminateNoise(values, std_factor = 2):
    mean = numpy.mean(values)
    standard_deviation = numpy.std(values)

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
                [humidity, temp] = Adafruit_DHT.read_retry(sensor, gpiopin)

            except IOError:
                print("we've got IO error")

            if math.isnan(temp) == False and math.isnan(humidity) == False:
                values.append({"temp" : temp, "hum" : humidity})
                counter += 1

            sleep(2) # pause between measurements

        lock.acquire()
        filtered_temperature.append(numpy.mean(eliminateNoise([x["temp"] for x in values])))
        filtered_humidity.append(numpy.mean(eliminateNoise([x["hum"] for x in values])))
        lock.release()

        values = []

def Main():
    # here we start the thread
    # we use a thread in order to gather/process the data separately from the printing proceess
    data_collector = threading.Thread(target = readingValues)
    data_collector.start()
    while not event.is_set():
        if len(filtered_temperature) > 0: # or we could have used filtered_humidity instead
            lock.acquire()

            # here you can do whatever you want with the variables: print them, file them out, anything
            temperature = filtered_temperature.pop()
            humidity = filtered_humidity.pop()
            redis_db.set('Humidity', humidity)
            redis_db.set('Temperature', temperature)
            lock.release()
            sleep(1)
            event.set()


if __name__ == "__main__":
    try:
        Main()

    except KeyboardInterrupt:
        event.set()
