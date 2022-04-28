<?php
$redis = new Redis();
$redis->connect('127.0.0.1', 6379);

$rpimskeys = $redis->keys('*');

foreach ($rpimskeys as $key) {
    $value = $redis->get($key);
    $rpims[$key] = $value;
}

$obj = $redis-> get('config');
$config = json_decode($obj, true);

$obj = $redis-> get('sensors');
$sensors = json_decode($obj, true);

$rpims_api = array();

if (empty($_GET) || $_GET['all'] == 'show') {
$showAll = true;
}

if ($_GET['settings'] == "show" || $showAll == true){
    $obj = $redis-> get('config');
    $rpims_api["settings"] = json_decode($obj, true);
}
if ($_GET['system'] == "show" || $showAll == true){
    $obj = $redis-> get('zabbix_agent');
    $zabbix_agent = json_decode($obj, true);
    $_system = $redis->hgetall("SYSTEM");

    $system["hostip"] = $_system['hostip'];
    $system["memused"] = $_system['memused'];
    $system["fsused"] = $_system['fsused'];
    $system["uptime"] = $_system['uptime'];
    $system["hostname"] = $zabbix_agent["hostname"];
    $system["location"] = $zabbix_agent["location"];

    $rpims_api["system"] = $system;
}
if ($_GET['cpu'] == "show" || $_GET['sensors'] == "show" || $showAll == true){
    if ($config["use_cpu_sensor"] == true) {
        $rpims_api["sensors"]["cpu"]["temperature"] = $rpims["CPU_Temperature"];
    }
}
if ($_GET['picamera'] == "show" || $_GET['sensors'] == "show" || $showAll == true){
    if ($config["use_picamera"] == show) {
        $rpims_api["sensors"]["picamera"]["rotation"] = $sensors["PICAMERA"]["rotation"];
        $rpims_api["sensors"]["picamera"]["mode"] = $sensors["PICAMERA"]["mode"];
        $rpims_api["sensors"]["picamera"]["fps"] = $sensors["PICAMERA"]["fps"];
    }
}
if ($_GET['bme280'] == "show" || $_GET['sensors'] == "show" || $showAll == true){
    if ($config["use_bme280_sensor"] == true) {
        foreach ($sensors['BME280'] as $key => $value) {
            $id = $sensors['BME280'][$key]["id"];
            $bme280id = $id."_BME280";
            $_bme280 = $redis->hgetall($bme280id);
            if ($sensors["BME280"][$id]["use"] == true) {
                $rpims_api["sensors"]["bme280"][$id]["name"] = $sensors["BME280"][$id]["name"];
		$rpims_api["sensors"]["bme280"][$id]["temperature"] = $_bme280['Temperature'];
		$rpims_api["sensors"]["bme280"][$id]["humidity"] = $_bme280['Humidity'];
		$rpims_api["sensors"]["bme280"][$id]["pressure"] = $_bme280['Pressure'];
            }
	}
        //$BME280_sensors = $redis->smembers('BME280_sensors');
        //foreach ($BME280_sensors as $key => $value) {
        //    $bme280id = $value."_BME280";
	//    $rpims_api["sensors"]["bme280"][$value]["temperature"] = $redis->hget($bme280id,"Temperature");
	//    $rpims_api["sensors"]["bme280"][$value]["humidity"] = $redis->hget($bme280id,"Humidity");
	//    $rpims_api["sensors"]["bme280"][$value]["pressure"] = $redis->hget($bme280id,"Pressure");
	//}
    }
}
if ($_GET['one_wire'] == "show" || $_GET['sensors'] == "show" || $showAll == true){
    if ($config["use_ds18b20_sensor"] == true) {
        $DS18B20_sensors = $redis->smembers('DS18B20_sensors');
        foreach ($DS18B20_sensors as $key => $value) {
            $ds18b20_name = $value."_name";
            $rpims_api["sensors"]["one_wire"]["ds18b20"]["$value"]["temperature"] = $rpims[$value];
            $rpims_api["sensors"]["one_wire"]["ds18b20"]["$value"]["name"] = $sensors["ONE_WIRE"]["DS18B20"]["addresses"]["$value"]["name"];
        }
    }
}
if ($_GET['dht'] == "show" || $_GET['sensors'] == "show" || $showAll == true){
    if ($config["use_dht_sensor"] == true) {
        $rpims_api["sensors"]["dht"]["temperature"] = $rpims["DHT_Temperature"];
        $rpims_api["sensors"]["dht"]["humidity"] = $rpims["DHT_Humidity"];
    }
}
if ($_GET['weather_station'] == "show" || $_GET['sensors'] == "show" || $showAll == true){
    if ($config["use_weather_station"] == true) {
        $rpims_api["weather_station"]["wind_speed"] = $rpims["wind_speed"];
        $rpims_api["weather_station"]["average_wind_speed"] = $rpims["average_wind_speed"];
        $rpims_api["weather_station"]["daily_average_wind_speed"] = $rpims["daily_average_wind_speed"];
        $rpims_api["weather_station"]["wind_gust"] = $rpims["wind_gust"];
        $rpims_api["weather_station"]["daily_wind_gust"] = $rpims["daily_wind_gust"];
        $rpims_api["weather_station"]["average_wind_direction"] = $rpims["average_wind_direction"];
        $rpims_api["weather_station"]["daily_rainfall"] = $rpims["daily_rainfall"];
    }
}
if ($_GET['gpio'] == "show" || $_GET['sensors'] == "show" || $showAll == true){
    $obj = $redis-> get('gpio');
    $gpio = json_decode($obj, true);
    $_gpio = $redis->hgetall('GPIO');
    if ($config["use_door_sensor"] == true) {
        foreach ($gpio as $key=> $value) {
            if ($gpio[$key]["type"] == "DoorSensor" ) {
                $door_sensors[$key] = ($gpio[$key]);
            }
        }
        foreach ($door_sensors as $key => $value){
            $rpims_api["sensors"]["door_sensors"]["$key"] = $_gpio[$key];
        }
    }
    if ($config["use_motion_sensor"] == true){
        foreach ($gpio as $key=> $value) {
            if ($gpio[$key]["type"] == "MotionSensor" ) {
                $motion_sensors[$key] = ($gpio[$key]);
            }
        }
        foreach ($motion_sensors as $key => $value) {
            $rpims_api["sensors"]["motion_sensors"]["$key"] = $_gpio[$key];
        }
    }
}

header("content-type: application/json");
header("Cache-Control: no-cache");
echo json_encode($rpims_api);
