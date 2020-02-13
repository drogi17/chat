function login() {
    var message_text = document.getElementById("username").value;
    $.ajax({
        type: 'POST'
        , url: '/login'
        , data: message_text
        , contentType: false
        , cache: false
        , processData: false
        , success: function () {
            // console.log(data.data);
            window.location.href = '/';
        }
    , });
    document.getElementById("username").value = '';
}