<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="description" content="RPiMS - Raspberry Pi Monitoring System">
    <meta name="keywords" content="Raspberry Pi, Monitoring System, Sensors">
    <meta name="author" content="Dariusz Kowalczyk">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="/css/index.css">
    <link rel="stylesheet" href="/css/w3.css">
    <link rel="stylesheet" href="/css/w3-colors-2020.css">
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    <script src="/js/jquery.min.js"></script>
    <script src="/js/navbar.js"></script>
    <script src="/js/index.js" defer></script>
    <title>RPiMS</title>
  </head>
  <body>
    <div class="w3-row w3-2020-ultramarine-green">
      <div class="w3-dropdown-click">
        <button onclick="navFunction()" class="w3-button w3-2020-ultramarine-green w3-xlarge">☰</button>
        <div id="NavBar" class="w3-dropdown-content w3-bar-block w3-card-4 w3-animate-zoom">
          <a href="/setup/" class="w3-bar-item w3-button w3-large">Setup</a>
          <a href="/api/" class="w3-bar-item w3-button w3-large">API</a>
        </div>
      </div>
    </div>

    <div class="rpimsbg">
      <div class="header"></div>

      <?php if ($config["show_sys_info"] == "True") {?>
        <div class="sensors" style="text-align: left;">
              <ul style="list-style-type:none;">
                <li>Hostname: <span class="value" id="hostname"></span></li>
                <li>Location: <span class="value" id="location"></span></li>
                <?php if ($config["use_cpu_sensor"] == "True") {?>
                <li>CPU Temperature: <span class="value" id="CPU_Temperature"> </span><span class="value" id="CPU_Temperature_unit"></span></li>
                <?php }?>
              </ul>
        </div>
      <?php }?>


      <?php if ($config["use_picamera"] == "True") {
        echo '<div class="sensors">';
        echo '<div><a class="sensors" href="http://'.$server_ip.':8080/stream/video.mjpeg">Video Stream URL</a></div>';
        echo '<div><iframe src="http://'.$server_ip.':8080/stream/video.mjpeg" width="100%" height="'.$picamera_height.'" style="border:none;" title="Video Stream"></iframe></div>';
        echo '</div>';
       }
      ?>

      <?php if ($config["use_dht_sensor"] == "True") {?>
        <div class="sensors">
          <div class="w3-container w3-margin">DHT Sensor</div>
          <div style="width: 100%; display: table;">
            <div style="display: table-row">
              <div class="gauge_dht" id="g11" display: table-cell";>
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

      <?php if ($config["use_bme280_sensor"] == "True") {?>
        <?php
            foreach ($sensors['BME280'] as $key => $value)
            {
          if ($value['use'] == "true")
          {
              $t = $key."_BME280_Temperature";
              $h = $key."_BME280_Humidity";
              $p = $key."_BME280_Pressure";
                    $n = $key."_BME280_name";

          echo "<div class='sensors'>";
              echo "<div id='$n' class='w3-container w3-margin'></div>";
              echo "<div style='width: 100%; display: table;'>";
              echo "<div style='display: table-row';>";

              echo " <div class='gauge_bme280' id='$t'>";
              echo "    <div class='gauge__body'>";
              echo "        <div class='gauge__fill'></div>";
              echo "        <div class='gauge__cover'></div>";
              echo "    </div>";
              echo "    <div class='sensors'>Temp</div>";
              echo " </div>";

              echo " <div class='gauge_bme280' id='$h'>";
              echo "    <div class='gauge__body'>";
              echo "        <div class='gauge__fill'></div>";
              echo "        <div class='gauge__cover'></div>";
              echo "    </div>";
              echo "    <div class='sensors'>Hum</div>";
              echo " </div>";

              echo " <div class='gauge_bme280' id='$p'>";
              echo "    <div class='gauge__body'>";
              echo "        <div class='gauge__fill'></div>";
              echo "        <div class='gauge__cover'></div>";
              echo "    </div>";
              echo "    <div class='sensors'>Pres</div>";
              echo " </div>";
              echo "</div>";
              echo "</div>";
          echo "</div>";
          }
            }
        ?>
      <?php }?>

      <!--
      <?php if ($config["use_ds18b20_sensor"] == "True") {?>
        <div class="sensors">
          <h3>DS18B20 Sensors</h3>
          <p>
            <?php foreach ($DS18B20_sensors_list as $key => $value) {
              $item = $value."_name";
              echo "<input name=$item id=$item class='w3-input' type='text' value='$DS18B20_sensors[$item]'><br>";
            }
            ?>
          </p>
        </div>
      <?php }?>
      -->

      <?php if ($config["use_ds18b20_sensor"] == "True") {?>
        <?php  foreach ($DS18B20_sensors_detected as $key => $value) {
          $item = "DS18B20_".$value;
          $name = $value."_name";
          $ds18b20_sensor_name = $DS18B20_sensors[$value];
          echo "<div class='sensors'>";
          echo "<div class='w3-container w3-margin'>$ds18b20_sensor_name</div>";
          echo "<div style='width: 100%; display: table;'>";
          echo "  <div style='display: table-row'>";
          echo "    <div class='gauge_ds18b20' id='$item'>";
          echo "      <div class='gauge__body'>";
          echo "        <div class='gauge__fill'></div>";
          echo "        <div class='gauge__cover'></div>";
          echo "      </div>";
          echo "    </div>";
          echo "  </div>";
          echo "</div>";
          echo "</div>";
        }
        ?>
      <?php }?>

      <?php if ($config["use_door_sensor"] == "True") {?>
        <div class="sensors">
          <div class="w3-container w3-margin">Door sensors</div>
          <p>
            <table class="center">
              <?php foreach ($door_sensors as $key => $value) {
              echo "<tr><td>"; echo $value["name"]; echo "</td><td>: <span class='value' id='$key'></span></td></tr>";
              }
              ?>
            </table>
          </p>
        </div>
      <?php }?>

      <?php if ($config["use_motion_sensor"] == "True") {?>
        <div class="sensors">
          <div class="w3-container w3-margin">Motion sensors</div>
          <p>
            <table class="center">
              <?php foreach ($motion_sensors as $key => $value) {
              echo "<tr><td>"; echo $value["name"]; echo "</td><td>: <span class='value' id='$key'></span></td></tr>";
              }
              ?>
            </table>
          </p>
        </div>
      <?php }?>

      <?php if ($config["use_weather_station"] == "True") {?>
        <div class="sensors">
          <div class="w3-container w3-margin">Wind</div>
          <div style="width: 100%; display: table;">
            <div style="display: table-row">
              <div class="gauge" id="g4" style="width: 33%; display: table-cell">
                <div class="gauge__body">
                  <div class="gauge__fill"></div>
                  <div class="gauge__cover"></div>
                </div>
                <div class="sensors">Speed</div>
              </div>
              <div class="gauge" id="g5" style="width: 33%; display: table-cell">
                <div class="gauge__body">
                  <div class="gauge__fill"></div>
                  <div class="gauge__cover"></div>
                </div>
                <div class="sensors">Gust</div>
              </div>
              <div class="gauge" id="g6" style="width: 33%; display: table-cell">
                <div class="gauge__body">
                  <div class="gauge__fill"></div>
                  <div class="gauge__cover"></div>
                </div>
                <div class="sensors">Gust 24h</div>
              </div>
            </div>
          </div>
          <div class="w3-container">
            <table class="w3-table">
              <tr><td>Wind speed: </td><td><span class="value" id="wind_speed"></span><span class="value"> km/h</span></td></tr>
              <tr><td>Average Wind speed: </td><td><span class="value" id="average_wind_speed"></span><span class="value"> km/h</span></td></tr>
              <tr><td>Average Wind speed (Past 24h): </td><td><span class="value" id="daily_average_wind_speed"></span><span class="value"> km/h</span></td></tr>
              <tr><td>Wind gust: </td><td><span class="value" id="wind_gust"></span><span class="value"> km/h</span></td></tr>
              <tr><td>Peak Wind Gust (Past 24h): </td><td><span class="value" id="daily_wind_gust"></span><span class="value"> km/h</span></td></tr>
              <tr><td>Wind direction: </td><td><span class="value" id="average_wind_direction"></span><span class="value"> &#176 </span></td></tr>
              <tr><td>Rainfall (Past 24h): </td><td><span class="value" id="daily_rainfall"></span><span class="value"> mm</span></td></tr>
            </table>
          </div>
        </div>
      <?php }?>

      <div class="footer">
      </div>

    </div>
  </body>
</html>
