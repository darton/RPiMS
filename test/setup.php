<!DOCTYPE html>
<html lang="en">

<head>
<title>RPiMS configuration</title>
<meta charset="utf-8"/>
</head>

<body>
<fieldset>
<legend>System configuration</legend>
<form action="/form.php" method="post">
<label>Verbose:<input name="verbose" type="hidden" value="False"><input name="verbose" type="checkbox" value="True"></label><br />
<label>Use zabbix sender:<input name="use_zabbix_sender" type="hidden" value="False"><input name="use_zabbix_sender" type="checkbox" value="True"></label><br />
<label>Use picamera:<input name="use_picamera" type="hidden" value="False"><input name="use_picamera" type="checkbox" value="True"></label>
<label>Use picamera recording:<input name="use_picamera_recording" type="hidden" value="False"><input name="use_picamera_recording" type="checkbox" value="True"></label><br />
<label>Use door sensor:<input name="use_door_sensor" type="hidden" value="False"><input name="use_door_sensor" type="checkbox" value="True"></label><br />
<label>Use motion sensor:<input name="use_motion_sensor" type="hidden" value="False"><input name="use_motion_sensor" type="checkbox" value="True"></label><br />
<label>Use system buttons:<input name="use_system_buttons" type="hidden" value="False"><input name="use_system_buttons" type="checkbox" value="True"></label><br />
<label>Use led indicator:<input name="use_led_indicator" type="hidden" value="False"><input name="use_led_indicator" type="checkbox" value="True"></label><br />
<label>Use serial display:<input name="use_serial_display" type="hidden" value="False"><input name="use_serial_display" type="checkbox" value="True"></label>
</div>
<label for="werial_display_type">Serial display type</label>
<select id="serial_display_type" name="serial_display_type">
  <option selected value="oled_sh1106">oled_sh1106</option>
  <option value="lcd_st7735">lcd_st7735</option>
</select>
<label>Serial display refresh rate: <input name="serial_display_refresh_rate" type="number" min="1" max="50" value="1" size="2"></label><br />
</fieldset>
<br />

<fieldset>
<legend>Sensor configuration</legend>
<label>Use CPU sensor: <input name="use_CPU_sensor" type="hidden" value="False"><input name="use_cpu_sensor" type="checkbox" value="True"></label>
<label>CPUtemp read interval: <input name="CPUtemp_read_interval" type="number" min="1" max="3600" value="1" size="4"></label><br />
<label>Use BME280 sensor: <input name="use_BME280_sensor" type="hidden" value="False"><input name="use_BME280_sensor" type="checkbox" value="True"></label>
<label>BME280 read interval: <input name="BME280_read_interval" type="number" min="1" max="3600" value="10" size="4"></label><br />
<label>Use DS18B20 sensor: <input name="use_DS18B20_sensor" type="hidden" value="False"><input name="use_DS18B20_sensor" type="checkbox" value="True"></label>
<label>DS18B20 read interval: <input name="DS18B20_read_interval" type="number" min="1" max="3600" value="60" size="4"></label><br />
<label>Use DHT sensor: <input name="use_DHT_sensor" type="hidden" value="False"><input name="use_DHT_sensor" type="checkbox" value="True"></label>
<label>DHT read interval: <input name="DHT_read_interval" type="number" min="1" max="3600"  value="5" size="4"></label>
<label for="DHT_type">DHT type:</label>
<select id="DHT_type" name="DHT_type">
  <option value="DHT11">DHT11</option>
  <option selected value="DHT22">DHT22</option>
  <option value="AM2302">AM2302</option>
</select><br />
</fieldset>
<br />

<fieldset>
<legend>Input configuration</legend>
<label for="GPIO_5">GPIO 5</label>
<select id="GPIO_5" name="GPIO_5">
  <option value="Button">Door Sensor</option>
  <option selected value="MotionSensor">Motion Sensor</option>
</select><br />
<label for="GPIO_6">GPIO 6</label>
<select id="GPIO_6" name="GPIO_6">
  <option value="Button">Door Sensor</option>
  <option selected value="MotionSensor">Motion Sensor</option>
</select><br />
<label for="GPIO_13">GPIO 13</label>
<select id="GPIO_13" name="GPIO_13">
  <option value="Button">Door Sensor</option>
  <option selected value="MotionSensor">Motion Sensor</option>
</select><br />
<label for="GPIO_16">GPIO 16</label>
<select id="GPIO_16" name="GPIO_16">
  <option value="Button">Door Sensor</option>
  <option selected value="MotionSensor">Motion Sensor</option>
</select><br />
<label for="GPIO_17">GPIO 17</label>
<select id="GPIO_17" name="GPIO_17">
  <option value="Door_Sensor">Door Sensor</option>
  <option selected value="MotionSensor">Motion Sensor</option>
</select><br />
<label for="GPIO_19">GPIO 19</label>
<select id="GPIO_19" name="GPIO_19">
  <option value="Button">Door Sensor</option>
  <option selected value="MotionSensor">Motion Sensor</option>
</select><br />
<label for="GPIO_20">GPIO 20</label>
<select id="GPIO_20" name="GPIO_20">
  <option selected value="Button">Door Sensor</option>
  <option value="MotionSensor">Motion Sensor</option>
</select><br />
<label for="GPIO_21">GPIO 21</label>
<select id="GPIO_21" name="GPIO_21">
  <option selected value="Button">Door Sensor</option>
  <option value="MotionSensor">Motion Sensor</option>
</select><br />
<label for="GPIO_26">GPIO 26</label>
<select id="GPIO_26" name="GPIO_26">
  <option value="Button">Door Sensor</option>
  <option selected value="MotionSensor">Motion Sensor</option>
</select><br />
</fieldset>
<br />

<fieldset>
<legend>Output configuration</legend>
<label for="GPIO_12">GPIO 12</label>
<select id="GPIO_12" name="GPIO_12"  >
  <option value="motion_led">Motion Indicator</option>
  <option selected value="door_led">Door Indicator</option>
</select><br />
<label for="GPIO_18">GPIO 18</label>
<select id="GPIO_18" name="GPIO_18" name>
  <option selected value="motion_led">Motion Indicator</option>
  <option value="door_led">Door Indicator</option>
</select><br />
</fieldset>
<br />

<fieldset>
<legend>Zabbix Agent configuration</legend>
<label>Zabbix server:<input name="zabbix_server" type="text" placeholder="zabbix.example.com" pattern="^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$"></label><br />
<label>Zabbix server Active:<input name="zabbix_server_active" type="text" placeholder="zabbix.example.com" pattern="^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$"></label><br />
<label>RPiMS location:<input name="location" type="text" value="My Home"></label><br />
<label>RPiMS hostname:<input name="hostname" type="text" value="rpims"></label><br />
</fieldset>
<br />
<input type="submit" value="Save">
</form>
</body>
</html>
