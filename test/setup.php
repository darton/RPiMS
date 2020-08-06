<!DOCTYPE html>
<html lang="en">

<head>
<title>RPiMS configuration</title>
<meta charset="utf-8"/>
</head>

<body>
<?php $rpims = yaml_parse_file ("/var/www/html/rpims2.yaml");
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
$use_system_buttons = filter_var($rpims['setup']['use_system_buttons'], FILTER_VALIDATE_BOOLEAN);
$use_led_indicator = filter_var($rpims['setup']['use_led_indicator'], FILTER_VALIDATE_BOOLEAN);
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
    //print_r('GPIO_'.$value['gpio_pin']);
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
//var_dump($GPIO);
?>

<fieldset>
<legend>System configuration</legend>
<form action="/form.php" method="post">
<label>Verbose: <input name="verbose" type="hidden" value="False"><input name="verbose" type="checkbox" <?php if ($verbose == 'yes') echo 'checked="checked"'; ?> value="True"></label><br />
<label>Use zabbix sender: <input name="use_zabbix_sender" type="hidden" value="False"><input name="use_zabbix_sender" type="checkbox" <?php if ($use_zabbix_sender == 'yes') echo 'checked="checked"'; ?> value="True"></label><br />
<label>Use picamera: <input name="use_picamera" type="hidden" value="False"><input name="use_picamera" type="checkbox" <?php if ($use_picamera == 'yes') echo 'checked="checked"'; ?> value="True"></label>
<label>Use picamera recording: <input name="use_picamera_recording" type="hidden" value="False"><input name="use_picamera_recording" type="checkbox" <?php if ($use_picamera_recording == 'yes') echo 'checked="checked"'; ?> value="True"></label><br />
<label>Use door sensor: <input name="use_door_sensor" type="hidden" value="False"><input name="use_door_sensor" type="checkbox" <?php if ($use_door_sensor == 'yes') echo 'checked="checked"'; ?> value="True"></label><br />
<label>Use motion sensor: <input name="use_motion_sensor" type="hidden" value="False"><input name="use_motion_sensor" type="checkbox" <?php if ($use_motion_sensor == 'yes') echo 'checked="checked"'; ?> value="True"></label><br />
<label>Use system buttons: <input name="use_system_buttons" type="hidden" value="False"><input name="use_system_buttons" type="checkbox" <?php if ($use_system_buttons == 'yes') echo 'checked="checked"'; ?> value="True"></label><br />
<label>Use led indicator: <input name="use_led_indicator" type="hidden" value="False"><input name="use_led_indicator" type="checkbox" <?php if ($use_led_indicator == 'yes') echo 'checked="checked"'; ?> value="True"></label><br />
<label>Use CPU sensor: <input name="use_CPU_sensor" type="hidden" value="False"><input name="use_CPU_sensor" type="checkbox" <?php if ($use_CPU_sensor == 'yes') echo 'checked="checked"'; ?> value="True"></label><br />
<label>Use BME280 sensor: <input name="use_BME280_sensor" type="hidden" value="False"><input name="use_BME280_sensor" type="checkbox" <?php if ($use_BME280_sensor == 'yes') echo 'checked="checked"'; ?> value="True"></label><br />
<label>Use DS18B20 sensor: <input name="use_DS18B20_sensor" type="hidden" value="False"><input name="use_DS18B20_sensor" type="checkbox" <?php if ($use_DS18B20_sensor == 'yes') echo 'checked="checked"'; ?> value="True"></label><br />
<label>Use DHT sensor: <input name="use_DHT_sensor" type="hidden" value="False"><input name="use_DHT_sensor" type="checkbox" <?php if ($use_DHT_sensor == 'yes') echo 'checked="checked"'; ?> value="True"></label><br />
<label>Use serial display: <input name="use_serial_display" type="hidden" value="False"><input name="use_serial_display" type="checkbox" <?php if ($use_serial_display == 'yes') echo 'checked="checked"'; ?> value="True"></label>
</div>

<label for="serial_display_type">Serial display type</label>
<select id="serial_display_type" name="serial_display_type">
<option value="oled_sh1106"<?php if ($serial_display_type == 'oled_sh1106') echo 'selected="selected"'; ?> >oled_sh1106</option>
<option value="lcd_st7735"<?php if ($serial_display_type == 'lcd_st7735') echo 'selected="selected"'; ?> >lcd_st7735</option>
</select>
<label>Serial display refresh rate: <input name="serial_display_refresh_rate" type="number" min="1" max="50" value=<?= is_null($serial_display_refresh_rate) ? 0: 10 ?> size="2"></label><br />
</fieldset>
<br />

