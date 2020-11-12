<!DOCTYPE html>
<html lang="en">
<head>
<title>RPiMS configuration</title>
<meta charset="utf-8"/>
<link rel="stylesheet" href="w3.css">
<style>
#t01 {
  width: 100%;
  background-color: #f1f1c1;
}
</style>
<script src="../jquery.min.js"></script>
<script src="setup.js" defer></script>
</head>

<body>
<div class="w3-responsive">
<form action="setup_form.php" method="post" class="w3-container">
<fieldset>
<legend>System configuration</legend>
<table id="t01" class="w3-table">
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
<label>Use led indicators:</label>
</td>
<td>
<input name="use_led_indicators" type="hidden" value="False"><input name="use_led_indicators" type="checkbox" class="w3-check" <?php if ($use_led_indicators == 'yes') echo 'checked="checked"'; ?> value="True">
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
<label for="serial_display_type">Serial display type</label>
</td>
<td>
<select id="serial_display_type" name="serial_display_type" class="w3-select">
<option value="oled_sh1106"<?php if ($serial_display_type == 'oled_sh1106') echo 'selected="selected"'; ?> >oled_sh1106</option>
<option value="lcd_st7735"<?php if ($serial_display_type == 'lcd_st7735') echo 'selected="selected"'; ?> >lcd_st7735</option>
</select>
</td>
<td>
<label for="serial_type">Serial type</label>
</td>
<td>
<select id="serial_type" name="serial_type" class="w3-select">
<option value="i2c"<?php if ($serial_type == 'i2c') echo 'selected="selected"'; ?> >i2c</option>
<option value="spi"<?php if ($serial_type == 'spi') echo 'selected="selected"'; ?> >spi</option>
</select>
</td>
<td>
<label for="serial_display_rotate">Serial display rotate</label>
</td>
<td>
<select id="serial_display_rotate" name="serial_display_rotate" class="w3-select">
<option value="0"<?php if ($serial_display_rotate == '0') echo 'selected="selected"'; ?> >0</option>
<option value="2"<?php if ($serial_display_rotate == '2') echo 'selected="selected"'; ?> >180</option>
</select>
</td>

<td>
<label>Serial display refresh rate:</label>
</td>
<td>
<input name="serial_display_refresh_rate" type="number" min="1" max="50" size="2" value="<?= $serial_display_refresh_rate ?>" >
</td>
</tr>
</table>
</fieldset>


<fieldset>
<legend>Sensor configuration</legend>
<table id="t01" class="w3-table">
<tr><td>
<label>CPUtemp read interval:</label>
</td>
<td>
<input name="CPUtemp_read_interval" type="number" min="1" max="3600" class="w3-input" size="4" value="<?= $CPUtemp_read_interval ?>" >
</td></tr>

<tr><td>
<label>DS18B20 read interval:</label>
</td>
<td>
<input name="DS18B20_read_interval" class="w3-input" type="number" min="1" max="3600" size="4" value="<?= $DS18B20_read_interval ?>" >
</td></tr>

<tr><td>
<label>BME280 read interval:</label>
</td>
<td>
<input name="BME280_read_interval" type="number" min="1" max="3600" class="w3-input" size="4" value="<?= $BME280_read_interval ?>" >
</td>
<td>
<label for="BME280_i2c_address">BME280_i2c_address:</label>
</td>
<td>
<select id="BME280_i2c_address" name="BME280_i2c_address" class="w3-select" >
<option <?php if ($BME280_i2c_address == '118') echo 'selected="selected"'; ?> value = "118" >0x76</option>
<option <?php if ($BME280_i2c_address == '119') echo 'selected="selected"'; ?> value = "119" >0x77</option>
</select>
</td></tr>

<tr><td>
<label>DHT read interval:</label>
</td><td>
<input name="DHT_read_interval" class="w3-input" type="number" min="1" max="3600" size="4" value="<?= $DHT_read_interval ?>" >
</td>
<td>
<label for="DHT_type">DHT type:</label>
</td>
<td>
<select id="DHT_type" name="DHT_type" class="w3-select">
  <option value="DHT11" <?php if ($DHT_type == 'DHT11') echo 'selected="selected"'; ?> >DHT11</option>
  <option value="DHT22" <?php if ($DHT_type == 'DHT22') echo 'selected="selected"'; ?> >DHT22</option>
  <option value="AM2302" <?php if ($DHT_type == 'AM2302') echo 'selected="selected"'; ?> >AM2302</option>
</select>
</td>
<td>
<label for="DHT_pin">DHT pin:</label>
</td>
<td>
<select id="DHT_pin" name="DHT_pin" class="w3-select">
  <option value = 17>17</option>
