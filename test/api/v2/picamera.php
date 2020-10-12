<?php

$picamera = [];
$picture = $_GET['picture'];
$id = $_GET['filename'];
$dir = '/var/www/html/pictures';

$picamera['settings']['picture_url'] = "/pictures/";
$picamera['settings']['picture_list'] = "/api/picamera.php?picture=list";
$picamera['settings']['picture_grab'] = "/api/picamera.php?picture=grab&filename=picturefilename";
$picamera['settings']['picture_delete'] = "/api/picamera.php?picture=delete&filename=picturefilename";


if (isset($picture) and isset($id) ){
    if ($picture == 'grab'){
	exec("sudo /home/pi/scripts/RPiMS/grab_pictures.sh ".$id);
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
