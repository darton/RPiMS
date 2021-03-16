<!DOCTYPE html>
<html lang="en">

<head>
<title>RPiMS configuration</title>
<meta charset="utf-8" name="viewport" content="width=device-width, initial-scale=1"/>
<link rel="stylesheet" href="w3.css">

<style>
.w3-table {
  background-color: #f1f1c1;
}

.gpioinputs {
  padding:8px;
  display:block;
  border:none;
  border-bottom:1px solid #ccc;
  width:100%
}
</style>
<script src="../jquery.min.js"></script>
<script src="setup.js" defer></script>
</head>

<body>
<div>

<form action="setup_form.php" method="post">

<fieldset>
<legend>System configuration</legend>
<div>
<table class="w3-table">

<tr>
<td>
<label>Verbose:</label>
</td>
<td>
<input name="verbose" type="hidden" value="no"><input name="verbose" type="checkbox" class="w3-check" <?php if ($verbose) echo 'checked="checked"'; ?> value="True">
</td>
</tr>

<tr>
<td>
<label>Use zabbix sender:</label>
</td>
<td>
<input name="use_zabbix_sender" type="hidden" value="False"><input name="use_zabbix_sender" type="checkbox" class="w3-check" <?php if ($use_zabbix_sender == 'yes') echo 'checked="checked"'; ?> value="True">
</td>
</tr>

<tr>
<td>
<label>Use picamera:</label>
</td>
<td>
<input name="use_picamera" type="hidden" value="False"><input name="use_picamera" type="checkbox" class="w3-check" <?php if ($use_picamera == 'yes') echo 'checked="checked"'; ?> value="True">
</td>
</tr>

<tr>
<td>
<label>Use picamera recording:</label>
</td>
<td>
<input name="use_picamera_recording" type="hidden" value="False"><input name="use_picamera_recording" type="checkbox" class="w3-check"  <?php if ($use_picamera_recording == 'yes') echo 'checked="checked"'; ?> value="True">
</td>
</tr>

<tr>
<td>
<label>Use button sensors:</label>
</td>
<td>
<input name="use_door_sensor" type="hidden" value="False"><input name="use_door_sensor" type="checkbox" class="w3-check" <?php if ($use_door_sensor == 'yes') echo 'checked="checked"'; ?> value="True">
</td>
</tr>

<tr>
<td>
<label>Use motion sensors:</label>
</td>
<td>
<input name="use_motion_sensor" type="hidden" value="False"><input name="use_motion_sensor" type="checkbox" class="w3-check" <?php if ($use_motion_sensor == 'yes') echo 'checked="checked"'; ?> value="True">
</td>
</tr>

<tr>
<td>
<label>Use CPU sensor:</label>
</td>
<td>
<input name="use_CPU_sensor" type="hidden" value="False"><input name="use_CPU_sensor" type="checkbox" class="w3-check" <?php if ($use_CPU_sensor == 'yes') echo 'checked="checked"'; ?> value="True">
</td>
</tr>

<tr>
<td>
<label>Use BME280 sensor:</label>
</td>
<td>
<input name="use_BME280_sensor" type="hidden" value="False"><input name="use_BME280_sensor" type="checkbox" class="w3-check" <?php if ($use_BME280_sensor == 'yes') echo 'checked="checked"'; ?> value="True">
</td>
</tr>

<tr>
<td>
<label>Use DS18B20 sensor:</label>
</td>
<td>
<input name="use_DS18B20_sensor" type="hidden" value="False"><input name="use_DS18B20_sensor" type="checkbox" class="w3-check" <?php if ($use_DS18B20_sensor == 'yes') echo 'checked="checked"'; ?> value="True">
</td>
</tr>

<tr>
<td>
<label>Use DHT sensor:</label>
</td>
<td>
<input name="use_DHT_sensor" type="hidden" value="False"><input name="use_DHT_sensor" type="checkbox" class="w3-check" <?php if ($use_DHT_sensor) echo 'checked="checked"'; ?> value="True">
</td>
</tr>

<tr>
<td>
<label>Use weather station:</label>
</td>
<td>
<input name="use_weather_station" type="hidden" value="False"><input name="use_weather_station" type="checkbox" class="w3-check" <?php if ($use_weather_station) echo 'checked="checked"'; ?> value="True">
</td>
</tr>

