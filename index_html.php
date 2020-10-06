<!DOCTYPE html>
<html lang="en">
<head>
<title>RPiMS</title>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>


/* Dropdown Button */
.dropbtn {
  background-color: #3498DB;
  color: white;
  padding: 16px;
  font-size: 16px;
  border: none;
  cursor: pointer;
}

/* Dropdown button on hover & focus */
.dropbtn:hover, .dropbtn:focus {
  background-color: #2980B9;
}

/* The container <div> - needed to position the dropdown content */
.dropdown {
  position: relative;
  display: inline-block;
}

/* Dropdown Content (Hidden by Default) */
.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f1f1f1;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}

/* Links inside the dropdown */
.dropdown-content a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

/* Change color of dropdown links on hover */
.dropdown-content a:hover {background-color: #ddd}

/* Show the dropdown menu (use JS to add this class to the .dropdown-content container when the user clicks on the dropdown button) */
.show {display:block;}


td {
  text-align: left;
}

.gauge {
  width: 100%;
  max-width: 250px;
  font-family: "Roboto", sans-serif;
  font-size: 32px;
  #color: #004033;
}

.gauge__body {
  width: 100%;
  height: 0;
  padding-bottom: 50%;
  background: #b4c0be;
  position: relative;
  border-top-left-radius: 100% 200%;
  border-top-right-radius: 100% 200%;
  overflow: hidden;
}

.gauge__fill {
  position: absolute;
  top: 100%;
  left: 0;
  width: inherit;
  height: 100%;
  background: #009578;
  transform-origin: center top;
  transform: rotate(0.25turn);
  transition: transform 0.2s ease-out;
}

.gauge__cover {
  width: 75%;
  height: 150%;
  #background: #ffffff;
  background: darkslategray;
  border-radius: 50%;
  position: absolute;
  top: 25%;
  left: 50%;
  transform: translateX(-50%);

  /* Text */
  display: flex;
  align-items: center;
  justify-content: center;
  padding-bottom: 25%;
  box-sizing: border-box;
}

span.value {
  font-size: 100%;
  color: yellow;
}
.rpimsbg
{
  background-color: steelblue;
  #background-color: slategray;
}
.header
{
  padding: 1px;
  margin: 0px;
}
.footer
{
  padding: 1px;
  margin: 0px;
}

.rpims {
 #background-color: #6159DB;
  background-color: darkslateblue;
  color: white;
  padding: 8px;
  margin: 10px;
  font-size: 120%;
}
.sensors {
  background-color: darkslategray;
  #background-color: white;
  color: white;
  padding: 8px;
  margin: 10px;
  font-size: 100%;
  text-align: center;
}

.table {
  background-color: darkslategray;
  color: white;
  padding: 0px;
  margin: 0px;
  font-size: 130%;
  text-align: left;
}

</style>
<script src="jquery.min.js"></script>
<script type="text/javascript" src="index.js"></script>
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

<div>
    <ul style="list-style-type:none;">
    <li>Hostname: <span class="value" id="hostname"></span></li>
    <li>Location: <span class="value" id="location"></span></li>
<?php if ($rpims["use_CPU_sensor"] == "True") {?>
    <li>CPU Temperature: <span class="value" id="CPU_Temperature"></span><span class="value">&#8451</span></li>
<?php }?>
    </ul>
</div>

</div>



<?php if ($rpims["use_BME280_sensor"] == "True") {?>
<div class="sensors">
    <h3>BME280 Sensor</h3>
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

<?php if ($rpims["use_DHT_sensor"] == "True") {?>
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


<?php if ($rpims["use_DS18B20_sensor"] == "True") {?>
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
<?php }?>
-->

<?php if ($rpims["use_DS18B20_sensor"] == "True") {?>
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


<?php if ($rpims["use_door_sensor"] == "True") {?>
<div class="sensors">
    <h3>Door sensors</h3>
    <ul style="list-style-type:none;">
    <?php foreach ($door_sensors as $key => $value) {
    echo "<li>"; echo $value; echo ": <span class='value' id='$value'></span></li>";
}
?>
    </ul>
</div>
<?php }?>

<?php if ($rpims["use_motion_sensor"] == "True") {?>
<div class="sensors">
    <h3>Motion sensors</h3>
    <ul style="list-style-type:none;">
<?php foreach ($motion_sensors as $key => $value) {
    echo "<li>"; echo $value; echo ": <span class='value' id='$value'></span></li>";
}
?>
    </ul>
</div>
<?php }?>

<?php if ($rpims["use_weather_station"] == "True") {?>
<div class="sensors">

<div style="width: 100%; display: table;">
<div style="display: table-row">
<div class="gauge" id="g4" style="width: 300px; display: table-cell">
  <div class="gauge__body">
    <div class="gauge__fill"></div>
    <div class="gauge__cover"></div>
  </div>
<div class="sensors">Wind Speed</div>
</div>

<div class="gauge" id="g5" style="width: 300px; display: table-cell">
  <div class="gauge__body">
    <div class="gauge__fill"></div>
    <div class="gauge__cover"></div>
  </div>
<div class="sensors">Wind Gust</div>
</div>

<div class="gauge" id="g6" style="width: 300px; display: table-cell">
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

<?php if ($rpims["use_picamera"] == "True") {?>
<div class="sensors">
    <h3>Video Stream Url</h3>
    <ul style="list-style-type:none;">
    <li>rtsp://<span id="hostip"></span><span>:8554/</span></li>
    </ul>
</div>
<?php }?>

<div class="footer"></div>
</div>
</body>
</html>
