var check_mess = 1;
var block = document.getElementById("chat-messages");
block.scrollTop = 10000000 ;

function get_messages(){
        $.get( "/get_messages", function( data ) {
            if (document.getElementById("text").innerHTML != data.data){
                document.getElementById("text").innerHTML = data.data;
			    block.scrollTop = 10000000;
            }
        });
    }

setInterval(() => get_messages(), 50);
