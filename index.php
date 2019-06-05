<!DOCTYPE html>
<html>
<meta http-equiv="refresh" content="30"/>
<body>

<?php
   
   $redis = new Redis();
   $redis->connect('127.0.0.1', 6379);
   
   $temperature = $redis->get('Temperature');
   $humidity = $redis->get('Humidity');
   $door1 = $redis->get('Door1');
   $door2 = $redis->get('Door2');
   $door3 = $redis->get('Door3');
   $door4 = $redis->get('Door4');

   print "<p>Temperature: " . number_format($temperature,2) ." °C</p>";
   print "<p>Humidity: " . number_format($humidity,2) ." %</p>";

   print "<p>Door1: " . $door1 ."</p>";
   print "<p>Door2: " . $door2 ."</p>";
   print "<p>Door3: " . $door3 ."</p>";
   print "<p>Door4: " . $door4 ."</p>";

?>

</body>
</html>
