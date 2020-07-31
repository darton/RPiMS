<table>
<?php
$redis = new Redis();
$redis->connect('127.0.0.1', 6379);

    foreach ($_POST as $key => $value) {
        echo "<tr>";
        echo "<td>";
        //echo $key;
        echo "</td>";
        echo "<td>";
        //echo $value;
        echo "</td>";
        echo "</tr>";
        //$redis->set($key,$value);
    }
//$yaml = yaml_emit($_POST);
//var_dump($yaml);

$data = yaml_parse_file ("/home/pi/scripts/RPiMS/rpims.yaml");
//print_r(array_keys($data));
echo "<br/>";
print_r(array_keys($data['setup']));
echo "<br/>";
echo "<br/>";
print_r(array_keys($data['door_sensors']));
echo "<br/>";
echo "<br/>";
print_r(array_keys($data['motion_sensors']));
echo "<br/>";
echo "<br/>";
print_r(array_keys($data['system_buttons']));
echo "<br/>";
echo "<br/>";
print_r(array_keys($data['led_indicators']));
echo "<br/>";
echo "<br/>";
print_r(array_keys($data['zabbix_agent']));
//print_r($_POST);


yaml_emit_file ("/var/www/html/rpims/rpims2.yaml", $yaml);

?>


</table>
