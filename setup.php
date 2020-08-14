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
</head>

<body>
<?php

$GPIO = array();
$GPIO_5 = array();
$GPIO_6 = array();
$GPIO_12 = array();
$GPIO_13 = array();
$GPIO_16 = array();
$GPIO_17 = array();
$GPIO_18 = array();
$GPIO_19 = array();
$GPIO_20 = array();
$GPIO_21 = array();
$GPIO_22 = array();
$GPIO_23 = array();
$GPIO_26 = array();

$rpims = yaml_parse_file ("/var/www/html/rpims.yaml");
$location = $rpims['zabbix_agent']['location'];
$hostname = $rpims['zabbix_agent']['hostname'];
$zabbix_server = $rpims['zabbix_agent']['zabbix_server'];
$zabbix_server_active = $rpims['zabbix_agent']['zabbix_server_active'];

$verbose = filter_var($rpims['setup']['verbose'], FILTER_VALIDATE_BOOLEAN);
$use_zabbix_sender = filter_var($rpims['setup']['use_zabbix_sender'], FILTER_VALIDATE_BOOLEAN);
$use_picamera = filter_var($rpims['setup']['use_picamera'], FILTER_VALIDATE_BOOLEAN);
$use_picamera_recording = filter_var($rpims['setup']['use_picamera_recording'], FILTER_VALIDATE_BOOLEAN);
$use_door_sensor = filter_var($rpims['setup']['use_door_sensor'], FILTER_VALIDATE_BOOLEAN);
$use_motion_sensor = filter_var($rpims['setup']['use_motion_sensor'], FILTER_VALIDATE_BOOLEAN);
//$use_system_buttons = filter_var($rpims['setup']['use_system_buttons'], FILTER_VALIDATE_BOOLEAN);
$use_led_indicators = filter_var($rpims['setup']['use_led_indicators'], FILTER_VALIDATE_BOOLEAN);
$use_serial_display = filter_var($rpims['setup']['use_serial_display'], FILTER_VALIDATE_BOOLEAN);
$use_CPU_sensor = filter_var($rpims['setup']['use_CPU_sensor'], FILTER_VALIDATE_BOOLEAN);
$use_BME280_sensor = filter_var($rpims['setup']['use_BME280_sensor'], FILTER_VALIDATE_BOOLEAN);
$use_DS18B20_sensor = filter_var($rpims['setup']['use_DS18B20_sensor'], FILTER_VALIDATE_BOOLEAN);
$use_DHT_sensor = filter_var($rpims['setup']['use_DHT_sensor'], FILTER_VALIDATE_BOOLEAN);

$serial_display_refresh_rate = $rpims['setup']['serial_display_refresh_rate'];
$serial_display_type = $rpims['setup']['serial_display_type'];

$CPUtemp_read_interval = $rpims['setup']['CPUtemp_read_interval'];

$BME280_i2c_address = $rpims['setup']['BME280_i2c_address'];
$BME280_read_interval = $rpims['setup']['BME280_read_interval'];

$DS18B20_read_interval = $rpims['setup']['DS18B20_read_interval'];

$DHT_read_interval = $rpims['setup']['DHT_read_interval'];
$DHT_type = $rpims['setup']['DHT_type'];
$DHT_pin = $rpims['setup']['DHT_pin'];

$motion_sensors_gpio = $rpims['motion_sensors'];
$door_sensors_gpio = $rpims['door_sensors'];
$system_buttons_gpio = $rpims['system_buttons'];

foreach ($door_sensors_gpio as $key => $value) {
    $gpioname = 'GPIO_'.$value['gpio_pin'] ;
    $GPIO[$gpioname]['type'] = 'DoorSensor';
    $GPIO[$gpioname]['hold_time'] = $value['hold_time'];
}
foreach ($motion_sensors_gpio as $key => $value) {
    $gpioname = 'GPIO_'.$value['gpio_pin'];
    $GPIO[$gpioname]['type'] = 'MotionSensor';
}
foreach ($system_buttons_gpio as $key => $value) {
    $gpioname = 'GPIO_'.$value['gpio_pin'];
    $GPIO[$gpioname]['type'] = 'ShutdownButton';
    $GPIO[$gpioname]['hold_time'] = $value['hold_time'];
}

