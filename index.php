<!DOCTYPE html>
<html>
<meta http-equiv="refresh" content="30"/>
<body>

<?php
    $hostname = gethostname();
    
    $redis = new Redis();
    $redis->connect('127.0.0.1', 6379);

    $location = $redis->get('Location');
    $temperature = $redis->get('Temperature');
    $humidity = $redis->get('Humidity');
    $sensor1 = $redis->get('door_sensor_1');
    $sensor2 = $redis->get('door_sensor_2');
    $sensor3 = $redis->get('door_sensor_3');
    $sensor4 = $redis->get('door_sensor_4');

    print "<p>Lokalizacja: " . $location ."</p>";
    print "<p>Hostname: " . $hostname ."</p><br>";

    print "<p style='color:blue;'>Temperature: " . number_format($temperature,1) ." °C</p>";
    print "<p style='color:blue;'>Humidity: " . number_format($humidity,1) ." %</p><br>";

    print "<p style='color:red;'>Door1: " . $door1 ."</p>";
    print "<p style='color:red;'>Door2: " . $door2 ."</p>";
    print "<p style='color:red;'>Door3: " . $door3 ."</p>";
    print "<p style='color:red;'>Door4: " . $door4 ."</p>";

?>

</body>
</html>
