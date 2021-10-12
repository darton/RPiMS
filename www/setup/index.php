<?php

$redis = new Redis();
$redis->connect('127.0.0.1', 6379);
$DS18B20_sensors_detected = $redis->smembers('DS18B20_sensors');


$obj = $redis-> get('sensors');
$sensors = json_decode($obj, true);

foreach ($DS18B20_sensors_detected as $key => $value){
	    $DS18B20_sensors[$value] = $sensors['ONE_WIRE']['DS18B20']['addresses'][$value]['name'];
	}

$rpims = yaml_parse_file ("/var/www/html/conf/rpims.yaml");
$location = $rpims['zabbix_agent']['location'];
$hostname = $rpims['zabbix_agent']['hostname'];
$zabbix_server = $rpims['zabbix_agent']['zabbix_server'];
$zabbix_server_active = $rpims['zabbix_agent']['zabbix_server_active'];
$TLSPSKIdentity = $rpims['zabbix_agent']['TLSPSKIdentity'];
$TLSPSK = $rpims['zabbix_agent']['TLSPSK'];
$Timeout = $rpims['zabbix_agent']['Timeout'];

$verbose = filter_var($rpims['setup']['verbose'], FILTER_VALIDATE_BOOLEAN);
$show_sys_info = filter_var($rpims['setup']['show_sys_info'], FILTER_VALIDATE_BOOLEAN);
$use_zabbix_sender = filter_var($rpims['setup']['use_zabbix_sender'], FILTER_VALIDATE_BOOLEAN);
$use_picamera = filter_var($rpims['setup']['use_picamera'], FILTER_VALIDATE_BOOLEAN);
$use_picamera_recording = filter_var($rpims['setup']['use_picamera_recording'], FILTER_VALIDATE_BOOLEAN);
$use_door_sensor = filter_var($rpims['setup']['use_door_sensor'], FILTER_VALIDATE_BOOLEAN);
$use_motion_sensor = filter_var($rpims['setup']['use_motion_sensor'], FILTER_VALIDATE_BOOLEAN);
//$use_system_buttons = filter_var($rpims['setup']['use_system_buttons'], FILTER_VALIDATE_BOOLEAN);
//$use_led_indicators = filter_var($rpims['setup']['use_led_indicators'], FILTER_VALIDATE_BOOLEAN);
$use_serial_display = filter_var($rpims['setup']['use_serial_display'], FILTER_VALIDATE_BOOLEAN);
$use_cpu_sensor = filter_var($rpims['setup']['use_cpu_sensor'], FILTER_VALIDATE_BOOLEAN);
$use_bme280_sensor = filter_var($rpims['setup']['use_bme280_sensor'], FILTER_VALIDATE_BOOLEAN);
$use_ds18b20_sensor = filter_var($rpims['setup']['use_ds18b20_sensor'], FILTER_VALIDATE_BOOLEAN);
$use_dht_sensor = filter_var($rpims['setup']['use_dht_sensor'], FILTER_VALIDATE_BOOLEAN);
$use_weather_station = filter_var($rpims['setup']['use_weather_station'], FILTER_VALIDATE_BOOLEAN);

$serial_display_refresh_rate = $rpims['setup']['serial_display_refresh_rate'];
$serial_display_type = $rpims['setup']['serial_display_type'];
$serial_type = $rpims['setup']['serial_type'];
$serial_display_rotate = $rpims['setup']['serial_display_rotate'];

$CPUtemp_read_interval = $rpims['sensors']['CPU']['temp']['read_interval'];

$picamera_rotation = $rpims['sensors']['PICAMERA']['rotation'];
$picamera_mode = $rpims['sensors']['PICAMERA']['mode'];
$picamera_fps = $rpims['sensors']['PICAMERA']['fps'];

$id1_BME280_use = $rpims['sensors']['BME280']['id1']['use'];
$id1_BME280_name = $rpims['sensors']['BME280']['id1']['name'];
$id1_BME280_read_interval = $rpims['sensors']['BME280']['id1']['read_interval'];
$id1_BME280_interface = $rpims['sensors']['BME280']['id1']['interface'];
$id1_BME280_i2c_address = $rpims['sensors']['BME280']['id1']['i2c_address'];
//$id1_BME280_serial_port = $rpims['sensors']['BME280']['id1']['serial_port'];

$id2_BME280_use = $rpims['sensors']['BME280']['id2']['use'];
$id2_BME280_name = $rpims['sensors']['BME280']['id2']['name'];
$id2_BME280_read_interval = $rpims['sensors']['BME280']['id2']['read_interval'];
$id2_BME280_interface = $rpims['sensors']['BME280']['id2']['interface'];
$id2_BME280_serial_port = $rpims['sensors']['BME280']['id2']['serial_port'];

$id3_BME280_use = $rpims['sensors']['BME280']['id3']['use'];
$id3_BME280_name = $rpims['sensors']['BME280']['id3']['name'];
$id3_BME280_read_interval = $rpims['sensors']['BME280']['id3']['read_interval'];
$id3_BME280_interface = $rpims['sensors']['BME280']['id3']['interface'];
$id3_BME280_serial_port = $rpims['sensors']['BME280']['id3']['serial_port'];

$DS18B20_read_interval = $rpims['sensors']['ONE_WIRE']['DS18B20']['read_interval'];

$DHT_read_interval = $rpims['sensors']['DHT']['read_interval'];
$DHT_type = $rpims['sensors']['DHT']['type'];
$DHT_pin = $rpims['sensors']['DHT']['pin'];
$DHT_name = $rpims['sensors']['DHT']['name'];

$windspeed_use = $rpims['sensors']['WEATHER']['WIND']['SPEED']['use'];
$windspeed_sensor_pin = $rpims['sensors']['WEATHER']['WIND']['SPEED']['sensor_pin'];
$windspeed_acquisition_time = $rpims['sensors']['WEATHER']['WIND']['SPEED']['acquisition_time'];
$windspeed_agregation_time = $rpims['sensors']['WEATHER']['WIND']['SPEED']['agregation_time'];

$winddirection_use = $rpims['sensors']['WEATHER']['WIND']['DIRECTION']['use'];
$winddirection_acquisition_time = $rpims['sensors']['WEATHER']['WIND']['DIRECTION']['acquisition_time'];
$winddirection_adc_type = $rpims['sensors']['WEATHER']['WIND']['DIRECTION']['adc_type'];
$winddirection_adc_input = $rpims['sensors']['WEATHER']['WIND']['DIRECTION']['adc_input'];
$reference_voltage_adc_input = $rpims['sensors']['WEATHER']['WIND']['DIRECTION']['reference_voltage_adc_input'];

$rainfall_use = $rpims['sensors']['WEATHER']['RAINFALL']['use'];
$rainfall_sensor_pin = $rpims['sensors']['WEATHER']['RAINFALL']['sensor_pin'];
$rainfall_acquisition_time = $rpims['sensors']['WEATHER']['RAINFALL']['acquisition_time'];
$rainfall_agregation_time = $rpims['sensors']['WEATHER']['RAINFALL']['agregation_time'];

$GPIO = $rpims['gpio'];

include 'setup_html.php';
