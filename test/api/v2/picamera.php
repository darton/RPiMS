<?php

$dir = '/var/www/html/pictures';
$raspistill_path = "/usr/bin/raspistill";

$picamera = [];
$picture = $_GET['picture'];
$id = $_GET['filename'];

if (isset($_GET['rotate'])){
    $rotate = $_GET['rotate'];
    if ($rotate >= 0 and $rotate <= 360){
	$rotate = $_GET['rotate'];
    }
    else {
	$rotate = 0;
    }
}
else {
    $rotate = 0;
}


if (isset($_GET['horizontal_flip'])){
    if ($_GET['horizontal_flip'] == "yes"){
	$horizontal_flip = "-hf";
	$hf = "yes";
    }
    else {
	$horizontal_flip = "";
	$hf = "no";
    }
}
else {
    $horizontal_flip = "";
    $hf = "no";
}

if (isset($_GET['vertical_flip'])){
    if ($_GET['vertical_flip'] == "yes"){
	$vertical_flip = "-vf";
	$vf = "yes";
    }
    else {
	$vertical_flip = "";
        $vf = "no";
    }
}
else {
    $vertical_flip = "";
    $vf = "no";
}


$picamera['settings']['picture_url'] = "/pictures/";
$picamera['settings']['picture_list'] = "/api/picamera.php?picture=list";
$picamera['settings']['picture_grab'] = "/api/picamera.php?picture=grab&filename=picturefilename";
$picamera['settings']['picture_delete'] = "/api/picamera.php?picture=delete&filename=picturefilename";
$picamera['settings']['horizontal_flip'] = $hf;
$picamera['settings']['vertical_flip'] = $vf;
$picamera['settings']['rotate'] = $rotate ;


if (isset($picture) and isset($id) ){
    if ($picture == 'grab'){
	exec("sudo " . $raspistill_path . " " . $vertical_flip . " " . $horizontal_flip . " -rot " . $rotate . " -o " . $dir . "/" . $id);
        $picamera = [];
	$picamera['status'] = "Photo $id grabed";
    }

    if ($picture == 'delete'){
	if (!unlink($dir."/".$id)) {
	    $picamera = [];
    	    $picamera['status'] = "Photo $id can not be deleted";
	}
	else {
	    $picamera = [];
	    $picamera['status'] = "Photo $id has been deleted";
	    }
    }
}

if ($picture == 'list'){
    $files = scandir($dir);
    $picamera = [];
    foreach ($files as $key => $value) {
        if ('.' !== $value && '..' !== $value){
	    $pictures_lst[]=$value;
	    $picamera['pictures'] = $pictures_lst;
   }
}

}

Header("Content-type: application/json");
echo json_encode($picamera);

?>
