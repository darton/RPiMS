<!DOCTYPE html>
<html lang="en">

<head>
<title>RPiMS configuration</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
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
<input name="verbose" type="hidden" value="no"><input name="verbose" type="checkbox" class="w3-check" <?php if ($verbose) echo 'checked="checked"'; ?> value="True">
<label>Verbose mode</label>
</td>
</tr>

<tr>
<td>
<input name="show_sys_info" type="hidden" value="False"><input name="show_sys_info" type="checkbox" class="w3-check" <?php if ($show_sys_info == 'yes') echo 'checked="checked"'; ?> value="True">
<label>Show system info</label>
</td>
</tr>

<tr>
<td>
<input name="use_zabbix_sender" type="hidden" value="False"><input name="use_zabbix_sender" type="checkbox" class="w3-check" <?php if ($use_zabbix_sender == 'yes') echo 'checked="checked"'; ?> value="True">
<label>Use zabbix sender</label>
</td>
</tr>

<tr>
<td>
<input name="use_picamera" type="hidden" value="False"><input name="use_picamera" type="checkbox" class="w3-check" <?php if ($use_picamera == 'yes') echo 'checked="checked"'; ?> value="True">
<label>Use picamera</label>
</td>
</tr>

<tr>
<td>
<input name="use_picamera_recording" type="hidden" value="False"><input name="use_picamera_recording" type="checkbox" class="w3-check"  <?php if ($use_picamera_recording == 'yes') echo 'checked="checked"'; ?> value="True">
<label>Use picamera recording</label>
</td>

</tr>

<tr>
<td>
<input name="use_door_sensor" type="hidden" value="False"><input name="use_door_sensor" type="checkbox" class="w3-check" <?php if ($use_door_sensor == 'yes') echo 'checked="checked"'; ?> value="True">
<label>Use door sensors</label>
</td>
</tr>

<tr>
<td>
<input name="use_motion_sensor" type="hidden" value="False"><input name="use_motion_sensor" type="checkbox" class="w3-check" <?php if ($use_motion_sensor == 'yes') echo 'checked="checked"'; ?> value="True">
<label>Use motion sensors</label>
</td>
</tr>

<tr>
<td>
<input name="use_CPU_sensor" type="hidden" value="False"><input name="use_CPU_sensor" type="checkbox" class="w3-check" <?php if ($use_CPU_sensor == 'yes') echo 'checked="checked"'; ?> value="True">
<label>Use CPU sensor</label>
</td>
</tr>

<tr>
<td>
<input name="use_BME280_sensor" type="hidden" value="False"><input name="use_BME280_sensor" type="checkbox" class="w3-check" <?php if ($use_BME280_sensor == 'yes') echo 'checked="checked"'; ?> value="True">
<label>Use BME280 sensor</label>
</td>
</tr>

<tr>
<td>
<input name="use_DS18B20_sensor" type="hidden" value="False"><input name="use_DS18B20_sensor" type="checkbox" class="w3-check" <?php if ($use_DS18B20_sensor == 'yes') echo 'checked="checked"'; ?> value="True">
<label>Use DS18B20 sensor</label>
</td>
</tr>

<tr>
<td>
<input name="use_DHT_sensor" type="hidden" value="False"><input name="use_DHT_sensor" type="checkbox" class="w3-check" <?php if ($use_DHT_sensor) echo 'checked="checked"'; ?> value="True">
<label>Use DHT sensor</label>
</td>
</tr>

<tr>
<td>
<input name="use_weather_station" type="hidden" value="False"><input name="use_weather_station" type="checkbox" class="w3-check" <?php if ($use_weather_station) echo 'checked="checked"'; ?> value="True">
<label>Use weather station</label>
</td>
</tr>

<tr>
<td>
<input name="use_serial_display" type="hidden" value="False"><input name="use_serial_display" type="checkbox" class="w3-check" <?php if ($use_serial_display == 'yes') echo 'checked="checked"'; ?> value="True">
<label>Use serial display</label>
</td>
</tr>
</table>
</div>
</fieldset>

<fieldset>
<legend>Serial display configuration</legend>
<div>
<table class="w3-table">

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
</tr>
<tr>
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
<legend>CPU sensor configuration</legend>
<div>
<table class="w3-table">

