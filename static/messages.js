var check_mess = 1;
var all_text = 0;



$(document).ready(function() {

    var socket = io.connect('/');

    socket.on('connect', function() {
        socket.send({'data': ''});
    });

    socket.on('message', function(text) {
        // console.log(text[0] == 'exit' && text[1] == document.cookie);
        if (text[0] == 'exit' && text[1] == document.cookie){
            document.cookie = "username="
            window.location.href = '/';
        }
        html_to_add = '';
        var max = text.length;
        var i = 0;

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
        var block = document.getElementById("chat-messages");
        block.scrollTop = 10000000 ;
        all_text = text.length;
        document.getElementById("message_text").value = '';
    });
    $('#send-button').on('click', function() {
        var send_data = document.getElementById("message_text").value;
        socket.send({'data':send_data});
    });
    document.addEventListener('keydown', function(event) {
      if (event.code == 'Enter') {
        var send_data = document.getElementById("message_text").value;
        socket.send({'data':send_data});
      }
    });

});