<fieldset>
<legend>Sensor configuration</legend>
<label>CPUtemp read interval: <input name="CPUtemp_read_interval" type="number" min="1" max="3600" value=<?= is_null($CPUtemp_read_interval) ? 0: 1 ?> size="4"></label><br />
<label>BME280 read interval: <input name="BME280_read_interval" type="number" min="1" max="3600" value=<?= is_null($BME280_read_interval) ? 0: 10 ?> size="4"></label>
<label for="BME280_i2c_address">BME280_i2c_address:</label>
<select id="BME280_i2c_address" name="BME280_i2c_address">
<option value = 0x76 <?php if ($BME280_i2c_address == '118') echo 'selected="selected"'; ?> >0x76</option>
<option value = 0x77 <?php if ($BME280_i2c_address == '119') echo 'selected="selected"'; ?> >0x77</option>
</select>
<br />
<label>DS18B20 read interval: <input name="DS18B20_read_interval" type="number" min="1" max="3600" value=<?= is_null($DS18B20_read_interval) ? 0: 60 ?> size="4"></label><br />
<label>DHT read interval: <input name="DHT_read_interval" type="number" min="1" max="3600"  value=<?= is_null($DHT_read_interval) ? 0: 5 ?> size="4"></label>
<label for="DHT_type">DHT type:</label>
<select id="DHT_type" name="DHT_type">
  <option value="DHT11" <?php if ($DHT_type == 'DHT11') echo 'selected="selected"'; ?> >DHT11</option>
  <option value="DHT22" <?php if ($DHT_type == 'DHT22') echo 'selected="selected"'; ?> >DHT22</option>
  <option value="AM2302" <?php if ($DHT_type == 'AM2302') echo 'selected="selected"'; ?> >AM2302</option>
</select>
<label for="DHT_pin">DHT pin:</label>
<select id="DHT_pin" name="DHT_pin">
  <option value = 17 <?php if ($DHT_pin == '17') echo 'selected="selected"'; ?> >17</option>
  <option value = 18 <?php if ($DHT_pin == '18') echo 'selected="selected"'; ?> >18</option>
</select><br />
</fieldset>
<br />