<tr>
<td>
<label for="CPUtemp_read_interval">CPUtemp read interval:</label>
<input name="CPUtemp_read_interval" class="w3-input" id="CPUtemp_read_interval" type="number" min="1" max="3600" value="<?= $CPUtemp_read_interval ?>" >
</td>
</tr>

</table>
</div>
</fieldset>


<fieldset>
<legend>DS18B20 sensor configuration</legend>
<div>

<table class="w3-table">
<tr>
<td>
<label>DS18B20</label>
</td>
</tr>
<tr>
<td>
<label for="DS18B20_read_interval">Read interval:</label>
<input name="DS18B20_read_interval" class="w3-input" id="DS18B20_read_interval" type="number" min="1" max="3600" value="<?= $DS18B20_read_interval ?>" >
</td>
</tr>
</table>
<br>

<?php foreach ($DS18B20_sensors_detected as $key => $value)
    {
	$DS18B20_name = $DS18B20_sensors[$value];
	echo "<table class='w3-table'>";
	echo "<tr><td><p>Address: $value</p>name: <input name='DS18B20[$value][name]' class='w3-input' type='text' value='$DS18B20_name'></td></tr>";
	echo "</table><br>";
    }
?>

</div>
</fieldset>


<fieldset>
<legend>BME280 sensor configuration</legend>
<div>

<table class="w3-table">
<tr>
<td>
<label>Use #1 BME280:</label>
<input name="id1_BME280_use" type="hidden" value="no"><input name="id1_BME280_use" type="checkbox" class="w3-check" <?php if ($id1_BME280_use) echo 'checked="checked"'; ?> value="True">
</td>
</tr>

<tr>
<td>
<label>name:</label>
<input name="id1_BME280_name" class="w3-input" type="text" value="<?=$id1_BME280_name?>" >
</td>
<td>
<label for="id1_BME280_read_interval">Read interval:</label>
<input name="id1_BME280_read_interval" class="w3-input" id="id1_BME280_read_interval" type="number" min="1" max="3600" value="<?= $id1_BME280_read_interval ?>" >
</td>
</tr>

<tr>
<td>
<label for="id1_BME280_interface">Interface type:</label>
<select name="id1_BME280_interface" class="w3-select" id="id1_BME280_interface">
<option <?php if ($id1_BME280_2_interface == 'i2c') echo 'selected="selected"'; ?> value = "i2c" >i2c</option>
</select>
</td>

<td>
<label id="id1_BME280_i2c_address">Serial port:
<select name="id1_BME280_i2c_address" class="w3-select" >
<option <?php if ($id1_BME280_i2c_address == '118') echo 'selected="selected"'; ?> value = "118" >0x76</option>
<option <?php if ($id1_BME280_i2c_address == '119') echo 'selected="selected"'; ?> value = "119" >0x77</option>
</select>
</label>
</td>
</tr>
</table>
<br>

<table class="w3-table">
<tr>
<td>
<label>Use #2 BME280:</label>
<input name="id2_BME280_use" type="hidden" value="no"><input name="id2_BME280_use" type="checkbox" class="w3-check" <?php if ($id2_BME280_use) echo 'checked="checked"'; ?> value="True">
</td>
</tr>

<tr>
<td>
<label>name:</label>
<input name="id2_BME280_name" class="w3-input" type="text" value="<?=$id2_BME280_name?>" >
</td>
<td>
<label for="id2_BME280_read_interval">Read interval:</label>
<input name="id2_BME280_read_interval" class="w3-input" id="id2_BME280_read_interval" type="number" min="1" max="3600" value="<?= $id2_BME280_read_interval ?>" >
</td>
</tr>