</select>
</td></tr>


<tr>
<td><label>Rainfall aquisition time:</label></td>
<td><input name="rainfall_acquisition_time" class="w3-input" type="number" min="1" max="3600" size="4" value="<?= $rainfall_acquisition_time ?>" ></td>
<td><label>Rainfall agregation time:</label></td>
<td><input name="rainfall_agregation_time" class="w3-input" type="number" min="1" max="86400" size="4" value="<?= $rainfall_agregation_time ?>" ></td>
<td><label for="rainfall_sensor_pin">Rainfall sensor pin:</label></td>
<td><select id="rainfall_sensor_pin" name="rainfall_sensor_pin" class="w3-select">
  <option value = 22>22</option>
</select></td>
</tr>


<tr>
<td><label>Wind speed acquisition time:</label></td>
<td><input name="windspeed_acquisition_time" class="w3-input" type="number" min="1" max="3600" size="4" value="<?= $windspeed_acquisition_time ?>" ></td>

<td><label>Wind speed agregation time:</label></td>
<td><input name="windspeed_agregation_time" class="w3-input" type="number" min="1" max="3600" size="4" value="<?= $windspeed_agregation_time ?>" ></td>

<td><label for="windspeed_sensor_pin">Wind speed sensor pin:</label></td>
<td><select id="windspeed_sensor_pin" name="windspeed_sensor_pin" class="w3-select">
  <option value = 23>23</option>
</select></td>
</tr>

<tr>
<td><label>Wind direction acquisition time:</label></td>
<td><input name="winddirection_acquisition_time" class="w3-input" type="number" min="1" max="3600" size="4" value="<?= $winddirection_acquisition_time ?>" ></td>

<td><label for="winddirection_adc_type">Wind direction ADC type:</label></td>
<td><select id="winddirection_adc_type" name="winddirection_adc_type" class="w3-select">
 <option value="AutomationPhat" <?php if ($winddirection_adc_type == 'AutomationPhat') echo 'selected="selected"'; ?> >AutomationPhat</option>
 <option value="STM32F030" <?php if ($winddirection_adc_type == 'STM32F030') echo 'selected="selected"'; ?> >STM32F030</option>
 <option value="ADS1115" <?php if ($winddirection_adc_type == 'ADS1115') echo 'selected="selected"'; ?> >ADS1115</option>
</select></td>

<td><label for="winddirection_adc_input">Wind direction ADC input:</label></td>
<td><select id="winddirection_adc_input" name="winddirection_adc_input" class="w3-select">
 <option value="1" <?php if ($winddirection_adc_input == '1') echo 'selected="selected"'; ?> >1</option>
 <option value="2" <?php if ($winddirection_adc_input == '2') echo 'selected="selected"'; ?> >2</option>
 <option value="3" <?php if ($winddirection_adc_input == '3') echo 'selected="selected"'; ?> >3</option>
 <option value="4" <?php if ($winddirection_adc_input == '4') echo 'selected="selected"'; ?> >4</option>
</select></td>

<td><label for="_adc_input">Reference voltage ADC input:</label></td>
<td><select id="reference_voltage_adc_input" name="reference_voltage_adc_input" class="w3-select">
 <option value="1" <?php if ($reference_voltage_adc_input == '1') echo 'selected="selected"'; ?> >1</option>
 <option value="2" <?php if ($reference_voltage_adc_input == '2') echo 'selected="selected"'; ?> >2</option>
 <option value="3" <?php if ($reference_voltage_adc_input == '3') echo 'selected="selected"'; ?> >3</option>
 <option value="4" <?php if ($reference_voltage_adc_input == '4') echo 'selected="selected"'; ?> >4</option>
</select></td>
</tr>



</table>
</fieldset>


<fieldset>
<legend>Input configuration</legend>
<table id="t01" class="w3-table">

