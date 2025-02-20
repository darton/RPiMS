import network
import socket
import json
from time import sleep
from picozero import pico_temp_sensor, pico_led
from machine import Pin, reset
from PicoDHT22 import PicoDHT22
    
location = "Room"
ssid = 'IoT'
password = 'verycomplexpassword'

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        pico_led.on()
        sleep(0.5)
        pico_led.off()
        sleep(0.5)
    pico_led.on()
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip


def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection


def webpage(location, temperature, humidity):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <meta name="viewport" content="width=device-width, initial-scale=2">
            <head>
            <p>Location: {location}</p>
            <p>Humidity is {humidity}%</p>
            <p>Temperature is {temperature}&deg;C</p>
            </body>
            </html>
            """
    return str(html)


def serve(connection):
    #Start a web server
    #location = "Room"
    t = 0
    h = 0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/sensors?':
            ''' request handler '''
            t,h = read_DHT()
            json_str = json.dumps({location:{"temperature": t, "humidity": h }})
            client.send("HTTP/1.1 200 OK\r\n")
            client.send("Content-Type: application/json\r\n\r\n")
            client.send(json_str)
        elif request == '/':
            ''' request handler '''
            t,h = read_DHT()
            html = webpage(location, t, h)
            client.send(html)
        client.close()


def read_DHT():
    DHT22_VCC = Pin(22, Pin.OUT)
    DHT_DATA_PIN = Pin(20,Pin.IN,Pin.PULL_UP)
    dht_sensor = PicoDHT22(DHT_DATA_PIN,DHT22_VCC,dht11=False)
    T,H = dht_sensor.read()
    print(T,H)
    return T,H

try:
    read_DHT()
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    reset()
except:
    sleep(5)
    exit
