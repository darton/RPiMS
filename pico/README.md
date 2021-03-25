# for RPi Pico

## Description
If you want to use BME280 sensor on long cable, copy two files from this repository to RPi Pico.

Connect the BME280 sensor to the i2C RPi Pico port.

Connect the RPi with the RPi Pico together with the USB cable.

Select serial as the interface type in RPiMS configuration for the BME280 sensor.

 - ### Temperature, Humidity, Pressure Sensor BME280
```
RPi Pico  [3V3  Pin 36]------------------------------ [VCC]  BME280
RPi Pico  [GP16 Pin 21] ----------------------------- [SDA]  BME280
RPi Pico  [GP17 Pin 22] ----------------------------- [SDC]  BME280
RPi Pico  [GND  Pin 23] ----------------------------- [GND]  BME280
```

```
BME280 [i2c] <------> [i2C] RPi Pico [USB] <----------------------------------->  RPi [USB]
```