<tr>
<td><label>GPIO 5<input name="GPIO_5[gpio_pin]" type="hidden" value="5"></label></td>
<td>
<label for="GPIO_5">Input type:</label>
<select id="GPIO_5_TYPE" name="GPIO_5[type]" style="width: 160px;"  class="gpioinputs">
  <option <?php if ($GPIO['GPIO_5']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Button</option>
  <option <?php if ($GPIO['GPIO_5']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
  <option <?php if ($GPIO['GPIO_5']['type'] == 'Reserved') echo 'selected="selected"'; ?> value="Reserved">Reserved</option>
</select>
</td>
<td><label>Name: <input name="GPIO_5[name]" type="text" value="<?=$GPIO['GPIO_5']['name']?>" size="30"></label></td>
<td><label id="GPIO_5_TYPE_DS">Hold time: <input id="GPIO_5_TYPE_DS_HT" name="GPIO_5[hold_time]" type="number" min="1" max="60" value="<?=$GPIO['GPIO_5']['hold_time']?>" size="2"></label></td>
</tr>

<tr>
<td><label>GPIO 6<input name="GPIO_6[gpio_pin]" type="hidden" value="6"></label></td>
<td>
<label for="GPIO_6">Input type:</label>
<select id="GPIO_6_TYPE" name="GPIO_6[type]" style="width: 160px;" class="gpioinputs">
  <option <?php if ($GPIO['GPIO_6']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Button</option>
  <option <?php if ($GPIO['GPIO_6']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
  <option <?php if ($GPIO['GPIO_6']['type'] == 'Reserved') echo 'selected="selected"'; ?> value="Reserved">Reserved</option>
</select>
</td>
<td><label>Name: <input name="GPIO_6[name]" type="text" value="<?=$GPIO['GPIO_6']['name']?>" size="30"></label></td>
<td><label id="GPIO_6_TYPE_DS">Hold time: <input id="GPIO_6_TYPE_DS_HT" name="GPIO_6[hold_time]" type="number" min="1" max="60" value="<?=$GPIO['GPIO_6']['hold_time']?>" size="2"></label></td>
</tr>

<tr>
<td><label>GPIO 13<input name="GPIO_13[gpio_pin]" type="hidden" value="13"></label></td>
<td>
<label for="GPIO_13">Input type:</label>
<select id="GPIO_13_TYPE" name="GPIO_13[type]" style="width: 160px;" class="gpioinputs">
  <option <?php if ($GPIO['GPIO_13']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Button</option>
  <option <?php if ($GPIO['GPIO_13']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
  <option <?php if ($GPIO['GPIO_13']['type'] == 'Reserved') echo 'selected="selected"'; ?> value="Reserved">Reserved</option>
</select>
</td>
<td><label>Name: <input name="GPIO_13[name]" type="text" value="<?=$GPIO['GPIO_13']['name']?>" size="30"></label></td>
<td><label id="GPIO_13_TYPE_DS">Hold time: <input id="GPIO_13_TYPE_DS_HT" name="GPIO_13[hold_time]" type="number" min="1" max="60" value="<?=$GPIO['GPIO_13']['hold_time']?>" size="2"></label></td>
</tr>

<tr>
<td><label>GPIO 16<input name="GPIO_16[gpio_pin]" type="hidden" value="16"></label></td>
<td>
<label for="GPIO_16">Input type:</label>
<select id="GPIO_16_TYPE" name="GPIO_16[type]" style="width: 160px;" class="gpioinputs">
  <option <?php if ($GPIO['GPIO_16']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Button</option>
  <option <?php if ($GPIO['GPIO_16']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
  <option <?php if ($GPIO['GPIO_16']['type'] == 'Reserved') echo 'selected="selected"'; ?> value="Reserved">Reserved</option>
  <option <?php if ($GPIO['GPIO_16']['type'] == 'ShutdownButton') echo 'selected="selected"'; ?> value="ShutdownButton">Shutdown Button</option>
</select>
</td>
<td><label>Name: <input name="GPIO_16[name]" type="text" value="<?=$GPIO['GPIO_16']['name']?>" size="30"></label></td>
<td><label id="GPIO_16_TYPE_DS">Hold time: <input id="GPIO_16_TYPE_DS_HT" name="GPIO_16[hold_time]" type="number" min="1" max="60" value="<?=$GPIO['GPIO_16']['hold_time']?>" size="2"></label></td>
</tr>

<tr>
<td><label>GPIO 19<input name="GPIO_19[gpio_pin]" type="hidden" value="19"></label></td>
<td>
<label for="GPIO_19">Input type:</label>
<select id="GPIO_19_TYPE" name="GPIO_19[type]" style="width: 160px;" class="gpioinputs">
  <option <?php if ($GPIO['GPIO_19']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Button</option>
  <option <?php if ($GPIO['GPIO_19']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
  <option <?php if ($GPIO['GPIO_19']['type'] == 'Reserved') echo 'selected="selected"'; ?> value="Reserved">Reserved</option>
</select>
</td>
<td><label>Name: <input name="GPIO_19[name]" type="text" value="<?=$GPIO['GPIO_19']['name']?>" size="30"></label></td>
<td><label id="GPIO_19_TYPE_DS">Hold time: <input id="GPIO_19_TYPE_DS_HT" name="GPIO_19[hold_time]" type="number" min="1" max="60" value="<?=$GPIO['GPIO_19']['hold_time']?>" size="2"></label></td>
</tr>


<tr>
<td><label>GPIO 20<input name="GPIO_20[gpio_pin]" type="hidden" value="20"></label></td>
<td>
<label for="GPIO_20">Input type:</label>
<select id="GPIO_20_TYPE" name="GPIO_20[type]" style="width: 160px;" class="gpioinputs">
  <option <?php if ($GPIO['GPIO_20']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Button</option>
  <option <?php if ($GPIO['GPIO_20']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
  <option <?php if ($GPIO['GPIO_20']['type'] == 'Reserved') echo 'selected="selected"'; ?> value="Reserved">Reserved</option>
</select>
</td>
<td><label>Name: <input name="GPIO_20[name]" type="text" value="<?=$GPIO['GPIO_20']['name']?>" size="30"></label></td>
<td><label id="GPIO_20_TYPE_DS">Hold time: <input id="GPIO_20_TYPE_DS_HT" name="GPIO_20[hold_time]" type="number" min="1" max="60" value="<?=$GPIO['GPIO_20']['hold_time']?>" size="2"></label></td>
</tr>


<tr>
<td><label>GPIO 21<input name="GPIO_21[gpio_pin]" type="hidden" value="21"></label></td>
<td>
<label for="GPIO_21">Input type:</label>
<select id="GPIO_21_TYPE" name="GPIO_21[type]" style="width: 160px;" class="gpioinputs">
  <option <?php if ($GPIO['GPIO_21']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Button</option>
  <option <?php if ($GPIO['GPIO_21']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
  <option <?php if ($GPIO['GPIO_21']['type'] == 'Reserved') echo 'selected="selected"'; ?> value="Reserved">Reserved</option>
</select>
</td>
<td><label>Name: <input name="GPIO_21[name]" type="text" value="<?=$GPIO['GPIO_21']['name']?>" size="30"></label></td>
<td><label id="GPIO_21_TYPE_DS">Hold time: <input id="GPIO_21_TYPE_DS_HT" name="GPIO_21[hold_time]" type="number" min="1" max="60" value="<?=$GPIO['GPIO_21']['hold_time']?>" size="2"></label></td>
</tr>

<!--
<tr>
<td><label>GPIO 22<input name="GPIO_22[gpio_pin]" type="hidden" value="22"></label></td>
<td>
<label for="GPIO_22">Input type:</label>
<select id="GPIO_22_TYPE" name="GPIO_22[type]" style="width: 160px;" class="gpioinputs">
  <option <?php if ($GPIO['GPIO_22']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Button</option>
  <option <?php if ($GPIO['GPIO_22']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
  <option <?php if ($GPIO['GPIO_22']['type'] == 'Reserved') echo 'selected="selected"'; ?> value="Reserved">Reserved</option>
</select>
</td>
<td><label>Name: <input name="GPIO_22[name]" type="text" value="<?=$GPIO['GPIO_22']['name']?>" size="30"></label></td>
<td><label id="GPIO_22_TYPE_DS">Hold time: <input id="GPIO_22_TYPE_DS_HT" name="GPIO_22[hold_time]" type="number" min="1" max="60" value="<?=$GPIO['GPIO_22']['hold_time']?>" size="2"></label></td>
</tr>

<tr>
<td><label>GPIO 23<input name="GPIO_23[gpio_pin]" type="hidden" value="23"></label></td>
<td>
<label for="GPIO_23">Input type:</label>
<select id="GPIO_23_TYPE" name="GPIO_23[type]" style="width: 160px;" class="gpioinputs">
  <option <?php if ($GPIO['GPIO_23']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Button</option>
  <option <?php if ($GPIO['GPIO_23']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
  <option <?php if ($GPIO['GPIO_23']['type'] == 'Reserved') echo 'selected="selected"'; ?> value="Reserved">Reserved</option>
</select>
</td>
<td><label>Name: <input name="GPIO_23[name]" type="text" value="<?=$GPIO['GPIO_23']['name']?>" size="30"></label></td>
<td><label id="GPIO_23_TYPE_DS">Hold time: <input id="GPIO_23_TYPE_DS_HT" name="GPIO_23[hold_time]" type="number" min="1" max="60" value="<?=$GPIO['GPIO_23']['hold_time']?>" size="2"></label></td>
</tr>
-->
<tr>
<td><label>GPIO 26<input name="GPIO_26[gpio_pin]" type="hidden" value="26"></label></td>
<td>
<label for="GPIO_26">Input type:</label>
<select id="GPIO_26_TYPE" name="GPIO_26[type]" style="width: 160px;" class="gpioinputs">
  <option <?php if ($GPIO['GPIO_26']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Button</option>
  <option <?php if ($GPIO['GPIO_26']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
  <option <?php if ($GPIO['GPIO_26']['type'] == 'Reserved') echo 'selected="selected"'; ?> value="Reserved">Reserved</option>
</select>
</td>
<td><label>Name: <input name="GPIO_26[name]" type="text" value="<?=$GPIO['GPIO_26']['name']?>" size="30"></label></td>
<td><label id="GPIO_26_TYPE_DS">Hold time: <input id="GPIO_26_TYPE_DS_HT" name="GPIO_26[hold_time]" type="number" min="1" max="60" value="<?=$GPIO['GPIO_26']['hold_time']?>" size="2"></label></td>
</tr>

</table>
</fieldset>


<fieldset>
<legend>Output configuration</legend>
<table id="t01" class="w3-table">
<tr>
<td><label for="GPIO_12">GPIO 12<input name="GPIO_12[gpio_pin]" type="hidden" value="12"></label></td>
<td>
<label for="GPIO_12">Output type:</label>
<select id="GPIO_12" name="GPIO_12[type]" class="w3-select" style="width: 160px;">
  <option <?php if ($GPIO['GPIO_12']['type'] == 'door_led') echo 'selected="selected"'; ?> value="door_led">Door Indicator</option>
  <option <?php if ($GPIO['GPIO_12']['type'] == 'led') echo 'selected="selected"'; ?>value="relay">Relay</option>
</select></td>
<td><label>Name: <input name="GPIO_12[name]" type="text" value="<?=$GPIO['GPIO_12']['name']?>" size="30"></label></td>
</tr>

<tr>
<td><label for="GPIO_18">GPIO 18<input name="GPIO_18[gpio_pin]" type="hidden" value="18"></label></td>
<td>
<label for="GPIO_18">Output type:</label>
<select id="GPIO_18" name="GPIO_18[type]" class="w3-select" style="width: 160px;">
  <option <?php if ($GPIO['GPIO_18']['type'] == 'motion_led') echo 'selected="selected"'; ?> value="motion_led">Motion Indicator</option>
  <option <?php if ($GPIO['GPIO_18']['type'] == 'led') echo 'selected="selected"'; ?>value="relay">Relay</option>
</select></td>
<td><label>Name: <input name="GPIO_18[name]" type="text" value="<?=$GPIO['GPIO_18']['name']?>" size="30"></label></td>
</tr>
</table>
</fieldset>

<fieldset>
<legend>Zabbix Agent configuration</legend>
<table id="t01" class="w3-table">

<tr><td>
<label>Zabbix server:</label>
</td>
<td>
<input name="zabbix_server" type="text" size="30" placeholder="zabbix.example.com" value="<?=$zabbix_server?>" pattern="^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$">
</td></tr>
<tr><td>
<label>Zabbix server Active:</label>
</td>
<td>
<input name="zabbix_server_active"  type="text" size="30" value="<?=$zabbix_server_active?>" placeholder="zabbix.example.com" pattern="^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$">
</td>
</tr>

<tr><td>
<label>RPiMS location:</label>
</td>
<td>
<input name="location" type="text" size="30" value="<?=$location?>" >
</td>
</tr>

<tr><td>
<label>RPiMS hostname:</label>
</td>
<td>
<input name="hostname" type="text" size="30" value="<?=$hostname?>" >
</td>
</tr>

<tr><td>
<label>PSK identity:</label>
</td>
<td>
<input name="TLSPSKIdentity" id="TLSPSKIdentity" type="text" size="17" value="<?=$TLSPSKIdentity?>">
</td>
<td>
<input type="button" onclick="gfg_Run(16,tlspskidentityid)" value="Generate PSK Identity">
</td>
</td>
</tr>

<tr><td>
<label>PSK:</label>
</td>
<td>
<input name="TLSPSK"  id="TLSPSK" type="text" size="75" value="<?=$TLSPSK?>" >
</td>
<td>
<input type="button" onclick="gfg_Run(64,tlspskid)" value="Generate PSK">
</td>
</td>
</tr>

<tr><td>
<label>Timeout:</label>
</td>
<td>
<input name="Timeout" type="number" min="1" max="10" value="<?=$Timeout?>" >
</td></tr>

</table>
</fieldset>
<fieldset>
<input type="submit" value="Save" class="w3-bar">
</fieldset>
</form>
</div>
</body>
</html>
