
setInterval(function() {
    $.getJSON("/api/picamera.php?picture=list", function(data) {

$("#picture").html(data['pictures']['0']);

});
}, 500);
