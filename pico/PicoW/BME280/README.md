# Raspberry Pico with BME280 sensor Data Logger with Redis Integration

This project provides a Python script for the Raspberry Pi Pico W to read sensor data from a BME280 sensor (temperature, humidity, and pressure), and then send that data to a Redis database. The system also includes functionalities for Wi-Fi connection, error handling, and power-saving by entering light sleep mode.

## Features

- **Wi-Fi Connectivity**: Connects to a specified Wi-Fi network using credentials.
- **Sensor Data Collection**: Reads temperature, humidity, and pressure data from the BME280 sensor.
- **Redis Integration**: Sends collected sensor data to a Redis database using the HSET command.
- **Error Handling**: Implements error handling for sensor reading and Redis communication.
- **Power-Saving Mode**: Enters light sleep mode for a specified period to save power.

## Configuration

The following parameters can be configured:

- `WIFI_SSID`: SSID of the Wi-Fi network to connect to.
- `WIFI_PASSWORD`: Password of the Wi-Fi network.
- `REDIS_HOST`: IP address of the Redis server.
- `REDIS_PORT`: Port number of the Redis server (default is 6379).
- `REDIS_PASSWORD`: Password for Redis authentication.
- `REDIS_KEY`: Redis key to store the sensor data.

## How to Use

1. Clone the repository and upload the script to your Raspberry Pi Pico W.
2. Configure the Wi-Fi and Redis settings in the script.
3. Run the script to start collecting and sending data to Redis.
4. Monitor the sensor data in your Redis database.

## Code Overview

### Main Functions

- `connect_wifi()`: Connects to the Wi-Fi network.
- `read_sensor()`: Reads data from the BME280 sensor.
- `send_to_redis(data)`: Sends sensor data to the Redis database.
- `main()`: Main loop that handles Wi-Fi connection, data reading, data sending, and entering light sleep mode.

### Helper Functions

- `led_blinking(on_time, off_time, number_of_blinks)`: Controls the LED to indicate different statuses.
- `reset_bme280()`: Resets the BME280 sensor in case of errors.
