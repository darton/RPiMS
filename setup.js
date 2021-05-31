
var tlspskidentityid = "TLSPSKIdentity";
var tlspskid = "TLSPSK";

/* Function to generate combination of PSK */
function generateP(lenght) {
        var pass = '';
        var str = 'abcdef0123456789';
        for (i = 1; i <= lenght; i++) {
                var char = Math.floor(Math.random()
                            * str.length + 1);
                pass += str.charAt(char)
            }
            return pass;
        }

        function gfg_Run(psk_len,id) {
            document.getElementById(id).value =  generateP(psk_len);
        }


document.addEventListener("DOMContentLoaded", () => {

/* When the page is loaded it shows the input Hold Time for the GPIO Button input type.
Hides the field for another GPIO input type value.  */
$('.gpioinputs').each(function(){
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
});
