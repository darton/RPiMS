<!DOCTYPE html>
<html lang="en">
<head>
<title>RPiMS</title>
<meta charset="utf-8"/>
<style>

.gauge {
  width: 100%;
  max-width: 250px;
  font-family: "Roboto", sans-serif;
  font-size: 30px;
  color: #004033;
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
  background: #ffffff;
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
  margin: 4px;
  font-size: 120%;
}
.sensors {
  background-color: darkslategray;
  color: white;
  padding: 8px;
  margin: 4px;
  font-size: 120%;
}
</style>
<script src="jquery.min.js"></script>
<script type="text/javascript" src="index.js"></script>
</head>
<body>

<div class="rpimsbg">
<div class="header"></div>
<div class="rpims">
    <ul style="list-style-type:none;">
    <li>Hostname: <span class="value" id="hostname"></span></li>
    <li>Location: <span class="value" id="location"></span></li>
<?php if ($rpims["use_CPU_sensor"] == "True") {?>
    <li>CPU Temperature: <span class="value" id="CPU_Temperature"></span><span class="value">&#8451</span></li>
<?php }?>
    </ul>
</div>

<?php if ($rpims["use_BME280_sensor"] == "True") {?>
<div class="sensors">

<div class="gauge" id="g1">
  <div class="gauge__body">
    <div class="gauge__fill"></div>
    <div class="gauge__cover"></div>
  </div>
</div>
<h5>Air Temperature</h5>

<div class="gauge" id="g2">
  <div class="gauge__body">
    <div class="gauge__fill"></div>
    <div class="gauge__cover"></div>
  </div>
</div>
<h5>Air Humidity</h5>

<div class="gauge" id="g3">
  <div class="gauge__body">
    <div class="gauge__fill"></div>
    <div class="gauge__cover"></div>
  </div>
</div>
<h5>Air Pressure</h5>
</div>

<?php }?>

<?php if ($rpims["use_DHT_sensor"] == "True") {?>
<div class="sensors">
    <h3><?=$rpims["DHT_type"]?></h3>
    <ul style="list-style-type:none;">
        <li>Temperature: <span class="value" id="DHT_Temperature"></span><span class="value"> &#8451</span></li>
        <li>Humidity: <span class="value" id="DHT_Humidity"></span><span class="value"> %</span></li>
    </ul>
</div>
<?php }?>

<?php if ($rpims["use_DS18B20_sensor"] == "True") {?>
<div class="sensors">
    <h3>DS18B20</h3>
    <ul style="list-style-type:none;">
<?php  foreach ($DS18B20_sensors as $key => $value) {;
	echo "<li>"; echo $value; echo ": <span class='value' id='$value'></span>"; echo "<span class='value'> &#8451</span></li>";
}
?>
    </ul>
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
<div class="sensors"
<h2>Weather Station</h2>

<div class="gauge" id="g4" style="text-align:center">
  <div class="gauge__body">
    <div class="gauge__fill"></div>
    <div class="gauge__cover"></div>
  </div>
</div>
<h5>Wind Speed</h5>
    <ul style="list-style-type:none;">
        <li>Wind speed: <span class="value" id="wind_speed"></span><span class="value"> km/h</span></li>
        <li>Average Wind speed: <span class="value" id="average_wind_speed"></span><span class="value"> km/h</span></li>
        <li>Average Wind speed From the Past 24h: <span class="value" id="daily_average_wind_speed"></span><span class="value"> km/h</span></li>
        <li>Wind gust: <span class="value" id="wind_gust"></span><span class="value"> km/h</span></li>
        <li>Peak Wind Gust From the Past 24 Hours: <span class="value" id="daily_wind_gust"></span><span class="value"> km/h</span></li>
        <li>Wind direction: <span class="value" id="average_wind_direction"></span><span class="value"> &#176 </span></li>
        <li>Rainfall From the Past 24 Hours: <span class="value" id="daily_rainfall"></span><span class="value"> mm</span></li>
    </ul>
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
