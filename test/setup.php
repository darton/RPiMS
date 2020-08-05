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

<?php $data = yaml_parse_file ("/home/pi/scripts/RPiMS/rpims.yaml");
$location = $data['setup']['location'];
$hostname = $data['setup']['hostname'];
$zabbix_server = $data['setup']['zabbix_server'];
$zabbix_server_active = $data['setup']['zabbix_server_active'];

$verbose = $data['setup']['verbose'];
$use_zabbix_sender = $data['setup']['use_zabbix_sender'];
$use_picamera = $data['setup']['use_picamera'];
$use_picamera_recording = $data['setup']['use_picamera_recording'];
$use_door_sensor = $data['setup']['use_door_sensor'];
$use_motion_sensor = $data['setup']['use_motion_sensor'];
$use_system_buttons = $data['setup']['use_system_buttons'];
$use_led_indicator = $data['setup']['use_led_indicator'];
$use_serial_display = $data['setup']['use_serial_display'];
$serial_display_refresh_rate = $data['setup']['serial_display_refresh_rate'];
$serial_display_type = $data['setup']['serial_display_type'];
$use_CPU_sensor = $data['setup']['use_CPU_sensor'];
$CPUtemp_read_interval = $data['setup']['CPUtemp_read_interval'];

$use_BME280_sensor = $data['setup']['use_BME280_sensor'];
$BME280_i2c_address = $data['setup']['BME280_i2c_address'];
$BME280_read_interval = $data['setup']['BME280_read_interval'];

$use_DS18B20_sensor = $data['setup']['use_DS18B20_sensor'];
$DS18B20_read_interval = $data['setup']['DS18B20_read_interval'];

$use_DHT_sensor = $data['setup']['use_DHT_sensor'];
$DHT_read_interval = $data['setup']['DHT_read_interval'];
$DHT_type = $data['setup']['DHT_type'];
$DHT_pin = $data['setup']['DHT_pin'];

?>



<label>Verbose: <input name="verbose" type="hidden" value="False"><input name="verbose" type="checkbox" <?php if ($verbose == 'yes') echo 'checked="checked"'; ?> value="True"></label><br />
<label>Use zabbix sender: <input name="use_zabbix_sender" type="hidden" value="False"><input name="use_zabbix_sender" type="checkbox" <?php if ($use_zabbix_sender == 'yes') echo 'checked="checked"'; ?> value="True"></label><br />
<label>Use picamera: <input name="use_picamera" type="hidden" value="False"><input name="use_picamera" type="checkbox" <?php if ($use_picamera == 'yes') echo 'checked="checked"'; ?> value="True"></label>
<label>Use picamera recording: <input name="use_picamera_recording" type="hidden" value="False"><input name="use_picamera_recording" type="checkbox" <?php if ($use_picamera_recording == 'yes') echo 'checked="checked"'; ?> value="True"></label><br />
<label>Use door sensor: <input name="use_door_sensor" type="hidden" value="False"><input name="use_door_sensor" type="checkbox" <?php if ($use_door_sensor == 'yes') echo 'checked="checked"'; ?> value="True"></label><br />
<label>Use motion sensor: <input name="use_motion_sensor" type="hidden" value="False"><input name="use_motion_sensor" type="checkbox" <?php if ($use_motion_sensor == 'yes') echo 'checked="checked"'; ?> value="True"></label><br />
<label>Use system buttons: <input name="use_system_buttons" type="hidden" value="False"><input name="use_system_buttons" type="checkbox" <?php if ($use_system_buttons == 'yes') echo 'checked="checked"'; ?> value="True"></label><br />
<label>Use led indicator: <input name="use_led_indicator" type="hidden" value="False"><input name="use_led_indicator" type="checkbox" <?php if ($use_led_indicator == 'yes') echo 'checked="checked"'; ?> value="True"></label><br />
<label>Use serial display: <input name="use_serial_display" type="hidden" value="False"><input name="use_serial_display" type="checkbox" <?php if ($use_serial_display == 'yes') echo 'checked="checked"'; ?> value="True"></label>
</div>

