<!DOCTYPE html>
<html>
<meta http-equiv="refresh" content="30"/>
<body>

<?php

    $redis = new Redis();
    $redis->connect('127.0.0.1', 6379);

    $location = $redis->get('Location');
    $hostname = gethostname();


    $temperature = $redis->get('Temperature');
    $humidity = $redis->get('Humidity');

    $door1 = $redis->get('Door1');
    $door2 = $redis->get('Door2');
    $door3 = $redis->get('Door3');
    $door4 = $redis->get('Door4');

    print "<p>Lokalizacja: " . $location ."</p>";
    print "<p>Hostname: " . $hostname ."</p><br>";

    print "<p style='color:blue;'>Temperature: " . number_format($temperature,2) ." °C</p>";
    print "<p style='color:blue;'>Humidity: " . number_format($humidity,2) ." %</p><br>";

    print "<p style='color:red;'>Door1: " . $door1 ."</p>";
    print "<p style='color:red;'>Door2: " . $door2 ."</p>";
    print "<p style='color:red;'>Door3: " . $door3 ."</p>";
    print "<p style='color:red;'>Door4: " . $door4 ."</p>";

?>

</body>
</html>