//var_dump($GPIO['GPIO_16']['hold_time']);

?>
<div class="w3-responsive">
<form action="/form.php" method="post" class="w3-container">
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
<label>Use door sensor:</label>
</td>
<td>
<input name="use_door_sensor" type="hidden" value="False"><input name="use_door_sensor" type="checkbox" class="w3-check" <?php if ($use_door_sensor == 'yes') echo 'checked="checked"'; ?> value="True">
</td>
</tr>
<tr>
<td>
<label>Use motion sensor:</label>
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
<option value="oled_sh1106_i2c"<?php if ($serial_display_type == 'oled_sh1106_i2c') echo 'selected="selected"'; ?> >oled_sh1106_i2c</option>
<option value="oled_sh1106_spi"<?php if ($serial_display_type == 'oled_sh1106_spi') echo 'selected="selected"'; ?> >oled_sh1106_spi</option>
<option value="lcd_st7735"<?php if ($serial_display_type == 'lcd_st7735') echo 'selected="selected"'; ?> >lcd_st7735</option>
</select>
</td>
<td>
<label>Serial display refresh rate:</label>
</td>
<td>
<input name="serial_display_refresh_rate" type="number" min="1" max="50" size="2" value="<?= is_null($serial_display_refresh_rate) ? 0: 10 ?>" >
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
<input name="CPUtemp_read_interval" type="number" min="1" max="3600" class="w3-input" size="4" value="<?= is_null($CPUtemp_read_interval) ? 0: 1 ?>" >
</td></tr>
<tr><td>
<label>BME280 read interval:</label>
</td>
<td>
<input name="BME280_read_interval" type="number" min="1" max="3600" class="w3-input" size="4" value="<?= is_null($BME280_read_interval) ? 0: 10 ?>" >
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
<label>DS18B20 read interval:</label>
</td>
<td>
<input name="DS18B20_read_interval" class="w3-input" type="number" min="1" max="3600" size="4" value="<?= is_null($DS18B20_read_interval) ? 0: 60 ?>" >
</td></tr>
<tr><td>
<label>DHT read interval:</label>
</td><td>
<input name="DHT_read_interval" class="w3-input" type="number" min="1" max="3600" size="4" value="<?= is_null($DHT_read_interval) ? 0: 5 ?>" >
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
  <option value = 17 <?php if ($DHT_pin == '17') echo 'selected="selected"'; ?> >17</option>
  <option value = 22 <?php if ($DHT_pin == '22') echo 'selected="selected"'; ?> >22</option>
</select>
</td></tr>
</table>
</fieldset>


