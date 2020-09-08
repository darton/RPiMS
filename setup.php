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

$rpims = yaml_parse_file ("/var/www/html/conf/rpims.yaml");
$location = $rpims['zabbix_agent']['location'];
$hostname = $rpims['zabbix_agent']['hostname'];
$zabbix_server = $rpims['zabbix_agent']['zabbix_server'];
$zabbix_server_active = $rpims['zabbix_agent']['zabbix_server_active'];
$TLSPSKIdentity = $rpims['zabbix_agent']['TLSPSKIdentity'];
$TLSPSK = $rpims['zabbix_agent']['TLSPSK'];
$Timeout = $rpims['zabbix_agent']['Timeout'];

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
$serial_display_rotate = $rpims['setup']['serial_display_rotate'];

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

include 'setup_html.php';
?>
