<?php

$setup = array(
    "verbose" => filter_var($_POST['verbose'], FILTER_VALIDATE_BOOLEAN),
    "use_zabbix_sender" => filter_var($_POST['use_zabbix_sender'], FILTER_VALIDATE_BOOLEAN),
    "use_picamera" => filter_var($_POST['use_picamera'], FILTER_VALIDATE_BOOLEAN),
    "use_picamera_recording" => filter_var($_POST['use_picamera_recording'], FILTER_VALIDATE_BOOLEAN),
    "use_door_sensor" => filter_var($_POST['use_door_sensor'], FILTER_VALIDATE_BOOLEAN),
    "use_motion_sensor" => filter_var($_POST['use_motion_sensor'], FILTER_VALIDATE_BOOLEAN),
    "use_system_buttons" => filter_var($_POST['use_system_buttons'], FILTER_VALIDATE_BOOLEAN),
    "use_led_indicators" => filter_var($_POST['use_led_indicator'], FILTER_VALIDATE_BOOLEAN),
    "use_serial_display" => filter_var($_POST['use_serial_display'], FILTER_VALIDATE_BOOLEAN),
    "use_serial_display" => filter_var($_POST['use_serial_display'], FILTER_VALIDATE_BOOLEAN),
    "use_CPU_sensor" => filter_var($_POST['use_CPU_sensor'], FILTER_VALIDATE_BOOLEAN),
    "use_BME280_sensor" => filter_var($_POST['use_BME280_sensor'], FILTER_VALIDATE_BOOLEAN),
    "use_DS18B20_sensor" => filter_var($_POST['use_DS18B20_sensor'], FILTER_VALIDATE_BOOLEAN),
    "use_DHT_sensor" => filter_var($_POST['use_DHT_sensor'], FILTER_VALIDATE_BOOLEAN),

    "serial_display_type" => $_POST['serial_display_type'],
    "serial_display_refresh_rate" => (int)$_POST['serial_display_refresh_rate'],

    "CPUtemp_read_interval" => (int)$_POST['CPUtemp_read_interval'],

    "BME280_read_interval" => (int)$_POST['BME280_read_interval'],
    "BME280_i2c_address" => $_POST['BME280_i2c_address'],

    "DS18B20_read_interval" => (int)$_POST['DS18B20_read_interval'],

    "DHT_read_interval" => (int)$_POST['DHT_read_interval'],
    "DHT_type" => $_POST['DHT_type'],
    "DHT_pin" => (int)$_POST['DHT_pin'],
);

$door_sensors = array();
$system_buttons = array();
$motion_sensors = array();
$led_indicators = array();

$count = 1;
foreach ($_POST as $key => $value) {
    if ($value['type'] == 'DoorSensor'){
        $varname = 'door_sensor_'.$count;
        $door_sensors[$varname]['gpio_pin'] = (int)$value['gpio_pin'];
        $door_sensors[$varname]['hold_time'] = (int)$value['hold_time'];
    $count++;
}
}

$count = 1;
foreach ($_POST as $key => $value) {
    if ($value['type'] == 'MotionSensor'){
        $varname = 'motion_sensor_'.$count;
        $motion_sensors[$varname]['gpio_pin'] = (int)$value['gpio_pin'];
    $count++;
}
}

$arrayName = 'shutdown_button';
foreach ($_POST as $key => $value) {
    if ($value['type'] == 'ShutdownButton'){
        $system_buttons[$arrayName] = [];
        $system_buttons[$arrayName]['gpio_pin'] = (int)$value['gpio_pin'] ;
        $system_buttons[$arrayName]['hold_time'] = (int)$value['hold_time'];
    }
}


foreach ($_POST as $key => $value) {
    if ($value['type'] == 'door_led'){
        $led_indicators['door_led']['gpio_pin'] = (int)$value['gpio_pin'];
}
    if ($value['type'] == 'motion_led'){
        $led_indicators['motion_led']['gpio_pin'] = (int)$value['gpio_pin'];
}
}

$zabbix_agent = array(
    "zabbix_server" => $_POST['zabbix_server'],
    "zabbix_server_active" => $_POST['zabbix_server_active'],
    "location" => $_POST['location'],
    "hostname" => $_POST['hostname'],
    "chassis"  => "embedded",
    "deployment" => "RPiMS",
);

$rpims = array(
    "setup" => $setup,
    "led_indicators" => $led_indicators,
    "door_sensors"   => $door_sensors,
    "motion_sensors" => $motion_sensors,
    "system_buttons" => $system_buttons,
    "zabbix_agent"   => $zabbix_agent,
);

yaml_emit_file ("/var/www/html/rpims.yaml", $rpims, YAML_UTF8_ENCODING, YAML_ANY_BREAK);

?>
