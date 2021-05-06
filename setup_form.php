<?php

if ($_POST['GPIO_16']['type'] == 'ShutdownButton') {
    $use_system_buttons = true;
} else {
    $use_system_buttons = false;
}

if ($_POST['GPIO_12']['type'] == 'door_led') {
    $use_door_led_indicator = true;
} else {
    $use_door_led_indicator = false;
}

if ($_POST['GPIO_18']['type'] == 'motion_led') {
    $use_motion_led_indicator = true;
} else {
    $use_motion_led_indicator = false;
}

$setup = array(
    "verbose" => filter_var($_POST['verbose'], FILTER_VALIDATE_BOOLEAN),
    "show_sys_info" => filter_var($_POST['show_sys_info'], FILTER_VALIDATE_BOOLEAN),
    "use_zabbix_sender" => filter_var($_POST['use_zabbix_sender'], FILTER_VALIDATE_BOOLEAN),
    "use_picamera" => filter_var($_POST['use_picamera'], FILTER_VALIDATE_BOOLEAN),
    "use_picamera_recording" => filter_var($_POST['use_picamera_recording'], FILTER_VALIDATE_BOOLEAN),
    "use_door_sensor" => filter_var($_POST['use_door_sensor'], FILTER_VALIDATE_BOOLEAN),
    "use_motion_sensor" => filter_var($_POST['use_motion_sensor'], FILTER_VALIDATE_BOOLEAN),
    "use_system_buttons" => filter_var($use_system_buttons, FILTER_VALIDATE_BOOLEAN),
    "use_door_led_indicator" => filter_var($use_door_led_indicator, FILTER_VALIDATE_BOOLEAN),
    "use_motion_led_indicator" => filter_var($use_motion_led_indicator, FILTER_VALIDATE_BOOLEAN),
    "use_CPU_sensor" => filter_var($_POST['use_CPU_sensor'], FILTER_VALIDATE_BOOLEAN),
    "use_BME280_sensor" => filter_var($_POST['use_BME280_sensor'], FILTER_VALIDATE_BOOLEAN),
    "use_DS18B20_sensor" => filter_var($_POST['use_DS18B20_sensor'], FILTER_VALIDATE_BOOLEAN),
    "use_DHT_sensor" => filter_var($_POST['use_DHT_sensor'], FILTER_VALIDATE_BOOLEAN),
    "use_weather_station" => filter_var($_POST['use_weather_station'], FILTER_VALIDATE_BOOLEAN),
    "use_serial_display" => filter_var($_POST['use_serial_display'], FILTER_VALIDATE_BOOLEAN),

    "serial_display_type" => $_POST['serial_display_type'],
    "serial_type" => $_POST['serial_type'],
    "serial_display_rotate" => (int)$_POST['serial_display_rotate'],
    "serial_display_refresh_rate" => (int)$_POST['serial_display_refresh_rate'],
);

$BME280["id1"] = array(
    "id" => 'id1',
    "name" => $_POST['id1_BME280_name'],
    "use" => filter_var($_POST['id1_BME280_use'], FILTER_VALIDATE_BOOLEAN),
    "read_interval" => (int)$_POST['id1_BME280_read_interval'],
    "interface" => $_POST['id1_BME280_interface'],
    "i2c_address" => (int)$_POST['id1_BME280_i2c_address'],
);

$BME280["id2"] = array(
    "id" => 'id2',
    "name" => $_POST['id2_BME280_name'],
    "use" => filter_var($_POST['id2_BME280_use'], FILTER_VALIDATE_BOOLEAN),
    "read_interval" => (int)$_POST['id2_BME280_read_interval'],
    "interface" => $_POST['id2_BME280_interface'],
    "serial_port" => $_POST['id2_BME280_serial_port'],
);

$BME280["id3"] = array(
    "id" => 'id3',
    "name" => $_POST['id3_BME280_name'],
    "use" => filter_var($_POST['id3_BME280_use'], FILTER_VALIDATE_BOOLEAN),
    "read_interval" => (int)$_POST['id3_BME280_read_interval'],
    "interface" => $_POST['id3_BME280_interface'],
    "serial_port" => $_POST['id3_BME280_serial_port'],
);

$DHT = array(
    "name" => $_POST['DHT_name'],
    "read_interval" => (int)$_POST['DHT_read_interval'],
    "type" => $_POST['DHT_type'],
    "pin" => $_POST['DHT_pin'],
);

$ONE_WIRE["DS18B20"] = array(
    "read_interval" => (int)$_POST['DS18B20_read_interval'],
    "addresses" => $_POST['DS18B20'],
);


/*foreach ($DS18B20_sensors_detected as $key => $value)
{
    $ONE_WIRE["DS18B20"]["addresses"] = $_POST[$value]['name'];
    var_dump($_POST[$value]);
}
*/

$CPU["temp"] = array(
    "read_interval" => (int)$_POST['CPUtemp_read_interval'],
);