<tr>
<td>
<label>Use serial display:</label>
</td>
<td>
<input name="use_serial_display" type="hidden" value="False"><input name="use_serial_display" type="checkbox" class="w3-check" <?php if ($use_serial_display == 'yes') echo 'checked="checked"'; ?> value="True">
</td>
</tr>

<tr>
<td>
<label>Serial display</label>
</td>
</tr>
<tr>
<td>
<label for="serial_type">Serial type:</label>
<select id="serial_type" name="serial_type" class="w3-select">
<option value="i2c"<?php if ($serial_type == 'i2c') echo 'selected="selected"'; ?> >i2c</option>
<option value="spi"<?php if ($serial_type == 'spi') echo 'selected="selected"'; ?> >spi</option>
</select>
</td>
<td>
<label for="serial_display_type">Display type:</label>
<select id="serial_display_type" name="serial_display_type" class="w3-select">
<option value="oled_sh1106"<?php if ($serial_display_type == 'oled_sh1106') echo 'selected="selected"'; ?> >oled_sh1106</option>
<option value="lcd_st7735"<?php if ($serial_display_type == 'lcd_st7735') echo 'selected="selected"'; ?> >lcd_st7735</option>
</select>
</td>
<td>
<label for="serial_display_rotate">Display rotate:</label>
<select id="serial_display_rotate" name="serial_display_rotate" class="w3-select">
<option value="0"<?php if ($serial_display_rotate == '0') echo 'selected="selected"'; ?> >0</option>
<option value="2"<?php if ($serial_display_rotate == '2') echo 'selected="selected"'; ?> >180</option>
</select>
</td>
<td>
<label>Refresh rate:</label>
<input name="serial_display_refresh_rate" class="w3-select" type="number" min="1" max="50" value="<?= $serial_display_refresh_rate ?>" >
</td>
</tr>

</table>
</div>
</fieldset>


<fieldset>
<legend>Sensor configuration</legend>
<div>
<table class="w3-table">

<tr>
<td>
<label for="CPUtemp_read_interval">CPUtemp read interval:</label>
<input name="CPUtemp_read_interval" class="w3-input" id="CPUtemp_read_interval" type="number" min="1" max="3600" value="<?= $CPUtemp_read_interval ?>" >
</td>
</tr>

<tr>
<td>
<label>DS18B20</label>
</td>
</tr>
<tr>
<td>
<label for="DS18B20_read_interval">read interval:</label>
<input name="DS18B20_read_interval" class="w3-input" id="DS18B20_read_interval" type="number" min="1" max="3600" value="<?= $DS18B20_read_interval ?>" >
</td>
</tr>

<tr>
<td>
<label>BME280</label>
</td>
</tr>
<tr>
<td>
<label for="BME280_read_interval">Read interval:</label>
<input name="BME280_read_interval" class="w3-input" id="BME280_read_interval" type="number" min="1" max="3600" value="<?= $BME280_read_interval ?>" >
</td>
<td>
<label for="BME280_interface">Interface type:</label>
<select name="BME280_interface" class="w3-input" id="BME280_interface">
<option <?php if ($BME280_interface == 'i2c') echo 'selected="selected"'; ?> value = "i2c" >i2c</option>
<option <?php if ($BME280_interface == 'serial') echo 'selected="selected"'; ?> value = "serial" >serial</option>
</select>
</td>
<td>
<label id="BME280_i2c_address">I2c address:
<select name="BME280_i2c_address" class="w3-input" >
<option <?php if ($BME280_i2c_address == '118') echo 'selected="selected"'; ?> value = "118" >0x76</option>
<option <?php if ($BME280_i2c_address == '119') echo 'selected="selected"'; ?> value = "119" >0x77</option>
</select>
</label>
</td>
</tr>


<tr>
<td>
<label>DHT</label>
</td>
</tr>
<tr>
<td>
<label for="DHT_read_interval">Read interval:</label>
<input name="DHT_read_interval" class="w3-input" id="DHT_read_interval" type="number" min="1" max="3600" value="<?= $DHT_read_interval ?>" >
</td>

