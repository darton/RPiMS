<!DOCTYPE html>
<html lang="en">
	<meta charset="utf-8"/>
	<meta name="description" content="RPiMS - Raspberry Pi Monitoring System">
	<meta name="keywords" content="Raspberry Pi, Monitoring System, Sensors">
	<meta name="author" content="Dariusz Kowalczyk">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="/css/w3.css">
	<link rel="stylesheet" href="/css/w3-colors-2020.css">
	<script src="/js/navbar.js"></script>
	<title>RPiMS API</title>
	<body>
		<div class="w3-row w3-2020-ultramarine-green">
			<div class="w3-dropdown-click">
				<button onclick="navFunction()" class="w3-button w3-2020-ultramarine-green w3-xlarge">☰ API</button>
				<div id="NavBar" class="w3-dropdown-content w3-bar-block w3-card-4 w3-animate-zoom">
					<a href="/" class="w3-bar-item w3-button w3-large">Start</a>
					<a href="/setup/" class="w3-bar-item w3-button w3-large">Setup</a>
				</div>
			</div>
		</div>
		<div class="w3-2020-brilliant-white">
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
				<p>GPIO sensors</p>
			</div>
			<div class="w3-container w3-light-grey">
				<p><a href="/api/data/?gpio=show">http://<?=$server_ip?>/api/data/?gpio=show</a></p>
			</div>

			<div class="w3-container">
				<p>BME280 sensors</p>
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
	</body>
</html>
