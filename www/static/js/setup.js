
var tlspskidentityid = "TLSPSKIdentity";
var tlspskid = "TLSPSK";

/* Function to generate combination of PSK */
function generateP(lenght) {
        const RandomHex = size => [...Array(size)].map(() => Math.floor(Math.random() * 16).toString(16)).join('');
        return RandomHex(lenght);
        }

function gfg_Run(psk_len,id) {
            document.getElementById(id).value =  generateP(psk_len);
        }


function showFunction(id) {
            var x = document.getElementById(id);
            if (x.className.indexOf("w3-show") == -1) {
                x.className = x.className.replace(" w3-hide", "");
                x.className += " w3-show";
            }
          }

function hideFunction(id) {
            var x = document.getElementById(id);
            if (x.className.indexOf("w3-hide") == -1) {
                x.className = x.className.replace(" w3-show", "");
                x.className += " w3-hide";
            }
          }

function gpioSH(id) {
            var x = document.getElementById(id);
            if (x.className.indexOf("w3-show") == -1) {
                x.className += " w3-show";
            }
            else {
                x.className = x.className.replace(" w3-show", "");
            }
          }


document.addEventListener("DOMContentLoaded", () => {

var select2 = document.body.querySelector('#id2_BME280_serial_port_select')
var select3 = document.body.querySelector('#id3_BME280_serial_port_select')

var select3si = document.body.querySelector('#id3_BME280_serial_port_select').selectedIndex
for ( var i=0; i<select2.length; i++ ) {
    if (select2.options[i].value == select3.options[select3si].value){
	    select2.remove(i);
    }
}

var select2si = document.body.querySelector('#id2_BME280_serial_port_select').selectedIndex
for ( var i=0; i<select3.length; i++ ) {
    if (select3.options[i].value == select2.options[select2si].value) {
	    select3.remove(i);
    }
}

var id2_selectedport = $('#id2_BME280_serial_port_select').children("option:selected").val();
//var id2_selectedid = $('#id2_BME280_serial_port_select').attr('id');
var id3_selectedport = $('#id3_BME280_serial_port_select').children("option:selected").val();
//var id3_selectedid = $('#id3_BME280_serial_port_select').attr('id');

$('.serial-port').change(function() {
    var selectedport = $(this).children("option:selected").val();
    var selectedid = $(this).attr('id');
    if (selectedid == 'id2_BME280_serial_port_select') {
        $('#id3_BME280_serial_port_select').find('option[value='+ selectedport +']').remove();
        $('#id3_BME280_serial_port_select').append($("<option></option>").attr("value", id2_selectedport).text(id2_selectedport));
        id2_selectedport = $('#id2_BME280_serial_port_select').children("option:selected").val();
        //console.log(selectedport,selectedid);
    }

    if (selectedid == 'id3_BME280_serial_port_select') {
        $('#id2_BME280_serial_port_select').find('option[value='+ selectedport +']').remove();
        $('#id2_BME280_serial_port_select').append($("<option></option>").attr("value", id3_selectedport).text(id3_selectedport));
        id3_selectedport = $('#id3_BME280_serial_port_select').children("option:selected").val();
        //console.log(selectedport,selectedid);
    }
})

/* When the page is loaded it shows the input Hold Time for the GPIO Button input type.
Hides the field for another GPIO input type value.  */
$('.gpioinputs').each(function() {
            var selectedGPIOtype = $(this).children("option:selected").val();
            var z = $(this).attr('id') + "_" + 'DS'
            if (selectedGPIOtype == 'DoorSensor' || selectedGPIOtype == 'ShutdownButton' ) {
                $("#" + z).show();
            }
            else {
                $("#" + z).hide();
            }
        });

/* Shows input Hold Time when GPIO input type is selected as Button,
and sets default hold time value to 1. 
Hides this field when other GPIO input type is selected. */
$('.gpioinputs').change(function(){
            var selectedGPIOtype = $(this).children("option:selected").val();
            var z = $(this).attr('id') + "_" + 'DS'
            if (selectedGPIOtype == 'DoorSensor' || selectedGPIOtype == 'ShutdownButton') {
                $("#" + z).show();
		$("#" + z + "_HT").val("1");
            }
            else {
                $("#" + z).hide();
            }
        });

/*
$('#id1_BME280_interface').change(function(){
            var selectedInterfacetype = $(this).children("option:selected").val();
            if (selectedInterfacetype == 'i2c') {
                $("#id1_BME280_i2c_address").show();
                $("#id1_BME280_serial_port").hide();
            }
            else {
                $("#id1_BME280_i2c_address").hide();
                $("#id1_BME280_serial_port").show();
            }
        });

$('#id1_BME280_interface').each(function(){
            var selectedInterfacetype = $(this).children("option:selected").val();
            if (selectedInterfacetype == 'i2c') {
                $("#id1_BME280_i2c_address").show();
                $("#id1_BME280_serial_port").hide();
            }
            else {
                $("#id1_BME280_i2c_address").hide();
                $("#id1_BME280_serial_port").show();
            }
        });
*/

$("#use_serial_display").change(function() {
    if(this.checked) {
        showFunction('serial_display')
    }
    if (!(this.checked)) {
        hideFunction('serial_display')
    }
});

$("#use_serial_display").each(function() {
    if(this.checked) {
        showFunction('serial_display') 
    }
    if (!(this.checked)) {
        hideFunction('serial_display')
    }
});

$("#use_picamera").change(function() {
    if(this.checked) {
        showFunction('picamera')
    }
    if (!(this.checked)) {
        hideFunction('picamera')
    }
});

$("#use_picamera").each(function() {
    if(this.checked) {
        showFunction('picamera')
    }
    if (!(this.checked)) {
        hideFunction('picamera')
    }
});

$("#use_weather_station").change(function() {
    if(this.checked) {
        showFunction('weather_station')
    }
    if (!(this.checked)) {
        hideFunction('weather_station')
    }
});

$("#use_weather_station").each(function() {
    if(this.checked) {
        showFunction('weather_station')
    }
    if (!(this.checked)) {
        hideFunction('weather_station')
    }
});

$("#use_dht_sensor").change(function() {
    if(this.checked) {
        showFunction('DHT_sensor')
    }
    if (!(this.checked)) {
        hideFunction('DHT_sensor')
    }
});

$("#use_dht_sensor").each(function() {
    if(this.checked) {
        showFunction('DHT_sensor')
    }
    if (!(this.checked)) {
        hideFunction('DHT_sensor')
    }
});

$("#use_bme280_sensor").change(function() {
    if(this.checked) {
        showFunction('BME280_sensor')
    }
    if (!(this.checked)) {
        hideFunction('BME280_sensor')
    }
});

$("#use_bme280_sensor").each(function() {
    if(this.checked) {
        showFunction('BME280_sensor')
    }
    if (!(this.checked)) {
        hideFunction('BME280_sensor')
    }
});

$("#id1_BME280_use").change(function() {
    if(this.checked) {
        showFunction('id1_BME280')
    }
    if (!(this.checked)) {
        hideFunction('id1_BME280')
    }
});

$("#id1_BME280_use").each(function() {
    if(this.checked) {
        showFunction('id1_BME280')
    }
    if (!(this.checked)) {
        hideFunction('id1_BME280')
    }
});

$("#id2_BME280_use").change(function() {
    if(this.checked) {
        showFunction('id2_BME280')
    }
    if (!(this.checked)) {
        hideFunction('id2_BME280')
    }
});

$("#id2_BME280_use").each(function() {
    if(this.checked) {
        showFunction('id2_BME280')
    }
    if (!(this.checked)) {
        hideFunction('id2_BME280')
    }
});

$("#id3_BME280_use").change(function() {
    if(this.checked) {
        showFunction('id3_BME280')
    }
    if (!(this.checked)) {
        hideFunction('id3_BME280')
    }
});

$("#id3_BME280_use").each(function() {
    if(this.checked) {
        showFunction('id3_BME280')
    }
    if (!(this.checked)) {
        hideFunction('id3_BME280')
    }
});

$("#use_ds18b20_sensor").change(function() {
    if(this.checked) {
        showFunction('DS18B20_sensor')
    }
    if (!(this.checked)) {
        hideFunction('DS18B20_sensor')
    }
});

$("#use_ds18b20_sensor").each(function() {
    if(this.checked) {
        showFunction('DS18B20_sensor')
    }
    if (!(this.checked)) {
        hideFunction('DS18B20_sensor')
    }
});

$("#use_cpu_sensor").change(function() {
    if(this.checked) {
        showFunction('CPU_sensor')
    }
    if (!(this.checked)) {
        hideFunction('CPU_sensor')
    }
});

$("#use_cpu_sensor").each(function() {
    if(this.checked) {
        showFunction('CPU_sensor')
    }
    if (!(this.checked)) {
        hideFunction('CPU_sensor')
    }
});


});