<tr>
<td>
<label for="id2_BME280_interface">Interface type:</label>
<select name="id2_BME280_interface" class="w3-select" id="id2_BME280_interface">
<option <?php if ($id2_BME280_interface == 'serial') echo 'selected="selected"'; ?> value = "serial" >serial</option>
</select>
</td>
<td>
<label id="id2_BME280_serial_port">Serial port:
<select name="id2_BME280_serial_port" class="w3-select" >
<option <?php if ($id2_BME280_serial_port == 'USB1') echo 'selected="selected"'; ?> value = "USB1" >USB1</option>
<option <?php if ($id2_BME280_serial_port == 'USB2') echo 'selected="selected"'; ?> value = "USB2" >USB2</option>
<option <?php if ($id2_BME280_serial_port == 'USB3') echo 'selected="selected"'; ?> value = "USB3" >USB3</option>
<option <?php if ($id2_BME280_serial_port == 'USB4') echo 'selected="selected"'; ?> value = "USB4" >USB4</option>
</select>
</label>
</td>
</tr>
</table>
<br>

<table class="w3-table">
<tr>
<td>
<label>Use #3 BME280:</label>
<input name="id3_BME280_use" type="hidden" value="no"><input name="id3_BME280_use" type="checkbox" class="w3-check" <?php if ($id3_BME280_use) echo 'checked="checked"'; ?> value="True">
</td>
</tr>

<tr>
<td>
<label>name:</label>
<input name="id3_BME280_name" class="w3-input" type="text" value="<?=$id3_BME280_name?>" >
</td>
<td>
<label for="id3_BME280_read_interval">Read interval:</label>
<input name="id3_BME280_read_interval" class="w3-input" id="id3_BME280_read_interval" type="number" min="1" max="3600" value="<?= $id3_BME280_read_interval ?>" >
</td>
</tr>

<tr>
<td>
<label for="id3_BME280_interface">Interface type:</label>
<select name="id3_BME280_interface" class="w3-select" id="id3_BME280_interface">
<option <?php if ($id3_BME280_interface == 'serial') echo 'selected="selected"'; ?> value = "serial" >serial</option>
</select>
</td>

<td>
<label id="id3_BME280_serial_port">Serial port:
<select name="id3_BME280_serial_port" class="w3-select" >
<option <?php if ($id3_BME280_serial_port == 'USB1') echo 'selected="selected"'; ?> value = "USB1" >USB1</option>
<option <?php if ($id3_BME280_serial_port == 'USB2') echo 'selected="selected"'; ?> value = "USB2" >USB2</option>
<option <?php if ($id3_BME280_serial_port == 'USB3') echo 'selected="selected"'; ?> value = "USB3" >USB3</option>
<option <?php if ($id3_BME280_serial_port == 'USB4') echo 'selected="selected"'; ?> value = "USB4" >USB4</option>
</select>
</label>
</td>
</tr>

</table>
</div>
</fieldset>


<fieldset>
<legend>DHT sensor configuration</legend>
<div>
    <table class="w3-table">
<tr>
<td>
<label>DHT</label>
</td>
</tr>

<tr>
<td>
<label>name:</label>
<input name="DHT_name" class="w3-input" type="text" value="<?=$DHT_name?>" >
</td>
</tr>
<tr>
<td>
<label for="DHT_read_interval">Read interval:</label>
<input name="DHT_read_interval" class="w3-input" id="DHT_read_interval" type="number" min="1" max="3600" value="<?= $DHT_read_interval ?>" >
</td>
</tr>

<tr>
<td>
<label for="DHT_type">Type:</label>
  <select name="DHT_type" class="w3-select" id="DHT_type">
  <option value="DHT11" <?php if ($DHT_type == 'DHT11') echo 'selected="selected"'; ?> >DHT11</option>
  <option value="DHT22" <?php if ($DHT_type == 'DHT22') echo 'selected="selected"'; ?> >DHT22</option>
  <option value="AM2302" <?php if ($DHT_type == 'AM2302') echo 'selected="selected"'; ?> >AM2302</option>
</select>
</td>
</tr>
<tr>
<td>
<label for="DHT_pin">Pin:</label>
<select name="DHT_pin" class="w3-select" id="DHT_pin">
  <option value = 17>17</option>
</select>
</td>
</tr>
    </table>
</div>
</fieldset>

<fieldset>
<legend>Weather sensor configuration</legend>
<div>

<table class="w3-table">
<tr>
<td>
<label>Rainfall</label>
</td>
</tr>