<fieldset>
<legend>Input configuration</legend>
<table id="t01" class="w3-table">
<tr><td>
<label for="GPIO_5">GPIO 5 input type:</label>
</td>
<td>
<select id="GPIO_5" name="GPIO_5[type]" style="width: 160px;" class="w3-select">
  <option <?php if ($GPIO['GPIO_5']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Door Sensor</option>
  <option <?php if ($GPIO['GPIO_5']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
</select>
</td>
<?php
if ($GPIO['GPIO_5']['type'] == 'DoorSensor'){
    if ($GPIO['GPIO_5']['hold_time'] == 0 ){ $GPIO_5_hold_time = 1;}
    else { $GPIO_5_hold_time = $GPIO['GPIO_5']['hold_time']; }
?>
<td>
<label>Hold Time: <input name="GPIO_5[hold_time]" type="number" min="1" max="10" value="<?=$GPIO_5_hold_time?>" size="2"></label>
</td>
<?php } ?>
<label><input name="GPIO_5[gpio_pin]" type="hidden" value="5"></label>
</tr>

<tr><td>
<label for="GPIO_6">GPIO 6 input type:</label>
</td>
<td>
<select id="GPIO_6" name="GPIO_6[type]" style="width: 160px;" class="w3-select">
  <option <?php if ($GPIO['GPIO_6']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Door Sensor</option>
  <option <?php if ($GPIO['GPIO_6']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
</select>
</td>
<?php
if ($GPIO['GPIO_6']['type'] == 'DoorSensor'){
    if ($GPIO['GPIO_6']['hold_time'] == 0 ){ $GPIO_6_hold_time = 1;}
    else { $GPIO_6_hold_time = $GPIO['GPIO_6']['hold_time']; }
?>
<td>
<label>Hold Time: <input name="GPIO_6[hold_time]" type="number" min="1" max="10" value="<?=$GPIO_6_hold_time?>" size="2"></label>
</td>
<?php } ?>
<label><input name="GPIO_6[gpio_pin]" type="hidden" value="6"></label>
</tr>

<tr><td>
<label for="GPIO_13">GPIO 13 input type:</label>
</td>
<td>
<select id="GPIO_13" name="GPIO_13[type]" style="width: 160px;" class="w3-select">
  <option <?php if ($GPIO['GPIO_13']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Door Sensor</option>
  <option <?php if ($GPIO['GPIO_13']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
</select>
</td>
<?php
if ($GPIO['GPIO_13']['type'] == 'DoorSensor'){
    if ($GPIO['GPIO_13']['hold_time'] == 0 ){ $GPIO_13_hold_time = 1;}
    else { $GPIO_13_hold_time = $GPIO['GPIO_13']['hold_time']; }
?>
<td>
<label>Hold Time: <input name="GPIO_13[hold_time]" type="number" min="1" max="10" value="<?=$GPIO_13_hold_time?>" size="2"></label>
</td>
<?php } ?>
<tr>
<label><input name="GPIO_13[gpio_pin]" type="hidden" value="13"></label>
</tr>

<tr><td>
<label for="GPIO_16">GPIO 16 input type:</label>
</td>
<td>
<select id="GPIO_16" name="GPIO_16[type]" style="width: 160px;" class="w3-select">
  <option <?php if ($GPIO['GPIO_16']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Door Sensor</option>
  <option <?php if ($GPIO['GPIO_16']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
  <option <?php if ($GPIO['GPIO_16']['type'] == 'ShutdownButton') echo 'selected="selected"'; ?> value="ShutdownButton">Shutdown Button</option>
</select>
</td>
<?php
if ($GPIO['GPIO_16']['type'] == 'DoorSensor' OR $GPIO['GPIO_16']['type'] == 'ShutdownButton') {
    if ($GPIO['GPIO_16']['hold_time'] == 0 ){ $GPIO_16_hold_time = 1;}
    else { $GPIO_16_hold_time = $GPIO['GPIO_16']['hold_time']; }
?>
<td>
<label>Hold Time: <input name="GPIO_16[hold_time]" type="number" min="1" max="10"  value="<?=$GPIO_16_hold_time?>" size="2"></label>
</td>
<?php } ?>
<label><input name="GPIO_16[gpio_pin]" type="hidden" value="16"></label>
</tr>

<tr><td>
<label for="GPIO_17">GPIO 17 input type:</label>
</td>
<td>
<select id="GPIO_17" name="GPIO_17[type]" style="width: 160px;" class="w3-select">
  <option <?php if ($GPIO['GPIO_17']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Door Sensor</option>
  <option <?php if ($GPIO['GPIO_17']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
</select>
</td>
<?php
if ($GPIO['GPIO_17']['type'] == 'DoorSensor'){
    if ($GPIO['GPIO_17']['hold_time'] == 0 ){ $GPIO_17_hold_time = 1;}
    else { $GPIO_17_hold_time = $GPIO['GPIO_17']['hold_time']; }
?>
<td>
<label>Hold Time: <input name="GPIO_17[hold_time]" type="number" min="1" max="10"  value="<?=$GPIO_17_hold_time?>" size="2"></label>
<?php } ?>
</td>
<label><input name="GPIO_17[gpio_pin]" type="hidden" value="17"></label>
</tr>

<tr><td>
<label for="GPIO_19">GPIO 19 input type:</label>
</td>
<td>
<select id="GPIO_19" name="GPIO_19[type]" style="width: 160px;" class="w3-select">
  <option <?php if ($GPIO['GPIO_19']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Door Sensor</option>
  <option <?php if ($GPIO['GPIO_19']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
</select>
</td>
<?php
if ($GPIO['GPIO_19']['type'] == 'DoorSensor'){
    if ($GPIO['GPIO_19']['hold_time'] == 0 ){ $GPIO_19_hold_time = 1;}
    else { $GPIO_19_hold_time = $GPIO['GPIO_19']['hold_time']; }
?>
<td>
<label>Hold Time: <input name="GPIO_19[hold_time]" type="number" min="1" max="10" value="<?=$GPIO_19_hold_time?>" size="2"></label>
</td>
<?php } ?>
<label><input name="GPIO_19[gpio_pin]" type="hidden" value="19"></label>
</tr>

<tr><td>
<label for="GPIO_20">GPIO 20 input type:</label>
</td>
<td>
<select id="GPIO_20" name="GPIO_20[type]" style="width: 160px;" class="w3-select">
  <option <?php if ($GPIO['GPIO_20']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Door Sensor</option>
  <option <?php if ($GPIO['GPIO_20']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
</select>
</td>
<?php
if ($GPIO['GPIO_20']['type'] == 'DoorSensor'){
    if ($GPIO['GPIO_20']['hold_time'] == 0 ){ $GPIO_20_hold_time = 1;}
    else { $GPIO_20_hold_time = $GPIO['GPIO_20']['hold_time']; }
?>
<td>
<label>Hold Time: <input name="GPIO_20[hold_time]" type="number" min="1" max="10" value="<?=$GPIO_20_hold_time?>" size="2"></label>
</td>
<?php } ?>
<label><input name="GPIO_20[gpio_pin]" type="hidden" value="20"></label>
</tr>

<tr><td>
<label for="GPIO_21">GPIO 21 input type:</label>
</td>
<td>
<select id="GPIO_21" name="GPIO_21[type]" style="width: 160px;" class="w3-select">
  <option <?php if ($GPIO['GPIO_21']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Door Sensor</option>
  <option <?php if ($GPIO['GPIO_21']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
</select>
</td>
<?php
if ($GPIO['GPIO_21']['type'] == 'DoorSensor'){
    if ($GPIO['GPIO_21']['hold_time'] == 0 ){ $GPIO_21_hold_time = 1;}
    else { $GPIO_21_hold_time = $GPIO['GPIO_21']['hold_time']; }
?>
<td>
<label>Hold Time: <input name="GPIO_21[hold_time]" type="number" min="1" max="10" value="<?=$GPIO_21_hold_time?>" size="2"></label>
</td>
<?php } ?>
<label><input name="GPIO_21[gpio_pin]" type="hidden" value="21"></label>
</tr>

<tr><td>
<label for="GPIO_22">GPIO 22 input type:</label>
</td>
<td>
<select id="GPIO_22" name="GPIO_22[type]" style="width: 160px;" class="w3-select">
  <option <?php if ($GPIO['GPIO_22']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Door Sensor</option>
  <option <?php if ($GPIO['GPIO_22']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
</select>
</td>
<?php
if ($GPIO['GPIO_22']['type'] == 'DoorSensor'){
    if ($GPIO['GPIO_22']['hold_time'] == 0 ){ $GPIO_22_hold_time = 1;}
    else { $GPIO_22_hold_time = $GPIO['GPIO_22']['hold_time']; }
?>
<td>
<label>Hold Time: <input name="GPIO_22[hold_time]" type="number" min="1" max="10" value="<?=$GPIO_22_hold_time?>" size="2"></label>
</td>
<?php } ?>
<label><input name="GPIO_22[gpio_pin]" type="hidden" value="22"></label>
</tr>

<tr><td>
<label for="GPIO_23">GPIO 23 input type:</label>
</td>
<td>
<select id="GPIO_23" name="GPIO_23[type]" style="width: 160px;" class="w3-select">
  <option <?php if ($GPIO['GPIO_23']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Door Sensor</option>
  <option <?php if ($GPIO['GPIO_23']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
</select>
</td>
<?php
if ($GPIO['GPIO_23']['type'] == 'DoorSensor'){
    if ($GPIO['GPIO_23']['hold_time'] == 0 ){ $GPIO_23_hold_time = 1;}
    else { $GPIO_23_hold_time = $GPIO['GPIO_23']['hold_time']; }
?>
<td>
<label>Hold Time: <input name="GPIO_23[hold_time]" type="number" min="1" max="10" value="<?=$GPIO_23_hold_time?>" size="2"></label>
</td>
<?php } ?>
<label><input name="GPIO_23[gpio_pin]" type="hidden" value="23"></label>
</tr>

<tr><td>
<label for="GPIO_26">GPIO 26 input type:</label>
</td>
<td>
<select id="GPIO_26" name="GPIO_26[type]" style="width: 160px;" class="w3-select">
  <option <?php if ($GPIO['GPIO_26']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Door Sensor</option>
  <option <?php if ($GPIO['GPIO_26']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
</select>
</td>
<?php
if ($GPIO['GPIO_26']['type'] == 'DoorSensor'){
    if ($GPIO['GPIO_26']['hold_time'] == 0 ){ $GPIO_26_hold_time = 1;}
    else { $GPIO_26_hold_time = $GPIO['GPIO_26']['hold_time']; }
?>
<td>
<label>Hold Time: <input name="GPIO_26[hold_time]"  type="number" min="1" max="10" value="<?=$GPIO_26_hold_time?>" size="2"></label>
</td>
<?php } ?>
<label><input name="GPIO_26[gpio_pin]" type="hidden" value="26"></label>
</tr>
</table>
</fieldset>


<fieldset>
<legend>Output configuration</legend>
<table id="t01" class="w3-table">
<tr><td>
<label for="GPIO_12">GPIO 12:</label>
</td>
<td>
<select id="GPIO_12" name="GPIO_12[type]" class="w3-select" style="width: 160px;">
  <option value="motion_led">Motion Indicator</option>
  <option selected value="door_led">Door Indicator</option>
</select>
</td>
<label><input name="GPIO_12[gpio_pin]" type="hidden" value="12"></label>
</tr>

<tr><td>
<label for="GPIO_18">GPIO 18:</label>
</td>
<td>
<select id="GPIO_18" name="GPIO_18[type]" class="w3-select" style="width: 160px;">
  <option selected value="motion_led">Motion Indicator</option>
  <option value="door_led">Door Indicator</option>
</select>
</td>
<label><input name="GPIO_18[gpio_pin]" type="hidden" value="18"></label>
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
</td></tr>

<tr><td>
<label>RPiMS location:</label>
</td>
<td>
<input name="location" type="text" size="30" value="<?=$location?>" >
</td></tr>

<tr><td>
<label>RPiMS hostname:</label>
</td>
<td>
<input name="hostname" type="text" size="30" value="<?=$hostname?>" >
</td></tr>
</table>
</fieldset>

<input type="submit" value="Save" class="w3-bar">
</form>
</div>
</body>
</html>
