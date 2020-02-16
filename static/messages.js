// function deleteCookie() {
//   var del_co = document.cookie.split(';');
//   while(name = del_co.pop()) {
//   setCookie(name.split('=')[0],'11', -20, '/');
//   }
// }

function logout() {      
    document.cookie = "username=";  //          сделать куки имени пустым. (ГОВНОКОД)
    var socket = io.connect('/');   //          Подключится к /
    socket.send('$exit$');          //
    window.location.href = '/';     //          перейти в /
}

function send_data(socket) {
    var send_data = document.getElementById("message_text").value;                  // получить данные из input
    socket.send({'data':send_data, 'chat': window.location.pathname.substr(7)});    // Отправить данные из input
    document.getElementById("message_text").value = '';                             // очистить input
}


$(document).ready(function() {

    var socket = io.connect('/'); // Подключение сокета к /

    socket.on('connect', function() {		// выполнить при connect-е
        socket.send({'data':'', 'chat': window.location.pathname.substr(7)});
    });

    socket.on('message', function(text) {   // Приполучении сообщения
        if (text == 'exit'){				// Если сообщение exit:        
            logout();
        }
        var html_to_add = '';               // Обьявление текста для дополнения
        var max = text.length;              // Длина массива с сообщениями
        var i = 0;                          // первый элимент
        while (i <= max-1) {                // МОЖНО СДЕЛАТЬ ЧЕРЕЗ for
            if (text[i][3] == window.location.pathname.substr(7)) { // если чат сообения и  дериктория совпадают то добавить сообщение
                var img = "https://www.iphones.ru/wp-content/uploads/2017/02/AA-4.png";
                var html_element =  "<div class='message-block'><img src='" + text[i][1] + 
                                    "' class='message-avatar'><div class='message-data'><span class='message-user'>" + text[i][0] +
                                    "</span><br><span class='message-text'>" + text[i][2] + "</span></div></div>";
                html_to_add += html_element;
            }
            i++;
        }
        document.getElementById("text").innerHTML = html_to_add;    // Заменить html в нутри контейнера text на полученые сообщения
        var block = document.getElementById("chat-messages");       // ###ГОВНОКОД### обьявить элемент для скролла 
        block.scrollTop = 10000000 ;                                // ###ГОВНОКОД### Сделать скролл на 10000000 пикселей.
    });

    $('#send-button').on('click', function() {                      // если нажата кнопка для отправки сообщений
        send_data(socket);
    });
    document.addEventListener('keydown', function(event) {          // если нажата клавиша enter
      if (event.code == 'Enter') {
        send_data(socket);
      }
    });

});

