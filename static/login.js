function login() {                                                  // регистрация или вход
    var username = document.getElementById("username").value;       // логин юзера
    $.ajax({                                                        // AJAX запрос:
        type: 'POST'                                                //      POST типа
        , url: '/login'                                             //      На хост - /login
        , data: username                                            //      отправка данных (двнные - username)
        , contentType: false                                        //      контент не пизированый
        , cache: false                                              //      Без хэша
        , processData: false                                        //      
        , success: function () {                                    //      При приянытии ответа, перейти в дерикторию /
            // console.log(data.data);                              //      
            window.location.href = '/';                             //      переход в /
        }
    , });
    document.getElementById("username").value = '';                 // Убрать данные с input 
}