<tr>
<td>
<label>Use Rainfall:</label>
<input name="rainfall_use" type="hidden" value="no"><input name="rainfall_use" type="checkbox" class="w3-check" <?php if ($rainfall_use) echo 'checked="checked"'; ?> value="True">
</td>
</tr>

<tr>
<td>
<label for="rainfall_acquisition_time">Aquisition time:</label>
<input name="rainfall_acquisition_time" class="w3-input" id="rainfall_acquisition_time" type="number" min="1" max="3600" value="<?= $rainfall_acquisition_time ?>" >
</td>
</tr>
<tr>
<td>
<label for="rainfall_agregation_time">Agregation time:</label>
<input name="rainfall_agregation_time" class="w3-input" id="rainfall_agregation_time" type="number" min="1" max="86400" value="<?= $rainfall_agregation_time ?>" >
</td>
</tr>
<tr>
<td>
<label for="rainfall_sensor_pin">Sensor pin:</label>
<select  name="rainfall_sensor_pin" class="w3-select" id="rainfall_sensor_pin">
  <option value = 22>22</option>
</select>
</td>
</tr>
</table>
<br>


<table class="w3-table">
<tr>
<td>
<label>Wind speed</label>
</td>
</tr>

<tr>
<td>
<label>Use Wind speed:</label>
<input name="windspeed_use" type="hidden" value="no"><input name="windspeed_use" type="checkbox" class="w3-check" <?php if ($windspeed_use) echo 'checked="checked"'; ?> value="True">
</td>
</tr>

<tr>
<td>
<label for="windspeed_acquisition_time">Acquisition time:</label>
<input name="windspeed_acquisition_time" class="w3-input" id="windspeed_acquisition_time" type="number" min="1" max="3600" value="<?= $windspeed_acquisition_time ?>" >
</td>
</tr>
<tr>
<td>
<label for="windspeed_agregation_time">Agregation time:</label>
<input name="windspeed_agregation_time" class="w3-input" id="windspeed_agregation_time" type="number" min="1" max="3600" value="<?= $windspeed_agregation_time ?>" >
</td>
</tr>
<tr>
<td>
<label for="windspeed_sensor_pin">Sensor pin:</label>
<select name="windspeed_sensor_pin" class="w3-select" id="windspeed_sensor_pin">
  <option value = 23>23</option>
</select>
</td>
</tr>
</table>
<br>


<table class="w3-table">
<tr>
<td>
<label>Wind direction</label>
</td>
<tr>

<tr>
<td>
<label>Use Wind direction:</label>
<input name="winddirection_use" type="hidden" value="no"><input name="winddirection_use" type="checkbox" class="w3-check" <?php if ($winddirection_use) echo 'checked="checked"'; ?> value="True">
</td>
</tr>

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
</tr>
<tr>
<td>
<label for="winddirection_adc_input">Sensor input:</label>
<select name="winddirection_adc_input" class="w3-select" id="winddirection_adc_input">
 <option value="1" <?php if ($winddirection_adc_input == '1') echo 'selected="selected"'; ?> >1</option>
 <option value="2" <?php if ($winddirection_adc_input == '2') echo 'selected="selected"'; ?> >2</option>
 <option value="3" <?php if ($winddirection_adc_input == '3') echo 'selected="selected"'; ?> >3</option>
 <option value="4" <?php if ($winddirection_adc_input == '4') echo 'selected="selected"'; ?> >4</option>
</select>
</td>
</tr>
<tr>
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
<?php
$gpiopin = array("5", "6","13","16","19","20","21","26",);