<label for="serial_display_type">Serial display type</label>
<select id="serial_display_type" name="serial_display_type">
<option value="oled_sh1106"<?php if ($serial_display_type == 'oled_sh1106') echo 'selected="selected"'; ?> >oled_sh1106</option>
<option value="lcd_st7735"<?php if ($serial_display_type == 'lcd_st7735') echo 'selected="selected"'; ?> >lcd_st7735</option>
</select>
<label>Serial display refresh rate: <input name="serial_display_refresh_rate" type="number" min="1" max="50" value=<?=$serial_display_refresh_rate?> size="2"></label><br />
</fieldset>
<br />

<fieldset>
<legend>Sensor configuration</legend>
<label>Use CPU sensor: <input name="use_CPU_sensor" type="hidden" value="False"><input name="use_CPU_sensor" type="checkbox" <?php if ($use_CPU_sensor == 'yes') echo 'checked="checked"'; ?> value="True"></label>
<label>CPUtemp read interval: <input name="CPUtemp_read_interval" type="number" min="1" max="3600" value=<?=$CPUtemp_read_interval?> size="4"></label><br />

<label>Use BME280 sensor: <input name="use_BME280_sensor" type="hidden" value="False"><input name="use_BME280_sensor" type="checkbox" <?php if ($use_BME280_sensor == 'yes') echo 'checked="checked"'; ?> value="True"></label>
<label>BME280 read interval: <input name="BME280_read_interval" type="number" min="1" max="3600" value=<?=$BME280_read_interval?> size="4"></label>
<label for="BME280_i2c_address">BME280_i2c_address:</label>
<select id="BME280_i2c_address" name="BME280_i2c_address">
<option value = 0x76 <?php if ($BME280_i2c_address == '118') echo 'selected="selected"'; ?> >0x76</option>
<option value = 0x77 <?php if ($BME280_i2c_address == '119') echo 'selected="selected"'; ?> >0x77</option>
</select>
<br />
<label>Use DS18B20 sensor: <input name="use_DS18B20_sensor" type="hidden" value="False"><input name="use_DS18B20_sensor" type="checkbox" <?php if ($use_DS18B20_sensor == 'yes') echo 'checked="checked"'; ?> value="True"></label>
<label>DS18B20 read interval: <input name="DS18B20_read_interval" type="number" min="1" max="3600" value=<?=$DS18B20_read_interval?> size="4"></label><br />

<label>Use DHT sensor: <input name="use_DHT_sensor" type="hidden" value="False"><input name="use_DHT_sensor" type="checkbox" <?php if ($use_DHT_sensor == 'yes') echo 'checked="checked"'; ?> value="True"></label>
<label>DHT read interval: <input name="DHT_read_interval" type="number" min="1" max="3600"  value=<?=$DHT_read_interval?> size="4"></label>
<label for="DHT_type">DHT type:</label>
<select id="DHT_type" name="DHT_type">
  <option value="DHT11" <?php if ($DHT_type == 'DHT11') echo 'selected="selected"'; ?> >DHT11</option>
  <option value="DHT22" <?php if ($DHT_type == 'DHT22') echo 'selected="selected"'; ?> >DHT22</option>
  <option value="AM2302" <?php if ($DHT_type == 'AM2302') echo 'selected="selected"'; ?> >AM2302</option>
</select>
<label for="DHT_pin">DHT pin:</label>
<select id="DHT_pin" name="DHT_pin">
  <option value = 18 <?php if ($DHT_pin == '18') echo 'selected="selected"'; ?> >18</option>
  <option value = 17 <?php if ($DHT_pin == '17') echo 'selected="selected"'; ?> >17</option>
</select><br />
</fieldset>
<br />

<fieldset>
<legend>Input configuration</legend>
<label for="GPIO_5">GPIO 5 input type:</label>
<select id="GPIO_5" name="GPIO_5" style="width: 125px;">
  <option value="Button">Door Sensor</option>
  <option selected value="MotionSensor">Motion Sensor</option>
</select>
<label>Hold Time: <input name="GPIO_5_hold_time" type="number" min="1" max="10"  value="1" size="2"></label>
<br />
<label for="GPIO_6">GPIO 6 input type:</label>
<select id="GPIO_6" name="GPIO_6" style="width: 125px;">
  <option value="Button">Door Sensor</option>
  <option selected value="MotionSensor">Motion Sensor</option>
