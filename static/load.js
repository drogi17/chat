// $("#messages").load("/messages");

var data = $.get('/messages', 
    function(data_take) {
        return data_take
});


$('#messages').infinitescroll({
    //dataSource is required to append additional content
    dataSource: function(helpers, callback){
        //passing back more content
        callback({ content: data});
    }
});