$WEATHER["WIND"]["SPEED"] = array(
    "use" => filter_var($_POST['windspeed_use'], FILTER_VALIDATE_BOOLEAN),
    "sensor_pin" => (int)$_POST['windspeed_sensor_pin'],
    "acquisition_time" => (int)$_POST['windspeed_acquisition_time'],
    "agregation_time" => (int)$_POST['windspeed_agregation_time'],
);

$WEATHER["WIND"]["DIRECTION"] = array(
    "use" => filter_var($_POST['winddirection_use'], FILTER_VALIDATE_BOOLEAN),
    "acquisition_time" => (int)$_POST['winddirection_acquisition_time'],
    "adc_type" => $_POST['winddirection_adc_type'],
    "adc_input" => (int)$_POST['winddirection_adc_input'],
    "reference_voltage_adc_input" => (int)$_POST['reference_voltage_adc_input'],
);

$WEATHER["RAINFALL"] = array(
    "use" => filter_var($_POST['rainfall_use'], FILTER_VALIDATE_BOOLEAN),
    "sensor_pin" => (int)$_POST['rainfall_sensor_pin'],
    "acquisition_time" => (int)$_POST['rainfall_acquisition_time'],
    "agregation_time" => (int)$_POST['rainfall_agregation_time'],
);

$sensors = array(
    "CPU" => $CPU,
    "BME280" => $BME280,
    "ONE_WIRE" => $ONE_WIRE,
    "DHT" => $DHT,
    "WEATHER" => $WEATHER,
);

$GPIO = array(
    "GPIO_5" => $_POST['GPIO_5'],
    "GPIO_6" => $_POST['GPIO_6'],
    "GPIO_12" => $_POST['GPIO_12'],
    "GPIO_13" => $_POST['GPIO_13'],
    "GPIO_16" => $_POST['GPIO_16'],
    "GPIO_18" => $_POST['GPIO_18'],
    "GPIO_19" => $_POST['GPIO_19'],
    "GPIO_20" => $_POST['GPIO_20'],
    "GPIO_21" => $_POST['GPIO_21'],
    "GPIO_26" => $_POST['GPIO_26'],
);

$zabbix_agent = array(
    "zabbix_server" => $_POST['zabbix_server'],
    "zabbix_server_active" => $_POST['zabbix_server_active'],
    "location" => $_POST['location'],
    "hostname" => $_POST['hostname'],
    "chassis"  => "embedded",
    "deployment" => "RPiMS",
    "TLSPSKIdentity" => $_POST['TLSPSKIdentity'],
    "TLSConnect" => "psk",
    "TLSAccept" => "psk",
    "TLSPSK" =>  $_POST['TLSPSK'],
    "TLSPSKFile" => "/var/www/html/conf/zabbix_agentd.psk",
    "Timeout" => (int)$_POST['Timeout'],
);

$rpims = array(
    "setup"          => $setup,
    "sensors"        => $sensors,
    "gpio"           => $GPIO,
    "zabbix_agent"   => $zabbix_agent,
);

yaml_emit_file ("/var/www/html/conf/rpims.yaml", $rpims, YAML_UTF8_ENCODING, YAML_ANY_BREAK);
exec('sudo /bin/systemctl restart rpims.service');

$zabconfile = fopen("/var/www/html/conf/zabbix_agentd.conf", "w") or die("Unable to open file!");
$zabpskfile = fopen("/var/www/html/conf/zabbix_agentd.psk", "w") or die("Unable to open file!");
$Hostname="Hostname=".$zabbix_agent["hostname"]."\n";
$Server="Server=127.0.0.1,".$zabbix_agent["zabbix_server"]."\n";
$ServerActive="ServerActive=".$zabbix_agent["zabbix_server_active"]."\n";
$TLSPSKIdentity="TLSPSKIdentity=".$zabbix_agent["TLSPSKIdentity"]."\n";
$TLSConnect="TLSConnect=".$zabbix_agent["TLSConnect"]."\n";
$TLSAccept="TLSAccept=".$zabbix_agent["TLSAccept"]."\n";
$Timeout="Timeout=".$zabbix_agent["Timeout"]."\n";
$TLSPSKFile="TLSPSKFile=".$zabbix_agent["TLSPSKFile"]."\n";
$TLSPSK=$zabbix_agent["TLSPSK"];

fwrite($zabconfile, $Server);
fwrite($zabconfile, $ServerActive);
fwrite($zabconfile, $Hostname);
fwrite($zabconfile, $TLSPSKIdentity);
fwrite($zabconfile, $TLSPSKFile);
fwrite($zabconfile, $TLSConnect);
fwrite($zabconfile, $TLSAccept);
fwrite($zabconfile, $Timeout);
fwrite($zabpskfile, $TLSPSK);
fclose($zabconfile);
fclose($zabpskfile);
exec('sudo /bin/systemctl restart zabbix-agent.service');

sleep(2);
header("Location: /");
?>