</select>
<label>Hold Time: <input name="GPI0_6_hold_time" type="number" min="1" max="10"  value="1" size="2"></label>
<br />
<label for="GPIO_13">GPIO 13 input type:</label>
<select id="GPIO_13" name="GPIO_13" style="width: 125px;">
  <option value="Button">Door Sensor</option>
  <option selected value="MotionSensor">Motion Sensor</option>
</select>
<label>Hold Time: <input name="GPIO_13_hold_time" type="number" min="1" max="10"  value="1" size="2"></label>
<br />
<label for="GPIO_16">GPIO 16 input type:</label>
<select id="GPIO_16" name="GPIO_16" style="width: 125px;">
  <option value="Button">Door Sensor</option>
  <option selected value="Button">Shutdown Button</option>
  <option value="MotionSensor">Motion Sensor</option>
</select>
<label>Hold Time: <input name="GPIO_16_hold_time" type="number" min="1" max="10"  value="5" size="2"></label>
<br />

<label for="GPIO_17">GPIO 17 input type:</label>
<select id="GPIO_17" name="GPIO_17" style="width: 125px;">
  <option value="Button">Door Sensor</option>
  <option selected value="MotionSensor">Motion Sensor</option>
</select>
<label>Hold Time: <input name="GPIO_17_hold_time" type="number" min="1" max="10"  value="1" size="2"></label>
<br />
<label for="GPIO_19">GPIO 19 input type:</label>
<select id="GPIO_19" name="GPIO_19" style="width: 125px;">
  <option value="Button">Door Sensor</option>
  <option selected value="MotionSensor">Motion Sensor</option>
</select>
<label>Hold Time: <input name="GPIO_19_hold_time" type="number" min="1" max="10"  value="1" size="2"></label>
<br />
<label for="GPIO_20">GPIO 20 input type:</label>
<select id="GPIO_20" name="GPIO_20" style="width: 125px;">
  <option selected value="Button">Door Sensor</option>
  <option value="MotionSensor">Motion Sensor</option>
</select>
<label>Hold Time: <input name="GPIO_20_hold_time" type="number" min="1" max="10"  value="1" size="2"></label>
<br />
<label for="GPIO_21">GPIO 21 input type:</label>
<select id="GPIO_21" name="GPIO_21" style="width: 125px;">
  <option selected value="Button">Door Sensor</option>
  <option value="MotionSensor">Motion Sensor</option>
</select>
<label>Hold Time: <input name="GPIO_21_hold_time" type="number" min="1" max="10"  value="1" size="2"></label>
<br />
<label for="GPIO_26">GPIO 26 input type:</label>
<select id="GPIO_26" name="GPIO_26" style="width: 125px;">
  <option value="Button">Door Sensor</option>
  <option selected value="MotionSensor">Motion Sensor</option>
</select>
<label>Hold Time: <input name="GPIO_26_hold_time" type="number" min="1" max="10"  value="1" size="2"></label>
<br />
</fieldset>
<br />

<fieldset>
<legend>Output configuration</legend>
<label for="GPIO_12">GPIO 12:</label>
<select id="GPIO_12" name="GPIO_12" style="width: 125px;">
  <option value="motion_led">Motion Indicator</option>
  <option selected value="door_led">Door Indicator</option>
</select><br />
<label for="GPIO_18">GPIO 18:</label>
<select id="GPIO_18" name="GPIO_18" style="width: 125px;">
  <option selected value="motion_led">Motion Indicator</option>
  <option value="door_led">Door Indicator</option>
</select><br />
</fieldset>
<br />

<fieldset>
<legend>Zabbix Agent configuration</legend>
<label>Zabbix server:<input name="zabbix_server" type="text" size="30" placeholder="zabbix.example.com" value="<?=$zabbix_server?>" pattern="^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$"></label><br />
<label>Zabbix server Active:<input name="zabbix_server_active"  type="text" size="30" value="<?=$zabbix_server_active?>" placeholder="zabbix.example.com" pattern="^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$"></label><br />
<label>RPiMS location:<input name="location" type="text" size="30" value="<?=$location?>" ></label><br />
<label>RPiMS hostname:<input name="hostname" type="text" size="30" value="<?=$hostname?>" ></label><br />
</fieldset>
<br />
<input type="submit" value="Save">
</form>
</body>
</html>