foreach ($gpiopin as $pin) {

$_name = 'GPIO_'.$pin;
$gpio_name_value = $GPIO[$_name]['name'];
$gpio_input_type_value = $GPIO[$_name]['type'];
$gpio_hold_time_value = $GPIO[$_name]['hold_time'];

$gpio_input_pin = GPIO_.$pin."[gpio_pin]";
$gpio_input_holdtime_name = GPIO_.$pin."[hold_time]";

$gpio_select_name = GPIO_.$pin."[type]";
$gpio_select_id = GPIO_.$pin._TYPE;

$gpio_input_holdtime_id_ds = GPIO_.$pin._TYPE_DS;
$gpio_input_holdtime_id_ds_ht = GPIO_.$pin._TYPE_DS_HT;

$gpio_input_name_name = GPIO_.$pin."[name]";

echo "<div><table class='w3-table'>";
echo "<tr><td>";
echo "<label>GPIO $pin<input name='$gpio_input_pin' type='hidden' value='$pin'></label>";
echo "</td></tr>";
echo "<tr><td>";
echo "<label for='GPIO_.$pin'>Input type:</label>";
echo "<select name='$gpio_select_name' class='gpioinputs' id='$gpio_select_id'>";

if ($gpio_input_type_value == 'DoorSensor')
{
    echo "<option selected value='DoorSensor'>Door Sensor</option>";
    echo "<option value='MotionSensor'>Motion Sensor</option>";
    echo "<option value='Reserved'>Reserved</option>";
    echo "<option value='ShutdownButton'>Shutdown Button</option>";
}
if ($gpio_input_type_value == 'MotionSensor')
{
    echo "<option value='DoorSensor'>Door Sensor</option>";
    echo "<option selected value='MotionSensor'>Motion Sensor</option>";
    echo "<option value='Reserved'>Reserved</option>";
    echo "<option value='ShutdownButton'>Shutdown Button</option>";
}
if ($gpio_input_type_value == 'Reserved')
{
    echo "<option value='DoorSensor'>Door Sensor</option>";
    echo "<option value='MotionSensor'>Motion Sensor</option>";
    echo "<option selected value='Reserved'>Reserved</option>";
    echo "<option value='ShutdownButton'>Shutdown Button</option>";
}

if ($gpio_input_type_value == 'ShutdownButton')
{
    echo "<option value='DoorSensor'>Door Sensor</option>";
    echo "<option value='MotionSensor'>Motion Sensor</option>";
    echo "<option value='Reserved'>Reserved</option>";
    echo "<option selected value='ShutdownButton'>Shutdown Button</option>";
}

echo "</select></td></tr>";
echo "<tr><td><label>Name: <input name='$gpio_input_name_name' class='w3-input' type='text' value='$gpio_name_value'></label></td>";
echo "<tr><td><label id='$gpio_input_holdtime_id_ds'>Hold time: <input id='$gpio_input_holdtime_id_ds_ht' name='$gpio_input_holdtime_name' class='w3-input' type='number' min='1' max='60' value='$gpio_hold_time_value'></label></td></tr>";
echo "</tr></table></div>";
echo "<br>";
}
?>
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
<select  name="GPIO_12[type]" class="w3-select" id="GPIO_12">
  <option <?php if ($GPIO['GPIO_12']['type'] == 'door_led') echo 'selected="selected"'; ?> value="door_led">Door Indicator</option>
  <option <?php if ($GPIO['GPIO_12']['type'] == 'led') echo 'selected="selected"'; ?>value="led">LED</option>
</select>
</td>
</tr>
<tr>
<td>
<label>Name: <input name="GPIO_12[name]" class="w3-input" type="text" value="<?=$GPIO['GPIO_12']['name']?>"></label></td>
</tr>
</table>
<br>

<table class="w3-table">
<tr>
<td>
<label for="GPIO_18">GPIO 18<input name="GPIO_18[gpio_pin]" type="hidden" value="18"></label>
</td>
</tr>
<tr>
<td>
<label for="GPIO_18">Output type:</label>
<select  name="GPIO_18[type]" class="w3-select" id="GPIO_18">
  <option <?php if ($GPIO['GPIO_18']['type'] == 'motion_led') echo 'selected="selected"'; ?> value="motion_led">Motion Indicator</option>
  <option <?php if ($GPIO['GPIO_18']['type'] == 'led') echo 'selected="selected"'; ?>value="led">LED</option>
</select>
</td>
</tr>
<tr>
<td>
<label>Name: <input name="GPIO_18[name]" class="w3-input" type="text" value="<?=$GPIO['GPIO_18']['name']?>"></label></td>
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
<button name="save" type="submit"  value="Save" class="w3-bar">Save</button>
</div>
</fieldset>


</form>

</div>
</body>
</html>