<fieldset>
<legend>Input configuration</legend>
<label for="GPIO_5">GPIO 5 input type:</label>
<select id="GPIO_5" name="GPIO_5[type]" style="width: 125px;">
  <option <?php if ($GPIO['GPIO_5']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Door Sensor</option>
  <option <?php if ($GPIO['GPIO_5']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
</select>
<label>Hold Time: <input name="GPIO_5[hold_time]" type="number" min="1" max="10"  value=<?=$GPIO['GPIO_5']['hold_time']?> size="2"></label>
<label><input name="GPIO_5[gpio_pin]" type="hidden" value="5"></label>
<br />

<label for="GPIO_6">GPIO 6 input type:</label>
<select id="GPIO_6" name="GPIO_6[type]" style="width: 125px;">
  <option <?php if ($GPIO['GPIO_6']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Door Sensor</option>
  <option <?php if ($GPIO['GPIO_6']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
</select>
<label>Hold Time: <input name="GPIO_6[hold_time]" type="number" min="1" max="10"  value=<?=$GPIO['GPIO_6']['hold_time']?> size="2"></label>
<label><input name="GPIO_6[gpio_pin]" type="hidden" value="6"></label>
<br />

<label for="GPIO_13">GPIO 13 input type:</label>
<select id="GPIO_13" name="GPIO_13[type]" style="width: 125px;">
  <option <?php if ($GPIO['GPIO_13']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Door Sensor</option>
  <option <?php if ($GPIO['GPIO_13']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
</select>
<label>Hold Time: <input name="GPIO_13[hold_time]" type="number" min="1" max="10"  value=<?=$GPIO['GPIO_13']['hold_time']?> size="2"></label>
<label><input name="GPIO_13[gpio_pin]" type="hidden" value="13"></label>
<br />

<label for="GPIO_16">GPIO 16 input type:</label>
<select id="GPIO_16" name="GPIO_16[type]" style="width: 125px;">
  <option <?php if ($GPIO['GPIO_16']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Door Sensor</option>
  <option <?php if ($GPIO['GPIO_16']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
  <option <?php if ($GPIO['GPIO_16']['type'] == 'ShutdownButton') echo 'selected="selected"'; ?> value="ShutdownButton">Shutdown Button</option>
</select>
<label>Hold Time: <input name="GPIO_16[hold_time]" type="number" min="1" max="10"  value=<?=$GPIO['GPIO_16']['hold_time']?> size="2"></label>
<label><input name="GPIO_16[gpio_pin]" type="hidden" value="16"></label>
<br />

<label for="GPIO_17">GPIO 17 input type:</label>
<select id="GPIO_17" name="GPIO_17[type]" style="width: 125px;">
  <option <?php if ($GPIO['GPIO_17']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Door Sensor</option>
  <option <?php if ($GPIO['GPIO_17']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
</select>
<label>Hold Time: <input name="GPIO_17[hold_time]" type="number" min="1" max="10"  value=<?=$GPIO['GPIO_17']['hold_time']?> size="2"></label>
<label><input name="GPIO_17[gpio_pin]" type="hidden" value="17"></label>
<br />

<label for="GPIO_19">GPIO 19 input type:</label>
<select id="GPIO_19" name="GPIO_19[type]" style="width: 125px;">
  <option <?php if ($GPIO['GPIO_19']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Door Sensor</option>
  <option <?php if ($GPIO['GPIO_19']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
</select>
<label>Hold Time: <input name="GPIO_19[hold_time]" type="number" min="1" max="10"  value=<?=$GPIO['GPIO_19']['hold_time']?> size="2"></label>
<label><input name="GPIO_19[gpio_pin]" type="hidden" value="19"></label>
<br />

<label for="GPIO_20">GPIO 20 input type:</label>
<select id="GPIO_20" name="GPIO_20[type]" style="width: 125px;">
  <option <?php if ($GPIO['GPIO_20']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Door Sensor</option>
  <option <?php if ($GPIO['GPIO_20']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
</select>
<label>Hold Time: <input name="GPIO_20[hold_time]" type="number" min="1" max="10"  value=<?=$GPIO['GPIO_20']['hold_time']?> size="2"></label>
<label><input name="GPIO_20[gpio_pin]" type="hidden" value="20"></label>
<br />

<label for="GPIO_21">GPIO 21 input type:</label>
<select id="GPIO_21" name="GPIO_21[type]" style="width: 125px;">
  <option <?php if ($GPIO['GPIO_21']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Door Sensor</option>
  <option <?php if ($GPIO['GPIO_21']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
</select>
<label>Hold Time: <input name="GPIO_21[hold_time]" type="number" min="1" max="10"  value=<?=$GPIO['GPIO_21']['hold_time']?> size="2"></label>
<label><input name="GPIO_21[gpio_pin]" type="hidden" value="21"></label>
<br />

<label for="GPIO_26">GPIO 26 input type:</label>
<select id="GPIO_26" name="GPIO_26[type]" style="width: 125px;">
  <option <?php if ($GPIO['GPIO_26']['type'] == 'DoorSensor') echo 'selected="selected"'; ?> value="DoorSensor">Door Sensor</option>
  <option <?php if ($GPIO['GPIO_26']['type'] == 'MotionSensor') echo 'selected="selected"'; ?> value="MotionSensor">Motion Sensor</option>
</select>
<label>Hold Time: <input name="GPIO_26[hold_time]" type="number"  min="1" max="10"  value=<?=$GPIO['GPIO_26']['hold_time']?> size="2"></label>
<label><input name="GPIO_26[gpio_pin]" type="hidden" value="26"></label>
<br />
</fieldset>
<br />

<fieldset>
<legend>Output configuration</legend>
<label for="GPIO_12">GPIO 12:</label>
<select id="GPIO_12" name="GPIO_12[type]" style="width: 125px;">
  <option value="motion_led">Motion Indicator</option>
  <option selected value="door_led">Door Indicator</option>
</select>
<label><input name="GPIO_12[gpio_pin]" type="hidden" value="12"></label>
<br />
<label for="GPIO_18">GPIO 18:</label>
<select id="GPIO_18" name="GPIO_18[type]" style="width: 125px;">
  <option selected value="motion_led">Motion Indicator</option>
  <option value="door_led">Door Indicator</option>
</select>
<label><input name="GPIO_18[gpio_pin]" type="hidden" value="18"></label>
<br />
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

<br />

</body>
</html>
