function send() {
    var message_text = document.getElementById("message_text").value;
    $.ajax({
        type: 'POST'
        , url: '/send_text'
        , data: message_text
        , contentType: false
        , cache: false
        , processData: false
        , success: function (data) {
            // console.log(data)
            if (data.exit == 1) {
                window.location.href = '/';
            }
        }
    });
    document.getElementById("message_text").value = '';
}

document.addEventListener('keydown', function(event) {
  if (event.code == 'Enter') {
    send();
  }
});


$(document).ready(function(){
    $("#message_text").keypress(function (e)  
    {
        // console.log('пишет');
    });
  });