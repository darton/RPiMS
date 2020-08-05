
<?php

$setup = array(
    "verbose" => $_POST['verbose'],
    "use_zabbix_sender" => $_POST['use_zabbix_sender'],
    "use_picamera" => $_POST['use_picamera'],
    "use_door_sensor" => $_POST['use_door_sensor'],
    "use_motion_sensor" => $_POST['use_motion_sensor'],
    "use_system_buttons" => $_POST['use_system_buttons'],
    "use_led_indicators" => $_POST['use_led_indicator'],
    "use_serial_display" => $_POST['use_serial_display'],
    "use_serial_display" => $_POST['use_serial_display'],
    "serial_display_type" => $_POST['serial_display_type'],
    "serial_display_refresh_rate" => $_POST['serial_display_refresh_rate'],
    "use_CPU_sensor" => $_POST['use_CPU_sensor'],
    "CPUtemp_read_interval" => $_POST['CPUtemp_read_interval'],
    "use_BME280_sensor" => $_POST['use_BME280_sensor'],
    "BME280_read_interval" => $_POST['BME280_read_interval'],
    "BME280_i2c_address" => $_POST['BME280_i2c_address'],
    "use_DS18B20_sensor" => $_POST['use_DS18B20_sensor'],
    "DS18B20_read_interval" => $_POST['DS18B20_read_interval'],
    "use_DHT_sensor" => $_POST['use_DHT_sensor'],
    "DHT_read_interval" => $_POST['DHT_read_interval'],
    "DHT_type" => $_POST['DHT_type'],
    "DHT_pin" => $_POST['DHT_pin'],
);

$door_sensors = array();
$system_buttons = array();
$motion_sensors = array();
$led_indicators = array();

$count = 1;
foreach ($_POST as $key => $value) {
    if ($value['type'] == 'DoorSensor'){
        $varname = 'door_sensor_'.$count;
        $door_sensors[$varname]['gpio_pin'] = $value['gpio_pin'];
        $door_sensors[$varname]['hold_time'] = $value['hold_time'];
    $count++;
}
}

$count = 1;
foreach ($_POST as $key => $value) {
    if ($value['type'] == 'MotionSensor'){
        $varname = 'motion_sensor_'.$count;
        $motion_sensors[$varname]['gpio_pin'] = $value['gpio_pin'];
    $count++;
}
}

foreach ($_POST as $key => $value) {
    if ($value['type'] == 'ShutdownButton'){
        $system_buttons['shutdown_button'] = [];
        $system_buttons['shutdown_button']['gpio_pin'] = $value['gpio_pin'] ;
        $system_buttons['shutdown_button']['hold_time'] = $value['hold_time'];
    }
}

foreach ($_POST as $key => $value) {
    if ($value['type'] == 'door_led'){
        $led_indicators['door_led']['gpio_pin'] = $value['gpio_pin'];
}
    if ($value['type'] == 'motion_led'){
        $led_indicators['motion_led']['gpio_pin'] = $value['gpio_pin'];
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

$yaml = array(
    "setup" => $setup,
    "led_indicators" => $led_indicators,
    "door_sensors"   => $door_sensors,
    "motion_sensors" => $motion_sensors,
    "system_buttons" => $system_buttons,
    "zabbix_agent"   => $zabbix_agent,
);

$yaml = yaml_emit($yaml);
//var_dump($yaml);

yaml_emit_file ("/var/www/html/rpims2.yaml", $yaml);

?>

