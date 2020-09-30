var tlspskidentityid = "TLSPSKIdentity";
var tlspskid = "TLSPSK";

/* Function to generate combination of PSK */
function generateP(lenght) {
	var pass = '';
        var str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' +
                    'abcdefghijklmnopqrstuvwxyz0123456789';
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
