<!DOCTYPE html>
<html lang="en">
<head>
<script src="jquery.min.js"></script>
<title>RPiMS</title>
<meta charset="utf-8"/>
<style>
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
  margin: 8px;
  font-size: 160%;
}
.sensors {
  background-color: darkslategray;
  color: white;
  padding: 8px;
  margin: 8px;
  font-size: 160%;
}
</style>
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
    <h3>BME280</h3>
    <ul style="list-style-type:none;">
        <li>Temperature: <span class="value" id="BME280_Temperature"></span><span class="value"> &#8451</span></li>
        <li>Humidity: <span class="value" id="BME280_Humidity"></span><span class="value"> %</span></li>
        <li>Pressure: <span class="value" id="BME280_Pressure"></span><span class="value"> hPa</span></li>
    </ul>
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
<?php  foreach ($rpimskeys as $key) { $sensor_type = 'DS18B20-'; if (strpos($key, $sensor_type) !== false) {?>
        <li><?php $key?> Temperature:	 <span class="value"><?=round($rpims[$key],2)?> &#8451</span></li>
<?php }}?>
    </ul>
</div>
<?php }?>

<?php if ($rpims["use_door_sensor"] == "True") {?>
<div class="sensors">
    <h3>Door sensors</h3>
    <ul style="list-style-type:none;">
    <?php foreach ($door_sensors as $key => $value) {
    echo "<li>"; echo $key; echo "<span class='value'>: "; echo $rpims["$key"]; echo " </span></li>";
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
    echo "<li>"; echo $key; echo "<span class='value'>: "; echo $rpims["$key"]; echo " </span></li>";
}
?>
    </ul>
</div>
<?php }?>


<?php if ($rpims["use_weather_station"] == "True") {?>
<div class="sensors">
    <h3>Weather Meter</h3>
    <ul style="list-style-type:none;">
        <li>Wind speed: <span class="value" id="wind_speed"></span><span class="value"> km/h</span></li>
        <li>Average Wind speed: <span class="value" id="average_wind_speed"></span><span class="value"> km/h</span></li>
        <li>Average Wind speed From the Past 24 Hours: <span class="value" id="daily_average_wind_speed"></span><span class="value"> km/h</span></li>
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
    <li>rtsp://<span><?=$rpims["hostip"]?>:8554/</span></li>
    </ul>
</div>
<?php }?>

<div class="footer"></div>
</div>
<div></div>
<script type="text/javascript">
setInterval(function() {
$.getJSON("rpims.php", function(data) {
$("#average_wind_direction").html(data['average_wind_direction']);
$("#daily_average_wind_speed").html(data['daily_average_wind_speed']);
$("#average_wind_speed").html(data['average_wind_speed']);
$("#wind_speed").html(data['wind_speed']);
$("#wind_gust").html(data['wind_gust']);
$("#daily_wind_gust").html(data['daily_wind_gust']);
$("#daily_rainfall").html(data['daily_rainfall']);
$("#CPU_Temperature").html(data['CPU_Temperature']);
$("#hostip").html(data['hostip']);
$("#hostname").html(data['hostname']);
$("#location").html(data['location']);
$("#BME280_Temperature").html(data['BME280_Temperature']);
$("#BME280_Humidity").html(data['BME280_Humidity']);
$("#BME280_Pressure").html(data['BME280_Pressure']);
$("#DHT_Temperature").html(data['DHT_Temperature']);
$("#DHT_Humidity").html(data['DHT_Humidity']);
});
}, 100);
</script>

</body>
</html>
