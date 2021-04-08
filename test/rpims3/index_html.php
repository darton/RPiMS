<!DOCTYPE html>
<html lang="en">
<head>
<title>RPiMS</title>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="index.css">
<script src="jquery.min.js"></script>
<script src="index.js" defer></script>
</head>
<body>

<div class="rpimsbg">
<div class="header"></div>


<div class="rpims">

<div class="dropdown">
  <button onclick="myFunction()" class="dropbtn">Config</button>
  <div id="myDropdown" class="dropdown-content">
    <a href="/setup/">Setup</a>
    <a href="/rpims.php">API</a>
  </div>
</div>
</div>



<?php if ($config["show_sys_info"] == "True") {?>
<div class="sensors">
    <ul style="list-style-type:none;">
    <li>Hostname: <span class="value" id="hostname"></span></li>
    <li>Location: <span class="value" id="location"></span></li>
<?php if ($config["use_CPU_sensor"] == "True") {?>
    <li>CPU Temperature: <span class="value" id="CPU_Temperature"> </span><span class="value" id="CPU_Temperature_unit"></span></li>
<?php }?>
    </ul>
</div>
<?php }?>



<?php if ($config["use_BME280_sensor"] == "True") {?>
<div class="sensors">
    <h3>Internal BME280 Sensor</h3>
<div style="width: 100%; display: table;">
<div style="display: table-row">

<div class="gauge" id="g1"  style="width: 33%;  display: table-cell";>
  <div class="gauge__body">
    <div class="gauge__fill"></div>
    <div class="gauge__cover"></div>
  </div>
<div class="sensors">Temp</div>
</div>

<div class="gauge" id="g2"  style="width: 33%; display: table-cell";>
 <div class="gauge__body">
    <div class="gauge__fill"></div>
    <div class="gauge__cover"></div>
  </div>
<div class="sensors">Hum</div>
</div>

<div class="gauge" id="g3"  style="width: 33%; display: table-cell";>
  <div class="gauge__body">
    <div class="gauge__fill"></div>
    <div class="gauge__cover"></div>
  </div>
<div class="sensors">Pres</div>
</div>

</div>
</div>
</div>
<?php }?>

<?php if ($config["use_DHT_sensor"] == "True") {?>
<div class="sensors">
    <h3>DHT Sensor</h3>
<div style="width: 100%; display: table;">
<div style="display: table-row">

<div class="gauge" id="g11"  style="width: 50%;  display: table-cell";>
  <div class="gauge__body">
    <div class="gauge__fill"></div>
    <div class="gauge__cover"></div>
  </div>
<div class="sensors">Temp</div>
</div>

<div class="gauge" id="g12"  style="width: 50%; display: table-cell";>
 <div class="gauge__body">
    <div class="gauge__fill"></div>
    <div class="gauge__cover"></div>
  </div>
<div class="sensors">Hum</div>
</div>

</div>
</div>
</div>
<?php }?>


<?php if ($config["use_DS18B20_sensor"] == "True") {?>
<!--
<div class="sensors">
    <h3>DS18B20 Sensors</h3>
<ul style="list-style-type:none;">
<?php foreach ($DS18B20_sensors as $key => $value) {
    echo "<li>".$value.": <span class='value' id='$value'></span><span class='value'>&#8451</span></li></br>";
}
?>
</ul>
</div>
-->
<?php }?>

<?php if ($config["use_DS18B20_sensor"] == "True") {?>
<div class="sensors">
    <h3>DS18B20 Sensors</h3>
<div style="width: 100%; display: table;">
<div style="display: table-row">
<?php  foreach ($DS18B20_sensors as $key => $value) {
    $item = "DS18B20_".$value;
    echo "<div class='gauge' id='$item'  style='width: 33%;  display: table-cell';>";
    echo "  <div class='gauge__body'>";
    echo "  <div class='gauge__fill'></div>";
    echo "<div class='gauge__cover'></div>";
    echo "</div>";
    echo "<div class='sensors'>$value</div>";
    echo "</div>";
    }
?>
</div>
</div>
</div>
<?php }?>