<td>
<label for="DHT_type">Type:</label>
  <select name="DHT_type" class="w3-input" id="DHT_type">
  <option value="DHT11" <?php if ($DHT_type == 'DHT11') echo 'selected="selected"'; ?> >DHT11</option>
  <option value="DHT22" <?php if ($DHT_type == 'DHT22') echo 'selected="selected"'; ?> >DHT22</option>
  <option value="AM2302" <?php if ($DHT_type == 'AM2302') echo 'selected="selected"'; ?> >AM2302</option>
</select>
</td>

<td>
<label for="DHT_pin">Pin:</label>
<select name="DHT_pin" class="w3-input" id="DHT_pin">
  <option value = 17>17</option>
</select>
</td>
</tr>

<tr>
<td>
<label>Rainfall</label>
</td>
</tr>
<tr>
<td>
<label for="rainfall_acquisition_time">Aquisition time:</label>
<input name="rainfall_acquisition_time" class="w3-input" id="rainfall_acquisition_time" type="number" min="1" max="3600" value="<?= $rainfall_acquisition_time ?>" >
</td>
<td>
<label for="rainfall_agregation_time">Agregation time:</label>
<input name="rainfall_agregation_time" class="w3-input" id="rainfall_agregation_time" type="number" min="1" max="86400" value="<?= $rainfall_agregation_time ?>" >
</td>
<td>
<label for="rainfall_sensor_pin">Sensor pin:</label>
<select  name="rainfall_sensor_pin" class="w3-select" id="rainfall_sensor_pin">
  <option value = 22>22</option>
</select>
</td>
</tr>


<tr>
<td>
<label>Wind speed</label>
</td>
</tr>
<tr>
<td>
<label for="windspeed_acquisition_time">Acquisition time:</label>
<input name="windspeed_acquisition_time" class="w3-input" id="windspeed_acquisition_time" type="number" min="1" max="3600" value="<?= $windspeed_acquisition_time ?>" >
</td>
<td>
<label for="windspeed_agregation_time">Agregation time:</label>
<input name="windspeed_agregation_time" class="w3-input" id="windspeed_agregation_time" type="number" min="1" max="3600" value="<?= $windspeed_agregation_time ?>" >
</td>
<td>
<label for="windspeed_sensor_pin">Sensor pin:</label>
<select name="windspeed_sensor_pin" class="w3-select" id="windspeed_sensor_pin">
  <option value = 23>23</option>
</select>
</td>
</tr>

<tr>
<td>
<label>Wind direction</label>
</td>
<tr>
<tr>
<td>
<label for="winddirection_acquisition_time">Acquisition time:</label>
<input name="winddirection_acquisition_time" class="w3-input" id="winddirection_acquisition_time" type="number" min="1" max="3600" value="<?= $winddirection_acquisition_time ?>" >
</td>
</tr>
<tr>
<td>
<label for="winddirection_adc_type">ADC type:</label>
<select name="winddirection_adc_type" class="w3-select" id="winddirection_adc_type">
 <option value="AutomationPhat" <?php if ($winddirection_adc_type == 'AutomationPhat') echo 'selected="selected"'; ?> >AutomationPhat</option>
 <option value="STM32F030" <?php if ($winddirection_adc_type == 'STM32F030') echo 'selected="selected"'; ?> >STM32F030</option>
 <option value="ADS1115" <?php if ($winddirection_adc_type == 'ADS1115') echo 'selected="selected"'; ?> >ADS1115</option>
</select>
</td>
<td>
<label for="winddirection_adc_input">Sensor input:</label>
<select name="winddirection_adc_input" class="w3-select" id="winddirection_adc_input">
 <option value="1" <?php if ($winddirection_adc_input == '1') echo 'selected="selected"'; ?> >1</option>
 <option value="2" <?php if ($winddirection_adc_input == '2') echo 'selected="selected"'; ?> >2</option>
 <option value="3" <?php if ($winddirection_adc_input == '3') echo 'selected="selected"'; ?> >3</option>
 <option value="4" <?php if ($winddirection_adc_input == '4') echo 'selected="selected"'; ?> >4</option>
</select>
</td>
<td>
<label for="_adc_input">Reference input:</label>
<select name="reference_voltage_adc_input" class="w3-select" id="reference_voltage_adc_input">
 <option value="1" <?php if ($reference_voltage_adc_input == '1') echo 'selected="selected"'; ?> >1</option>
 <option value="2" <?php if ($reference_voltage_adc_input == '2') echo 'selected="selected"'; ?> >2</option>
 <option value="3" <?php if ($reference_voltage_adc_input == '3') echo 'selected="selected"'; ?> >3</option>
 <option value="4" <?php if ($reference_voltage_adc_input == '4') echo 'selected="selected"'; ?> >4</option>
