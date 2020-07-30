table>
<?php
$redis = new Redis();
$redis->connect('127.0.0.1', 6379);
    foreach ($_POST as $key => $value) {
        echo "<tr>";
        echo "<td>";
        echo $key;
        echo "</td>";
        echo "<td>";
        echo $value;
        echo "</td>";
        echo "</tr>";
        $redis->set($key,$value);
    }
//$yaml = yaml_emit($_POST);
//var_dump($yaml);
?>
</table>