<?php if ($config["use_BME280_sensor"] == "True") {?>
<div class="sensors">
    <h3>BME280</h3>
    <div style="width: 100%; display: table;">
<?php
    foreach ($sensors['BME280'] as $key => $value) 
    {
	if ($value['use'] == "true")
	{
	    $t = $key."_BME280_Temperature";
	    $h = $key."_BME280_Humidity";
	    $p = $key."_BME280_Pressure";

	    echo "<div style='display: table-row';>";

	    echo " <div class='gauge' id='$t' style='width: 33%;  display: table-cell';>";
	    echo "    <div class='gauge__body'>";
	    echo "        <div class='gauge__fill'></div>";
	    echo "        <div class='gauge__cover'></div>";
	    echo "    </div>";
	    echo "    <div class='sensors'>Temp</div>";
	    echo " </div>";

	    echo " <div class='gauge' id='$h' style='width: 33%;  display: table-cell';>";
	    echo "    <div class='gauge__body'>";
	    echo "        <div class='gauge__fill'></div>";
	    echo "        <div class='gauge__cover'></div>";
	    echo "    </div>";
	    echo "    <div class='sensors'>Hum</div>";
	    echo " </div>";

	    echo " <div class='gauge' id='$p' style='width: 33%;  display: table-cell';>";
	    echo "    <div class='gauge__body'>";
	    echo "        <div class='gauge__fill'></div>";
	    echo "        <div class='gauge__cover'></div>";
	    echo "    </div>";
	    echo "    <div class='sensors'>Pres</div>";
	    echo " </div>";

	    echo "</div>";
	}
    }
?>
    </div>
</div>
<?php }?>



<?php if ($config["use_door_sensor"] == "True") {?>
<div class="sensors">
    <h2>Door sensors</h2>
    <table class="center">
    <?php foreach ($door_sensors as $key => $value) {
    echo "<tr><td>"; echo $value["name"]; echo "</td><td>: <span class='value' id='$key'></span></td></tr>";
}
?>
    </table>
</div>
<?php }?>

<?php if ($config["use_motion_sensor"] == "True") {?>
<div class="sensors">
    <h2>Motion sensors</h2>
    <table class="center">
    <?php foreach ($motion_sensors as $key => $value) {
    echo "<tr><td>"; echo $value["name"]; echo "</td><td>: <span class='value' id='$key'></span></td></tr>";
}
?>
    </table>
</div>
<?php }?>

<?php if ($config["use_weather_station"] == "True") {?>
<div class="sensors">

<div style="width: 100%; display: table;">
<div style="display: table-row">

<div class="gauge" id="g4" style="width: 33%; display: table-cell">
  <div class="gauge__body">
    <div class="gauge__fill"></div>
    <div class="gauge__cover"></div>
  </div>
<div class="sensors">Wind Speed</div>
</div>

<div class="gauge" id="g5" style="width: 33%; display: table-cell">
  <div class="gauge__body">
    <div class="gauge__fill"></div>
    <div class="gauge__cover"></div>
  </div>
<div class="sensors">Wind Gust</div>
</div>

<div class="gauge" id="g6" style="width: 33%; display: table-cell">
  <div class="gauge__body">
    <div class="gauge__fill"></div>
    <div class="gauge__cover"></div>
  </div>
<div class="sensors">Wind Gust 24h</div>
</div>

</div>
</div>

<table class="table">
<tr><td>Wind speed: </td><td><span class="value" id="wind_speed"></span><span class="value"> km/h</span></td></tr>
<tr><td>Average Wind speed: </td><td><span class="value" id="average_wind_speed"></span><span class="value"> km/h</span></td></tr>
<tr><td>Average Wind speed (Past 24h): </td><td><span class="value" id="daily_average_wind_speed"></span><span class="value"> km/h</span></td></tr>
<tr><td>Wind gust: </td><td><span class="value" id="wind_gust"></span><span class="value"> km/h</span></td></tr>
<tr><td>Peak Wind Gust (Past 24h): </td><td><span class="value" id="daily_wind_gust"></span><span class="value"> km/h</span></td></tr>
<tr><td>Wind direction: </td><td><span class="value" id="average_wind_direction"></span><span class="value"> &#176 </span></td></tr>
<tr><td>Rainfall (Past 24h): </td><td><span class="value" id="daily_rainfall"></span><span class="value"> mm</span></td></tr>
</table>
</div>
<?php }?>

<?php if ($config["use_picamera"] == "True") {?>
<div class="sensors">
    <div>
         <a href="/streaming/stream.html">Camera Stream Url</a>
    </div>
    <div>
         <iframe width="655" height="500"
            src="/streaming/stream.html">
         </iframe>
    </div>
</div>
<?php }?>

<div class="footer"></div>
</div>
</body>
</html>