</select>
</td>
</tr>

</table>
</div>
</fieldset>


<fieldset>
<legend>Input configuration</legend>
<div>
<table class="w3-table">

<tr>
<td>
<label>GPIO 5<input name="GPIO_5[gpio_pin]" type="hidden" value="5"></label>
</td>
</tr>
<tr>
<td>
<label for="GPIO_5">Input type:</label>
<select name="GPIO_5[type]" class="gpioinputs" id="GPIO_5_TYPE">
  <option <?php if ($GPIO['GPIO_5']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Button</option>
  <option <?php if ($GPIO['GPIO_5']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
  <option <?php if ($GPIO['GPIO_5']['type'] == 'Reserved') echo 'selected="selected"'; ?> value="Reserved">Reserved</option>
</select>
</td>
<td><label>Name: <input name="GPIO_5[name]" class="w3-input" type="text" value="<?=$GPIO['GPIO_5']['name']?>"></label></td>
<td><label id="GPIO_5_TYPE_DS">Hold time: <input id="GPIO_5_TYPE_DS_HT" name="GPIO_5[hold_time]" class="w3-input" type="number" min="1" max="60" value="<?=$GPIO['GPIO_5']['hold_time']?>"></label></td>
</tr>

<tr>
<td>
<label>GPIO 6<input name="GPIO_6[gpio_pin]" type="hidden" value="6"></label>
</td>
</tr>
<tr>
<td>
<label for="GPIO_6">Input type:</label>
<select name="GPIO_6[type]" class="gpioinputs" id="GPIO_6_TYPE">
  <option <?php if ($GPIO['GPIO_6']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Button</option>
  <option <?php if ($GPIO['GPIO_6']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
  <option <?php if ($GPIO['GPIO_6']['type'] == 'Reserved') echo 'selected="selected"'; ?> value="Reserved">Reserved</option>
</select>
</td>
<td><label>Name: <input name="GPIO_6[name]" class="w3-input" type="text" value="<?=$GPIO['GPIO_6']['name']?>"></label></td>
<td><label id="GPIO_6_TYPE_DS">Hold time: <input id="GPIO_6_TYPE_DS_HT" name="GPIO_6[hold_time]" class="w3-input" type="number" min="1" max="60" value="<?=$GPIO['GPIO_6']['hold_time']?>"></label></td>
</tr>

<tr>
<td>
<label>GPIO 13<input name="GPIO_13[gpio_pin]" type="hidden" value="13"></label>
</td>
</tr>
<tr>
<td>
<label for="GPIO_13">Input type:</label>
<select name="GPIO_13[type]" class="gpioinputs" id="GPIO_13_TYPE">
  <option <?php if ($GPIO['GPIO_13']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Button</option>
  <option <?php if ($GPIO['GPIO_13']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
  <option <?php if ($GPIO['GPIO_13']['type'] == 'Reserved') echo 'selected="selected"'; ?> value="Reserved">Reserved</option>
</select>
</td>
<td><label>Name: <input name="GPIO_13[name]" class="w3-input" type="text" value="<?=$GPIO['GPIO_13']['name']?>"></label></td>
<td><label id="GPIO_13_TYPE_DS">Hold time: <input id="GPIO_13_TYPE_DS_HT" name="GPIO_13[hold_time]" class="w3-input" type="number" min="1" max="60" value="<?=$GPIO['GPIO_13']['hold_time']?>"></label></td>
</tr>

<tr>
<td>
<label>GPIO 16<input name="GPIO_16[gpio_pin]" type="hidden" value="16"></label>
</td>
</tr>
<tr>
<td><label for="GPIO_16">Input type:</label>
<select name="GPIO_16[type]" class="gpioinputs" id="GPIO_16_TYPE">
  <option <?php if ($GPIO['GPIO_16']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Button</option>
  <option <?php if ($GPIO['GPIO_16']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
  <option <?php if ($GPIO['GPIO_16']['type'] == 'Reserved') echo 'selected="selected"'; ?> value="Reserved">Reserved</option>
  <option <?php if ($GPIO['GPIO_16']['type'] == 'ShutdownButton') echo 'selected="selected"'; ?> value="ShutdownButton">Shutdown Button</option>
</select></td>
<td><label>Name: <input name="GPIO_16[name]" class="w3-input" type="text" value="<?=$GPIO['GPIO_16']['name']?>"></label></td>
<td><label id="GPIO_16_TYPE_DS">Hold time: <input id="GPIO_16_TYPE_DS_HT" name="GPIO_16[hold_time]" class="w3-input" type="number" min="1" max="60" value="<?=$GPIO['GPIO_16']['hold_time']?>"></label></td>
</tr>

<tr>
<td>
<label>GPIO 19<input name="GPIO_19[gpio_pin]" type="hidden" value="19"></label>
</td>
</tr>
<tr>
<td>
<label for="GPIO_19">Input type:</label>
<select name="GPIO_19[type]" class="gpioinputs" id="GPIO_19_TYPE">
  <option <?php if ($GPIO['GPIO_19']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Button</option>
  <option <?php if ($GPIO['GPIO_19']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
  <option <?php if ($GPIO['GPIO_19']['type'] == 'Reserved') echo 'selected="selected"'; ?> value="Reserved">Reserved</option>
</select>
</td>
<td><label>Name: <input name="GPIO_19[name]" class="w3-input" type="text" value="<?=$GPIO['GPIO_19']['name']?>"></label></td>
<td><label id="GPIO_19_TYPE_DS">Hold time: <input id="GPIO_19_TYPE_DS_HT" name="GPIO_19[hold_time]" class="w3-input" type="number" min="1" max="60" value="<?=$GPIO['GPIO_19']['hold_time']?>"></label></td>
</tr>

<tr>
<td>
<label>GPIO 20<input name="GPIO_20[gpio_pin]" type="hidden" value="20"></label>
</td>
</tr>
<tr>
<td>
<label for="GPIO_20">Input type:</label>
<select name="GPIO_20[type]" class="gpioinputs" id="GPIO_20_TYPE">
  <option <?php if ($GPIO['GPIO_20']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Button</option>
  <option <?php if ($GPIO['GPIO_20']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
  <option <?php if ($GPIO['GPIO_20']['type'] == 'Reserved') echo 'selected="selected"'; ?> value="Reserved">Reserved</option>
</select>
</td>
<td><label>Name: <input name="GPIO_20[name]" class="w3-input" type="text" value="<?=$GPIO['GPIO_20']['name']?>"></label></td>
<td><label id="GPIO_20_TYPE_DS">Hold time: <input id="GPIO_20_TYPE_DS_HT" name="GPIO_20[hold_time]" class="w3-input" type="number" min="1" max="60" value="<?=$GPIO['GPIO_20']['hold_time']?>"></label></td>
</tr>

<tr>
<td>
<label>GPIO 21<input name="GPIO_21[gpio_pin]" type="hidden" value="21"></label>
</td>
</tr>
<tr>
<td>
<label for="GPIO_21">Input type:</label>
<select name="GPIO_21[type]" class="gpioinputs" id="GPIO_21_TYPE">
  <option <?php if ($GPIO['GPIO_21']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Button</option>
  <option <?php if ($GPIO['GPIO_21']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
  <option <?php if ($GPIO['GPIO_21']['type'] == 'Reserved') echo 'selected="selected"'; ?> value="Reserved">Reserved</option>
</select>
</td>
<td><label>Name: <input name="GPIO_21[name]" class="w3-input" type="text" value="<?=$GPIO['GPIO_21']['name']?>"></label></td>
<td><label id="GPIO_21_TYPE_DS">Hold time: <input id="GPIO_21_TYPE_DS_HT" name="GPIO_21[hold_time]" class="w3-input" type="number" min="1" max="60" value="<?=$GPIO['GPIO_21']['hold_time']?>"></label></td>
</tr>

<tr>
<td>
<label>GPIO 26<input name="GPIO_26[gpio_pin]" type="hidden" value="26"></label>
</td>
</tr>
<tr>
<td>
<label for="GPIO_26">Input type:</label>
<select name="GPIO_26[type]" class="gpioinputs" id="GPIO_26_TYPE">
  <option <?php if ($GPIO['GPIO_26']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Button</option>
  <option <?php if ($GPIO['GPIO_26']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
  <option <?php if ($GPIO['GPIO_26']['type'] == 'Reserved') echo 'selected="selected"'; ?> value="Reserved">Reserved</option>
</select>
</td>
<td><label>Name: <input name="GPIO_26[name]" class="w3-input" type="text" value="<?=$GPIO['GPIO_26']['name']?>"></label></td>
<td><label id="GPIO_26_TYPE_DS">Hold time: <input id="GPIO_26_TYPE_DS_HT" name="GPIO_26[hold_time]" class="w3-input" type="number" min="1" max="60" value="<?=$GPIO['GPIO_26']['hold_time']?>"></label></td>
</tr>

</table>
</div>
</fieldset>


<fieldset>
<legend>Output configuration</legend>
<div>
<table class="w3-table">
<tr>
<td>
<label for="GPIO_12">GPIO 12<input name="GPIO_12[gpio_pin]" type="hidden" value="12"></label>
</td>
</tr>

<tr>
<td>
<label for="GPIO_12">Output type:</label>
<select  name="GPIO_12[type]" class="w3-input" id="GPIO_12">
  <option <?php if ($GPIO['GPIO_12']['type'] == 'door_led') echo 'selected="selected"'; ?> value="door_led">Door Indicator</option>
  <option <?php if ($GPIO['GPIO_12']['type'] == 'led') echo 'selected="selected"'; ?>value="led">LED</option>
</select></td>
<td><label>Name: <input name="GPIO_12[name]" class="w3-input" type="text" value="<?=$GPIO['GPIO_12']['name']?>"></label></td>
</tr>
<tr>
<td>
<label for="GPIO_18">GPIO 18<input name="GPIO_18[gpio_pin]" type="hidden" value="18"></label>
</td>
</tr>
<tr>
<td>
<label for="GPIO_18">Output type:</label>
<select  name="GPIO_18[type]" class="w3-input" id="GPIO_18">
  <option <?php if ($GPIO['GPIO_18']['type'] == 'motion_led') echo 'selected="selected"'; ?> value="motion_led">Motion Indicator</option>
  <option <?php if ($GPIO['GPIO_18']['type'] == 'led') echo 'selected="selected"'; ?>value="led">LED</option>
</select></td>
<td><label>Name: <input name="GPIO_18[name]" class="w3-input" type="text" value="<?=$GPIO['GPIO_18']['name']?>"></label></td>
</tr>
</table>
</div>
</fieldset>

<fieldset>
<legend>Zabbix Agent configuration</legend>
<div>
<table class="w3-table">

<tr>
<td>
<label>Zabbix server:</label>
<input name="zabbix_server" class="w3-input" type="text" placeholder="zabbix.example.com" value="<?=$zabbix_server?>" pattern="^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$">
</td>
</tr>

<tr>
<td>
<label>Zabbix server Active:</label>
<input name="zabbix_server_active" class="w3-input" type="text" value="<?=$zabbix_server_active?>" placeholder="zabbix.example.com" pattern="^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$">
</td>
</tr>

<tr>
<td>
<label>RPiMS location:</label>
<input name="location" class="w3-input" type="text" value="<?=$location?>" >
</td>
</tr>

<tr>
<td>
<label>RPiMS hostname:</label>
<input name="hostname" class="w3-input" type="text" value="<?=$hostname?>" >
</td>
</tr>

<tr>
<td>
<label>PSK identity:</label>
<input name="TLSPSKIdentity" class="w3-input" id="TLSPSKIdentity" type="text" value="<?=$TLSPSKIdentity?>">
<input class="w3-input" type="button" onclick="gfg_Run(16,tlspskidentityid)" value="Generate PSK Identity">
</td>
</tr>

<tr>
<td>
<label>PSK:</label>
<input name="TLSPSK" class="w3-input" id="TLSPSK" type="text" value="<?=$TLSPSK?>" >
<input class="w3-input" type="button" onclick="gfg_Run(64,tlspskid)" value="Generate PSK">
</td>
</tr>

<tr>
<td>
<label>Timeout:</label>
<input name="Timeout" class="w3-input" type="number" min="1" max="10" value="<?=$Timeout?>" >
</td>
</tr>

</table>
</div>
</fieldset>

<fieldset>
<div>
<input type="submit" value="Save" class="w3-bar">
</div>
</fieldset>

</form>

</div>
</body>
</html>
