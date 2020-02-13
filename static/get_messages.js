var check_mess = 1;
var block = document.getElementById("chat-messages");
block.scrollTop = 10000000 ;
var all_text = 0;


function get_messages(){
        $.get( "/get_messages", function( data ) {
            var text = data.text
            if (all_text != text.length){
                html_to_add = ''
            	var max = text.length;
                var i = 0;
                // console.log(max);
                while (i <= max-1) {
                    // console.log(text[i]);
                    var img = "https://www.iphones.ru/wp-content/uploads/2017/02/AA-4.png";
                    var html_element =  "<div class='message-block'><img src='" + text[i][1] + 
                                        "' class='message-avatar'><div class='message-data'><span class='message-user'>" + text[i][0] +
                                        "</span><br><span class='message-text'>" + text[i][2] + "</span></div></div>";
                    html_to_add += html_element;
                    i++;
                }
                document.getElementById("text").innerHTML = html_to_add;
			    block.scrollTop = 10000000;
			    all_text = text.length;
            }
        });
    }
// get_messages();
setInterval(() => get_messages(), 100);
