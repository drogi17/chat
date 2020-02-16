$.get( "/get_chats", function(data) {   // Получить все чаты
            var chats = data.text;      // Получить все чаты из отвеа с сервера
            var html_to_add = '<button href="javascript:void(0)" class="closebtn" onclick="closeNav()"><i class="fa fa-times" aria-hidden="true"></i></button>' // кнопка закрыть список
            var max = chats.length;     // Длина спискка чатов
            var i = 0;                  // начальный элемент
            while (i <= max-1) {        //Цикл
                var html_element =  '<a href="/chats/'+ chats[i][0] +'"# class="chat-block d-flex justify-content-between"><img src="' + chats[i][1]
                + '" class="chat-block-image"><div class="chat-preview d-flex"><p class="mb-auto p-2 bd-highlight">' + chats[i][0]
                + "</p></div></a>"; // Строка добавления. 
                html_to_add += html_element; // Добавить в html_to_add
                i++;
            }
            document.getElementById("mySidepanel").innerHTML = html_to_add; // вставить в блок
        }); 