<!DOCTYPE html>
<html lang="en">
	<meta charset="utf-8"/>
        <meta name="description" content="RPiMS - Raspberry Pi Monitoring System">
        <meta name="keywords" content="Raspberry Pi, Monitoring System, Sensors">
        <meta name="author" content="Dariusz Kowalczyk">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>RPiMS API</title>
	<link rel="stylesheet" href="/css/w3.css">
	<link rel="stylesheet" href="/css/w3-colors-2020.css">
	<body>
		<div class="w3-container w3-2020-brilliant-white">
			<div class="w3-panel w3-2020-ultramarine-green">
				<h2 id="rpims-api"> RPiMS API</h2>
			</div>
			<div class="w3-container">
			<p>To download all current data in JSON format, use the following address:</p>
			</div>
			<div class="w3-container w3-light-grey">
				<p><a href="/api/data/?all=show">http://<?=$server_ip?>/api/data/?all=show</a></p>
			</div>
			<div class="w3-container">
			    <p>In order to obtain data only for a selected sensor or a group of sensors, 
			    the address should be filled in with a parameter, e.g .:</p>
			</div>
			<div class="w3-container w3-light-grey w3-round">
				<p><a href="/api/data?sensors=show">http://<?=$server_ip?>/api/data/?sensors=show</a></p>
			</div>
			<div class="w3-container">
				<p>CPU sensor</p>
			</div>
			<div class="w3-container w3-light-grey">
				<p><a href="/api/data/?cpu=show">http://<?=$server_ip?>/api/data/?cpu=show</a></p>
			</div>
			<div class="w3-container">
				<p>BME280 sensor</p>
			</div>
			<div class="w3-container w3-light-grey">
				<p><a href="/api/data/?bme280=show">http://<?=$server_ip?>/api/data/?bme280=show</a></p>
			</div>
			<div class="w3-container">
				<p>Show data from CPU and BME280 sensors</p>
			</div>
			<div class="w3-container w3-light-grey">
				<p><a href="/api/data/?cpu=show&bme280=show">http://<?=$server_ip?>/api/data/?cpu=show&bme280=show</a></p>
			</div>
			<br>
		</div>
	<body>
</html>
