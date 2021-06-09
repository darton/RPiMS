<!DOCTYPE html>
<html lang="en">
    <head>
        <title>RPiMS configuration</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="/css/w3.css">
        <link rel="stylesheet" href="/css/w3-colors-2020.css">
        <script src="../jquery.min.js"></script>
        <script src="setup.js" defer></script>
    </head>
    <body>
        <div class="w3-2020-brilliant-white">
            <form action="setup_form.php" method="post">
                <fieldset>
                    <legend>System configuration</legend>
                    <div class="w3-row w3-2020-green-sheen">
                        <div class="w3-container">
                            <p><input name="verbose" type="hidden" value="no"><input name="verbose" type="checkbox" class="w3-check" <?php if ($verbose) echo 'checked="checked"'; ?> value="True">
                            <label>Verbose mode</label></p>
                            <p><input name="show_sys_info" type="hidden" value="False"><input name="show_sys_info" type="checkbox" class="w3-check" <?php if ($show_sys_info == 'yes') echo 'checked="checked"'; ?> value="True">
                            <label>Show system info</label></p>
                            <p><input name="use_picamera_recording" type="hidden" value="False"><input name="use_picamera_recording" type="checkbox" class="w3-check"  <?php if ($use_picamera_recording == 'yes') echo 'checked="checked"'; ?> value="True">
                            <label>Use picamera recording</label></p>
                            <p><input name="use_door_sensor" type="hidden" value="False"><input name="use_door_sensor" type="checkbox" class="w3-check" <?php if ($use_door_sensor == 'yes') echo 'checked="checked"'; ?> value="True">
                            <label>Use door sensors</label></p>
                            <p><input name="use_motion_sensor" type="hidden" value="False"><input name="use_motion_sensor" type="checkbox" class="w3-check" <?php if ($use_motion_sensor == 'yes') echo 'checked="checked"'; ?> value="True">
                            <label>Use motion sensors</label></p>
                        </div>
                    </div>
                </fieldset>
                <fieldset>
                    <legend>Serial display configuration</legend>
                    <div class="w3-row w3-2020-ultramarine-green">
                        <div class="w3-container w3-margin-top w3-margin-bottom">
                            <input name="use_serial_display" type="hidden" value="False"><input name="use_serial_display" type="checkbox" class="w3-check" id="use_serial_display"<?php if ($use_serial_display == 'yes') echo 'checked="checked"'; ?> value="True">
                            <label>Use serial display</label>
                        </div>
                    </div>
                    <div id="serial_display" class="w3-row w3-2020-green-sheen">
                        <div class="w3-quarter w3-container w3-margin-top">
                            <label for="serial_type">Serial type:</label>
                            <select id="serial_type" name="serial_type" class="w3-select">
                                <option value="i2c"<?php if ($serial_type == 'i2c') echo 'selected="selected"'; ?> >i2c</option>
                                <option value="spi"<?php if ($serial_type == 'spi') echo 'selected="selected"'; ?> >spi</option>
                            </select>
                        </div>
                        <div class="w3-quarter w3-container w3-margin-top">
                            <label for="serial_display_type">Display type:</label>
                            <select id="serial_display_type" name="serial_display_type" class="w3-select">
                                <option value="oled_sh1106"<?php if ($serial_display_type == 'oled_sh1106') echo 'selected="selected"'; ?> >oled_sh1106</option>
                                <option value="lcd_st7735"<?php if ($serial_display_type == 'lcd_st7735') echo 'selected="selected"'; ?> >lcd_st7735</option>
                            </select>
                        </div>
                        <div class="w3-quarter w3-container w3-margin-top">
                            <label for="serial_display_rotate">Display rotate:</label>
                            <select id="serial_display_rotate" name="serial_display_rotate" class="w3-select">
                                <option value="0"<?php if ($serial_display_rotate == '0') echo 'selected="selected"'; ?> >0</option>
                                <option value="2"<?php if ($serial_display_rotate == '2') echo 'selected="selected"'; ?> >180</option>
                            </select>
                        </div>
                        <div class="w3-quarter w3-container w3-margin-top w3-margin-bottom">
                            <label >Refresh rate:</label>
                            <input name="serial_display_refresh_rate" class="w3-input" type="number" min="1" max="50" value="<?= $serial_display_refresh_rate ?>" >
                        </div>
                    </div>
                </fieldset>
                <fieldset>
                    <legend>Pi Camera configuration</legend>
                    <div class="w3-row w3-2020-ultramarine-green">
                        <div class="w3-container w3-margin-top w3-margin-bottom">
                            <input name="use_picamera" type="hidden" value="False"><input name="use_picamera" type="checkbox" class="w3-check" id="use_picamera"<?php if ($use_picamera == 'yes') echo 'checked="checked"'; ?> value="True">
                            <label>Use Picamera</label>
                        </div>
                    </div>
                    <div id="picamera" class="w3-row w3-2020-green-sheen">
                        <div class="w3-quarter w3-container w3-margin-top">
                            <label for="picamera_rotation">Rotation:</label>
                            <select id="picamera_rotation" name="picamera_rotation" class="w3-select">
                                <option value="0"<?php if ($picamera_rotation == '0') echo 'selected="selected"'; ?> >0</option>
                                <option value="90"<?php if ($picamera_rotation == '90') echo 'selected="selected"'; ?> >90</option>
                                <option value="180"<?php if ($picamera_rotation == '180') echo 'selected="selected"'; ?> >180</option>
                                <option value="270"<?php if ($picamera_rotation == '270') echo 'selected="selected"'; ?> >270</option>
                            </select>
                        </div>
                        <div class="w3-quarter w3-container w3-margin-top">
                            <label for="picamera_mode">Mode:</label>
                            <select id="picamera_mode" name="picamera_mode" class="w3-select">
                                <option value="1"<?php if ($picamera_mode == '1') echo 'selected="selected"'; ?> >1920x1080</option>
                                <option value="6"<?php if ($picamera_mode == '6') echo 'selected="selected"'; ?> >1280x720</option>
                                <option value="7"<?php if ($picamera_mode == '7') echo 'selected="selected"'; ?> >640x480</option>
                            </select>
                        </div>
                        <div class="w3-quarter w3-container w3-margin-top w3-margin-bottom">
                            <label >FPS:</label>
                            <input name="picamera_fps" class="w3-input" type="number" min="1" max="60" value="<?= $picamera_fps ?>" >
                        </div>
                        <div class="w3-quarter w3-container w3-margin-top w3-margin-bottom">
                            <label >BITRATE:</label>
                            <input name="picamera_bitrate" class="w3-input" type="number" min="0" max="25000000" value="<?= $picamera_bitrate ?>" >
                        </div>
                    </div>
                </fieldset>
                <fieldset>
                    <legend>CPU sensor configuration</legend>
                    <div class="w3-row w3-2020-ultramarine-green">
                        <div class="w3-container w3-margin-top w3-margin-bottom">
                            <input name="use_CPU_sensor" type="hidden" value="False"><input name="use_CPU_sensor" type="checkbox" class="w3-check" id="use_CPU_sensor"<?php if ($use_CPU_sensor == 'yes') echo 'checked="checked"'; ?> value="True">
                            <label>Use CPU Sensor</label>
                        </div>
                    </div>
                    <div id="CPU_sensor" class="w3-row w3-2020-green-sheen">
                        <div class="w3-quarter w3-container w3-margin-top w3-margin-bottom">
                            <label for="CPUtemp_read_interval">CPUtemp read interval:</label>
                            <input name="CPUtemp_read_interval" class="w3-input" id="CPUtemp_read_interval" type="number" min="1" max="3600" value="<?= $CPUtemp_read_interval ?>" >
                        </div>
                    </div>
                </fieldset>
                <fieldset>
                    <legend>DS18B20 sensor configuration</legend>
                    <div class="w3-row w3-2020-ultramarine-green">
                        <div class="w3-container w3-margin-top w3-margin-bottom">
                            <input name="use_DS18B20_sensor" type="hidden" value="False"><input name="use_DS18B20_sensor" type="checkbox" class="w3-check" id="use_DS18B20_sensor"<?php if ($use_DS18B20_sensor == 'yes') echo 'checked="checked"'; ?> value="True">
                            <label>Use DS18B20 sensor</label>
                        </div>
                    </div>
                    <div id="DS18B20_sensor" class="w3-row w3-2020-green-sheen">
                        <div class="w3-quarter w3-container w3-margin-top w3-margin-bottom">
                            <label for="DS18B20_read_interval">Read interval:</label>
                            <input name="DS18B20_read_interval" class="w3-input" id="DS18B20_read_interval" type="number" min="1" max="3600" value="<?= $DS18B20_read_interval ?>" >
                            <br>
                        </div>
                        <?php
                            foreach ($DS18B20_sensors_detected as $key => $value){
                            $DS18B20_name = $DS18B20_sensors[$value];
                            echo "<div class='w3-row w3-margin-top w3-margin-bottom'>";
                            echo "<div class='w3-quarter w3-container w3-margin-bottom'>";
                            echo "<label>Address:</label>";
                            echo "<input class='w3-input' type='text' value='$value'>";
                            echo "</div>";
                            echo "<div class='w3-threequarter w3-container w3-margin-bottom'>";
                            echo "<label>name :</label>";
                            echo "<input name='DS18B20[$value][name]' class='w3-input' type='text' value='$DS18B20_name'>";
                            echo "</div>";
                            echo "</div>";
                            }
                        ?>
                    </div>
                </fieldset>
                <fieldset>
                    <legend>BME280 sensor configuration</legend>
                    <div class="w3-row w3-2020-ultramarine-green">
                        <div class="w3-container w3-margin-top w3-margin-bottom">
                            <input name="use_BME280_sensor" type="hidden" value="False"><input name="use_BME280_sensor" type="checkbox" class="w3-check" id="use_BME280_sensor"<?php if ($use_BME280_sensor == 'yes') echo 'checked="checked"'; ?> value="True">
                            <label>Use BME280 sensor</label>
                        </div>
                    </div>
                    <div id="BME280_sensor" class="w3-row">
                        <div class="w3-row w3-2020-ultramarine-green w3-margin-top">
                            <div class="w3-container w3-margin-top w3-margin-bottom">
                                <input name="id1_BME280_use" type="hidden" value="no"><input name="id1_BME280_use" type="checkbox" class="w3-check" id="id1_BME280_use" <?php if ($id1_BME280_use) echo 'checked="checked"'; ?> value="True">
                                <label>Use #1 BME280:</label>
                            </div>
                        </div>
                        <div id="id1_BME280" class="w3-row w3-2020-green-sheen">
                            <div class="w3-row w3-margin-bottom">
                                <div class="w3-quarter w3-container w3-margin-top">
                                    <label>name:</label>
                                    <input name="id1_BME280_name" class="w3-input" type="text" value="<?=$id1_BME280_name?>" >
                                </div>
                                <div class="w3-quarter w3-container w3-margin-top">
                                    <label for="id1_BME280_read_interval">Read interval:</label>
                                    <input name="id1_BME280_read_interval" class="w3-input" id="id1_BME280_read_interval" type="number" min="1" max="3600" value="<?= $id1_BME280_read_interval ?>" >
                                </div>
                                <div class="w3-quarter w3-container w3-margin-top">
                                    <label for="id1_BME280_interface">Interface type:</label>
                                    <select name="id1_BME280_interface" class="w3-select" id="id1_BME280_interface">
                                        <option <?php if ($id1_BME280_interface == 'i2c') echo 'selected="selected"'; ?> value = "i2c" >i2c</option>
                                    </select>
                                </div>
                                <div class="w3-quarter w3-container w3-margin-top">
                                    <label id="id1_BME280_i2c_address">I2C Address:
                                        <select name="id1_BME280_i2c_address" class="w3-select" >
                                            <option <?php if ($id1_BME280_i2c_address == '118') echo 'selected="selected"'; ?> value = "118" >0x76</option>
                                            <option <?php if ($id1_BME280_i2c_address == '119') echo 'selected="selected"'; ?> value = "119" >0x77</option>
                                        </select>
                                    </label>
                                </div>
                            </div>
                        </div>

                        <div class="w3-row w3-2020-ultramarine-green w3-margin-top">
                            <div class="w3-container w3-margin-top w3-margin-bottom">
                                <input name="id2_BME280_use" type="hidden" value="no"><input name="id2_BME280_use" type="checkbox" class="w3-check" id="id2_BME280_use" <?php if ($id2_BME280_use) echo 'checked="checked"'; ?> value="True">
                                <label>Use #2 BME280:</label>
                            </div>
                        </div>
                        <div id="id2_BME280" class="w3-row w3-2020-green-sheen">
                            <div class="w3-row w3-margin-bottom">
                                <div class="w3-quarter w3-container w3-margin-top">
                                    <label>name:</label>
                                    <input name="id2_BME280_name" class="w3-input" type="text" value="<?=$id2_BME280_name?>" >
                                </div>
                                <div class="w3-quarter w3-container w3-margin-top">
                                    <label for="id2_BME280_read_interval">Read interval:</label>
                                    <input name="id2_BME280_read_interval" class="w3-input" id="id2_BME280_read_interval" type="number" min="1" max="3600" value="<?= $id2_BME280_read_interval ?>" >
                                </div>
                                <div class="w3-quarter w3-container w3-margin-top">
                                    <label for="id2_BME280_interface">Interface type:</label>
                                    <select name="id2_BME280_interface" class="w3-select" id="id2_BME280_interface">
                                        <option <?php if ($id2_BME280_interface == 'serial') echo 'selected="selected"'; ?> value = "serial" >serial</option>
                                    </select>
                                </div>
                                <div class="w3-quarter w3-container w3-margin-top">
                                    <label id="id2_BME280_serial_port">Serial port:
                                        <select name="id2_BME280_serial_port" class="w3-select serial-port" id="id2_BME280_serial_port_select" >
                                            <option <?php if ($id2_BME280_serial_port == 'USB1') echo 'selected="selected"'; ?> value = "USB1" >USB1</option>
                                            <option <?php if ($id2_BME280_serial_port == 'USB2') echo 'selected="selected"'; ?> value = "USB2" >USB2</option>
                                            <option <?php if ($id2_BME280_serial_port == 'USB3') echo 'selected="selected"'; ?> value = "USB3" >USB3</option>
                                            <option <?php if ($id2_BME280_serial_port == 'USB4') echo 'selected="selected"'; ?> value = "USB4" >USB4</option>
                                        </select>
                                    </label>
                                </div>
                            </div>
                        </div>

                        <div class="w3-row w3-2020-ultramarine-green w3-margin-top">
                            <div class="w3-container w3-margin-top w3-margin-bottom">
                                <input name="id3_BME280_use" type="hidden" value="no"><input name="id3_BME280_use" type="checkbox" class="w3-check" id="id3_BME280_use" <?php if ($id3_BME280_use) echo 'checked="checked"'; ?> value="True">
                                <label>Use #3 BME280:</label>
                            </div>
                        </div>
                        <div id="id3_BME280" class="w3-row w3-2020-green-sheen">
                            <div class="w3-row w3-margin-bottom">
                                <div class="w3-quarter w3-container w3-margin-top">
                                    <label>name:</label>
                                    <input name="id3_BME280_name" class="w3-input" type="text" value="<?=$id3_BME280_name?>" >
                                </div>
                                <div class="w3-quarter w3-container w3-margin-top">
                                    <label for="id3_BME280_read_interval">Read interval:</label>
                                    <input name="id3_BME280_read_interval" class="w3-input" id="id3_BME280_read_interval" type="number" min="1" max="3600" value="<?= $id3_BME280_read_interval ?>" >
                                </div>
                                <div class="w3-quarter w3-container w3-margin-top">
                                    <label for="id3_BME280_interface">Interface type:</label>
                                    <select name="id3_BME280_interface" class="w3-select" id="id3_BME280_interface">
                                        <option <?php if ($id3_BME280_interface == 'serial') echo 'selected="selected"'; ?> value = "serial" >serial</option>
                                    </select>
                                </div>
                                <div class="w3-quarter w3-container w3-margin-top">
                                    <label id="id3_BME280_serial_port">Serial port:
                                        <select name="id3_BME280_serial_port" class="w3-select serial-port" id="id3_BME280_serial_port_select">
                                            <option <?php if ($id3_BME280_serial_port == 'USB1') echo 'selected="selected"'; ?> value = "USB1" >USB1</option>
                                            <option <?php if ($id3_BME280_serial_port == 'USB2') echo 'selected="selected"'; ?> value = "USB2" >USB2</option>
                                            <option <?php if ($id3_BME280_serial_port == 'USB3') echo 'selected="selected"'; ?> value = "USB3" >USB3</option>
                                            <option <?php if ($id3_BME280_serial_port == 'USB4') echo 'selected="selected"'; ?> value = "USB4" >USB4</option>
                                        </select>
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>
                </fieldset>
                <fieldset>
                    <legend>DHT sensor configuration</legend>
                    <div class="w3-row w3-2020-ultramarine-green">
                        <div class="w3-container w3-margin-top w3-margin-bottom">
                            <input name="use_DHT_sensor" type="hidden" value="False"><input name="use_DHT_sensor" type="checkbox" class="w3-check" id="use_DHT_sensor"<?php if ($use_DHT_sensor) echo 'checked="checked"'; ?> value="True">
                            <label>Use DHT sensor</label>
                        </div>
                    </div>
                    <div id="DHT_sensor" class="w3-row w3-2020-green-sheen">
                        <div class="w3-row w3-margin-bottom">
                            <div class="w3-quarter w3-container w3-margin-top">
                                <label for="DHT_type">Type:</label>
                                <select name="DHT_type" class="w3-select" id="DHT_type">
                                    <option <?php if ($DHT_type == 'DHT11') echo 'selected="selected"'; ?> value="DHT11" >DHT11</option>
                                    <option <?php if ($DHT_type == 'DHT22') echo 'selected="selected"'; ?> value="DHT22" >DHT22</option>
                                    <option <?php if ($DHT_type == 'AM2302') echo 'selected="selected"'; ?> value="AM2302" >AM2302</option>
                                </select>
                            </div>
                            <div class="w3-quarter w3-container w3-margin-top">
                                <label>name:</label>
                                <input name="DHT_name" class="w3-input" type="text" value="<?=$DHT_name?>" >
                            </div>
                            <div class="w3-quarter w3-container w3-margin-top">
                                <label for="DHT_read_interval">Read interval:</label>
                                <input name="DHT_read_interval" class="w3-input" id="DHT_read_interval" type="number" min="1" max="3600" value="<?= $DHT_read_interval ?>" >
                            </div>
                            <div class="w3-quarter w3-container w3-margin-top">
                                <label for="DHT_pin">Pin:</label>
                                <select name="DHT_pin" class="w3-select" id="DHT_pin">
                                    <option value = 17>17</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </fieldset>
                <fieldset>
                    <legend>Weather sensor configuration</legend>
                    <div class="w3-row w3-2020-ultramarine-green">
                        <div class="w3-container w3-margin-top w3-margin-bottom">
                            <input name="use_weather_station" type="hidden" value="False"><input name="use_weather_station" type="checkbox" class="w3-check" id="use_weather_station" <?php if ($use_weather_station) echo 'checked="checked"'; ?> value="True">
                            <label>Use weather station</label>
                        </div>
                    </div>
                    <div id="weather_station" class="w3-row">
                        <div class="w3-row w3-2020-green-sheen w3-margin-top">
                            <div class="w3-row w3-2020-ultramarine-green">
                                <div class="w3-container w3-margin-top w3-margin-bottom">
                                <input name="rainfall_use" type="hidden" value="no"><input name="rainfall_use" type="checkbox" class="w3-check" <?php if ($rainfall_use) echo 'checked="checked"'; ?> value="True">
                                <label>Use Rainfall:</label>
                                </div>
                            </div>
                            <div class="w3-row w3-margin-bottom">
                                <div class="w3-third w3-container w3-margin-top">
                                    <label for="rainfall_acquisition_time">Aquisition time:</label>
                                    <input name="rainfall_acquisition_time" class="w3-input" id="rainfall_acquisition_time" type="number" min="1" max="3600" value="<?= $rainfall_acquisition_time ?>" >
                                </div>
                                <div class="w3-third w3-container w3-margin-top">
                                    <label for="rainfall_agregation_time">Agregation time:</label>
                                    <input name="rainfall_agregation_time" class="w3-input" id="rainfall_agregation_time" type="number" min="1" max="86400" value="<?= $rainfall_agregation_time ?>" >
                                </div>
                                <div class="w3-third w3-container w3-margin-top">
                                    <label for="rainfall_sensor_pin">Sensor pin:</label>
                                    <select  name="rainfall_sensor_pin" class="w3-select" id="rainfall_sensor_pin">
                                        <option value = 22>22</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        <div class="w3-row w3-2020-green-sheen w3-margin-top">
                            <div class="w3-row w3-2020-ultramarine-green">
                                <div class="w3-container w3-margin-top w3-margin-bottom">
                                    <input name="windspeed_use" type="hidden" value="no"><input name="windspeed_use" type="checkbox" class="w3-check" <?php if ($windspeed_use) echo 'checked="checked"'; ?> value="True">
                                    <label>Use Wind speed:</label>
                                </div>
                            </div>
                            <div class="w3-row w3-margin-bottom">
                                <div class="w3-third w3-container w3-margin-top">
                                    <label for="windspeed_acquisition_time">Acquisition time:</label>
                                    <input name="windspeed_acquisition_time" class="w3-input" id="windspeed_acquisition_time" type="number" min="1" max="3600" value="<?= $windspeed_acquisition_time ?>" >
                                </div>
                                <div class="w3-third w3-container w3-margin-top">
                                    <label for="windspeed_agregation_time">Agregation time:</label>
                                    <input name="windspeed_agregation_time" class="w3-input" id="windspeed_agregation_time" type="number" min="1" max="3600" value="<?= $windspeed_agregation_time ?>" >
                                </div>
                                <div class="w3-third w3-container w3-margin-top">
                                    <label for="windspeed_sensor_pin">Sensor pin:</label>
                                    <select name="windspeed_sensor_pin" class="w3-select" id="windspeed_sensor_pin">
                                        <option value = 23>23</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        <div class="w3-row w3-2020-green-sheen w3-margin-top">
                            <div class="w3-row w3-2020-ultramarine-green">
                                <div class="w3-container w3-margin-top w3-margin-bottom">
                                    <input name="winddirection_use" type="hidden" value="no"><input name="winddirection_use" type="checkbox" class="w3-check" <?php if ($winddirection_use) echo 'checked="checked"'; ?> value="True">
                                    <label>Use Wind direction:</label>
                                </div>	
                            </div>
                            <div class="w3-row w3-margin-bottom">
                            <div class="w3-quarter w3-container w3-margin-top">
                                <label for="winddirection_acquisition_time">Acquisition time:</label>
                                <input name="winddirection_acquisition_time" class="w3-input" id="winddirection_acquisition_time" type="number" min="1" max="3600" value="<?= $winddirection_acquisition_time ?>" >
                            </div>
                            <div class="w3-quarter w3-container w3-margin-top">
                                <label for="winddirection_adc_type">ADC type:</label>
                                <select name="winddirection_adc_type" class="w3-select" id="winddirection_adc_type">
                                    <option value="AutomationPhat" <?php if ($winddirection_adc_type == 'AutomationPhat') echo 'selected="selected"'; ?> >AutomationPhat</option>
                                    <option value="STM32F030" <?php if ($winddirection_adc_type == 'STM32F030') echo 'selected="selected"'; ?> >STM32F030</option>
                                    <option value="ADS1115" <?php if ($winddirection_adc_type == 'ADS1115') echo 'selected="selected"'; ?> >ADS1115</option>
                                </select>
                            </div>
                            <div class="w3-quarter w3-container w3-margin-top">
                                <label for="winddirection_adc_input">Sensor input:</label>
                                <select name="winddirection_adc_input" class="w3-select" id="winddirection_adc_input">
                                    <option value="1" <?php if ($winddirection_adc_input == '1') echo 'selected="selected"'; ?> >1</option>
                                    <option value="2" <?php if ($winddirection_adc_input == '2') echo 'selected="selected"'; ?> >2</option>
                                    <option value="3" <?php if ($winddirection_adc_input == '3') echo 'selected="selected"'; ?> >3</option>
                                    <option value="4" <?php if ($winddirection_adc_input == '4') echo 'selected="selected"'; ?> >4</option>
                                </select>
                            </div>
                            <div class="w3-quarter w3-container w3-margin-top">
                                <label for="_adc_input">Reference input:</label>
                                <select name="reference_voltage_adc_input" class="w3-select" id="reference_voltage_adc_input">
                                    <option value="1" <?php if ($reference_voltage_adc_input == '1') echo 'selected="selected"'; ?> >1</option>
                                    <option value="2" <?php if ($reference_voltage_adc_input == '2') echo 'selected="selected"'; ?> >2</option>
                                    <option value="3" <?php if ($reference_voltage_adc_input == '3') echo 'selected="selected"'; ?> >3</option>
                                    <option value="4" <?php if ($reference_voltage_adc_input == '4') echo 'selected="selected"'; ?> >4</option>
                                </select>
                            </div>
                        </div>                   
                    </div>
                </fieldset>
                <fieldset>
                    <legend>GPIO configuration</legend>
                    <h2><input onclick="gpioSH('gpio')" type="button" value="GPIO" class="w3-btn w3-block w3-left-align w3-2020-ultramarine-green"></h2>
                    <div id="gpio" class="w3-row w3-hide">
                        <br>
                        <?php
                            $gpiopin = array("5","6","12","13","16","18","19","20","21","26",);

                            foreach ($gpiopin as $pin) {

                                $_name = 'GPIO_'.$pin;
                                $gpio_name_value = $GPIO[$_name]['name'];
                                $gpio_input_type_value = $GPIO[$_name]['type'];
                                $gpio_hold_time_value = $GPIO[$_name]['hold_time'];

                                $gpio_input_pin = "GPIO_".$pin."[gpio_pin]";
                                $gpio_input_holdtime_name = "GPIO_".$pin."[hold_time]";

                                $gpio_select_name = "GPIO_".$pin."[type]";
                                $gpio_select_id = "GPIO_".$pin."_TYPE";

                                $gpio_input_holdtime_id_ds = "GPIO_".$pin."_TYPE_DS";
                                $gpio_input_holdtime_id_ds_ht = "GPIO_".$pin."_TYPE_DS_HT";

                                $gpio_input_name_name = "GPIO_".$pin."[name]";

                                echo "<div class='w3-row w3-2020-ultramarine-green'>";
                                echo "<div class='w3-container w3-margin-top w3-margin-bottom'>";
                                echo "<label>GPIO $pin<input name='$gpio_input_pin' type='hidden' value='$pin'></label>";
                                echo "</div>";
                                echo "</div>";

                                echo "<div class='w3-row w3-margin-bottom w3-2020-green-sheen'>";
                                echo "<div class='w3-row w3-margin-bottom'>";
                                echo "<div class='w3-third w3-container w3-margin-top'>";
                                echo "<label for='GPIO_.$pin'>Type:</label>";
                                echo "<select name='$gpio_select_name' class='gpioinputs w3-select' id='$gpio_select_id'>";
                                if ($gpio_input_type_value == 'DoorSensor'){
                                    echo "<option selected value='DoorSensor'>INPUT - Door Sensor</option>";
                                    echo "<option value='MotionSensor'>INPUT - Motion Sensor</option>";
                                    echo "<option value='ShutdownButton'>INPUT - Shutdown Button</option>";
                                    echo "<option value='led'>OUT - LED</option>";
                                    echo "<option value='door_led'>OUT - Door Indicator</option>";
                                    echo "<option value='motion_led'>OUT - Motion Indicator</option>";
                                    echo "<option value='Reserved'>Reserved</option>";
                                }
                                if ($gpio_input_type_value == 'MotionSensor'){
                                    echo "<option value='DoorSensor'>INPUT - Door Sensor</option>";
                                    echo "<option selected value='MotionSensor'>INPUT - Motion Sensor</option>";
                                    echo "<option value='ShutdownButton'>INPUT - Shutdown Button</option>";
                                    echo "<option value='led'>OUT - LED</option>";
                                    echo "<option value='door_led'>OUT - Door Indicator</option>";
                                    echo "<option value='motion_led'>OUT - Motion Indicator</option>";
                                    echo "<option value='Reserved'>Reserved</option>";
                                }
                                if ($gpio_input_type_value == 'Reserved'){
                                    echo "<option value='DoorSensor'>INPUT - Door Sensor</option>";
                                    echo "<option value='MotionSensor'>INPUT - Motion Sensor</option>";
                                    echo "<option value='ShutdownButton'>INPUT - Shutdown Button</option>";
                                    echo "<option value='led'>OUT - LED</option>";
                                    echo "<option value='door_led'>OUT - Door Indicator</option>";
                                    echo "<option value='motion_led'>OUT - Motion Indicator</option>";
                                    echo "<option selected value='Reserved'>Reserved</option>";
                                }
                                if ($gpio_input_type_value == 'ShutdownButton'){
                                    echo "<option value='DoorSensor'>INPUT - Door Sensor</option>";
                                    echo "<option value='MotionSensor'>INPUT - Motion Sensor</option>";
                                    echo "<option selected value='ShutdownButton'>INPUT - Shutdown Button</option>";
                                    echo "<option value='led'>OUT - LED</option>";
                                    echo "<option value='door_led'>OUT - Door Indicator</option>";
                                    echo "<option value='motion_led'>OUT - Motion Indicator</option>";
                                    echo "<option value='Reserved'>Reserved</option>";
                                }
                                if ($gpio_input_type_value == 'led'){
                                    echo "<option value='DoorSensor'>INPUT - Door Sensor</option>";
                                    echo "<option value='MotionSensor'>INPUT - Motion Sensor</option>";
                                    echo "<option value='ShutdownButton'>INPUT - Shutdown Button</option>";
                                    echo "<option selected value='led'>OUT - LED</option>";
                                    echo "<option value='door_led'>OUT - Door Indicator</option>";
                                    echo "<option value='motion_led'>OUT - Motion Indicator</option>";
                                    echo "<option value='Reserved'>Reserved</option>";
                                }
                                if ($gpio_input_type_value == 'door_led'){
                                    echo "<option value='DoorSensor'>INPUT - Door Sensor</option>";
                                    echo "<option value='MotionSensor'>INPUT - Motion Sensor</option>";
                                    echo "<option value='ShutdownButton'>INPUT - Shutdown Button</option>";
                                    echo "<option value='led'>OUT - LED</option>";
                                    echo "<option selected value='door_led'>OUT - Door Indicator</option>";
                                    echo "<option value='motion_led'>OUT - Motion Indicator</option>";
                                    echo "<option value='Reserved'>Reserved</option>";
                                }
                                if ($gpio_input_type_value == 'motion_led'){
                                    echo "<option value='DoorSensor'>INPUT - Door Sensor</option>";
                                    echo "<option value='MotionSensor'>INPUT - Motion Sensor</option>";
                                    echo "<option value='ShutdownButton'>INPUT - Shutdown Button</option>";
                                    echo "<option value='led'>OUT - LED</option>";
                                    echo "<option value='door_led'>OUT - Door Indicator</option>";
                                    echo "<option selected value='motion_led'>OUT - Motion Indicator</option>";
                                    echo "<option value='Reserved'>Reserved</option>";
                                }
                                echo "</select>";
                                echo "</div>";
                                echo "<div class='w3-third w3-container w3-margin-top'>";
                                echo "<label>Name:<input name='$gpio_input_name_name' class='w3-input'  type='text' value='$gpio_name_value'></label>";
                                echo "</div>";
                                echo "<div class='w3-third w3-container w3-margin-top'>";
                                echo "<label id='$gpio_input_holdtime_id_ds'>Hold time:<input id='$gpio_input_holdtime_id_ds_ht' name='$gpio_input_holdtime_name' class='w3-input' type='number' min='1' max='60' value='$gpio_hold_time_value'></label>";
                                echo "</div>";
                                echo "</div>";
                                echo "</div>";
                            }
                        ?>
                    </div>
                </fieldset>
                <fieldset>
                    <legend>Zabbix Agent configuration</legend>
                    <div class="w3-row w3-2020-ultramarine-green">
                            <div class="w3-container  w3-margin-top w3-margin-bottom">
                                <input name="use_zabbix_sender" type="hidden" value="False"><input name="use_zabbix_sender" type="checkbox" class="w3-check" <?php if ($use_zabbix_sender == 'yes') echo 'checked="checked"'; ?> value="True">
                                <label >Use zabbix sender</label>
                            </div>
                    </div>  
                    <div>
                        <div class="w3-row w3-2020-green-sheen">
                            <p>
                            <div class="w3-third w3-container w3-margin-bottom">
                                <label>Zabbix server:</label>
                                <input name="zabbix_server" class="w3-input" type="text" placeholder="zabbix.example.com" value="<?=$zabbix_server?>" pattern="^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$">
                            </div>
                            <div class="w3-third w3-container w3-margin-bottom">
                                <label>Zabbix server Active:</label>
                                <input name="zabbix_server_active" class="w3-input" type="text" value="<?=$zabbix_server_active?>" placeholder="zabbix.example.com" pattern="^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$">
                            </div>
                            <div class="w3-third w3-container w3-margin-bottom">
                                <label>Timeout:</label>
                                <input name="Timeout" class="w3-input" type="number" min="1" max="10" value="<?=$Timeout?>" >
                            </div>
                            </p>
                        </div>
                        <div class="w3-row w3-2020-green-sheen">
                            <div class="w3-half w3-container w3-margin-bottom">
                                <label>RPiMS location:</label>
                                <input name="location" class="w3-input" type="text" value="<?=$location?>" >
                            </div>
                            <div class="w3-half w3-container w3-margin-bottom">
                                <label>RPiMS hostname:</label>
                                <input name="hostname" class="w3-input" type="text" value="<?=$hostname?>" >
                            </div>
                        </div>
                        <div class="w3-row w3-2020-green-sheen">
                            <div class="w3-half w3-container w3-margin-bottom">
                                <label>PSK identity:</label>
                                <input name="TLSPSKIdentity" class="w3-input" id="TLSPSKIdentity" type="text" value="<?=$TLSPSKIdentity?>">
                                <input class="w3-input w3-2020-classic-blue" type="button" onclick="gfg_Run(16,tlspskidentityid)" value="Generate PSK Identity">
                            </div>
                            <div class="w3-half w3-container w3-margin-bottom">
                                <label>PSK:</label>
                                <input name="TLSPSK" class="w3-input" id="TLSPSK" type="text" value="<?=$TLSPSK?>" >
                                <input class="w3-input w3-2020-classic-blue" type="button" onclick="gfg_Run(64,tlspskid)" value="Generate PSK">
                            </div>
                        </div>
                    </div>
                </fieldset>
                <fieldset>
                    <div class="w3-row w3-2020-green-sheen">
                        <div class="w3 w3-container w3-margin-top w3-margin-bottom">
                            <button name="save" type="submit"  value="Save" class="w3-bar w3-2020-samba w3-xlarge">Save</button>
                        </div>
                    </div>
                </fieldset>
            </form>
        </div>
    </body>
</html>
