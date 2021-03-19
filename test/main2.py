# Based on:  https://www.raspberrypi.org/forums/viewtopic.php?t=302889
# USB serial communication for the Raspberry Pi Pico (RD2040) using the second RD2040
# thread/processor (written by Dorian Wiskow - Janaury 2021)

from sys import stdin, exit
from _thread import start_new_thread

# 
# global variables to share between both threads/processors
# 
bufferSize = 1024                 # size of circular buffer to allocate
buffer = [' '] * bufferSize       # circuolar incomming USB serial data buffer (pre fill)
bufferEcho = False                 # USB serial port echo incooming characters (True/False) 
bufferNextIn, bufferNextOut = 0,0 # pointers to next in/out character in circualr buffer
terminateThread = False           # tell 'bufferSTDIN' function to terminate (True/False)
#
# bufferSTDIN() function to execute in parallel on second Pico RD2040 thread/processor
#
def bufferSTDIN():
    global buffer, bufferSize, bufferEcho, bufferNextIn, terminateThread
    
    while True:                                 # endless loop
        if terminateThread:                     # if requested by main thread ...
            break                               #    ... exit loop
        buffer[bufferNextIn] = stdin.read(1)    # wait for/store next byte from USB serial
        if bufferEcho:                          # if echo is True ...
            print(buffer[bufferNextIn], end='') #    ... output byte to USB serial
        bufferNextIn += 1                       # bump pointer
        if bufferNextIn == bufferSize:          # ... and wrap, if necessary
            bufferNextIn = 0
#
# instantiate second 'background' thread on RD2040 dual processor to monitor and buffer
# incomming data from 'stdin' over USB serial port using ‘bufferSTDIN‘ function (above)
#
bufferSTDINthread = start_new_thread(bufferSTDIN, ())

#
# function to check if a byte is available in the buffer and if so, return it
#
def getByteBuffer():
    global buffer, bufferSize, bufferNextOut, bufferNextIn
    
    if bufferNextOut == bufferNextIn:           # if no unclaimed byte in buffer ...
        return ''                               #    ... return a null string
    n = bufferNextOut                           # save current pointer
    bufferNextOut += 1                          # bump pointer
    if bufferNextOut == bufferSize:             #    ... wrap, if necessary
        bufferNextOut = 0
    return (buffer[n])                          # return byte from buffer

#
# function to check if a line is available in the buffer and if so return it
# otherwise return a null string
#
# NOTE 1: a line is one or more bytes with the last byte being LF (\x0a)
#      2: a line containing only a single LF byte will also return a null string
#
def getLineBuffer():
    global buffer, bufferSize, bufferNextOut, bufferNextIn

    if bufferNextOut == bufferNextIn:           # if no unclaimed byte in buffer ...
        return ''                               #    ... RETURN a null string

    n = bufferNextOut                           # search for a LF in unclaimed bytes
    while n != bufferNextIn:
        if buffer[n] == '\x0a':                 # if a LF found ... 
            break                               #    ... exit loop ('n' pointing to LF)
        n += 1                                  # bump pointer
        if n == bufferSize:                     #    ... wrap, if necessary
            n = 0
    if (n == bufferNextIn):                     # if no LF found ...
            return ''                           #    ... RETURN a null string

    line = ''                                   # LF found in unclaimed bytes at pointer 'n'
    n += 1                                      # bump pointer past LF
    if n == bufferSize:                         #    ... wrap, if necessary
        n = 0

    while bufferNextOut != n:                   # BUILD line to RETURN until LF pointer 'n' hit
        
        if buffer[bufferNextOut] == '\x0d':     # if byte is CR
            bufferNextOut += 1                  #    bump pointer
            if bufferNextOut == bufferSize:     #    ... wrap, if necessary
                bufferNextOut = 0
            continue                            #    ignore (strip) any CR (\x0d) bytes
        
        if buffer[bufferNextOut] == '\x0a':     # if current byte is LF ...
            bufferNextOut += 1                  #    bump pointer
            if bufferNextOut == bufferSize:     #    ... wrap, if necessary
                bufferNextOut = 0
            break                               #    and exit loop, ignoring (i.e. strip) LF byte
        line = line + buffer[bufferNextOut]     # add byte to line
        bufferNextOut += 1                      # bump pointer
        if bufferNextOut == bufferSize:         #    wrap, if necessary
            bufferNextOut = 0
    return line                                 # RETURN unclaimed line of input

#
# main program begins here ...
#
# set 'inputOption' to either  one byte ‘BYTE’  OR one line ‘LINE’ at a time. Remember, ‘bufferEcho’
# determines if the background buffering function ‘bufferSTDIN’ should automatically echo each
# byte it receives from the USB serial port or not (useful when operating in line mode when the
# host computer is running a serial terminal program)
#
# start this MicroPython code running (exit Thonny with code still running) and then start a
# serial terminal program (e.g. putty, minicom or screen) on the host computer and connect
# to the Raspberry Pi Pico ...
#
#    ... start typing text and hit return.
#
#    NOTE: use Ctrl-C, Ctrl-C, Ctrl-D then Ctrl-B on in the host computer terminal program 
#           to terminate the MicroPython code running on the Pico 
#

from machine import Pin, I2C
from time import sleep
import BME280

sda = Pin(16)
scl = Pin(17)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=50000)
BME280_i2c_address = 0x77

try:
    inputOption = 'LINE'                    # get input from buffer one BYTE or LINE at a time
          
    while True:
        if inputOption == 'LINE':         # NON-BLOCKING input one line at a time (ending LF)
            buffLine = getLineBuffer()      # get a line if it is available?
        if buffLine == 'read_bme280':                    # if there is...
            bme = BME280.BME280(address=BME280_i2c_address,i2c=i2c)
            temp = bme.temperature
            hum = bme.humidity
            pres = bme.pressure
            print(temp,hum,pres)
        sleep(0.1)
        
except KeyboardInterrupt:                   # trap Ctrl-C input
    terminateThread = True                  # signal second 'background' thread to terminate 
    exit()
