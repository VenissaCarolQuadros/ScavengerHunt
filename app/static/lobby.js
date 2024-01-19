var socket;
$(document).ready(function(){
    socket = io.connect(window.location.host);
    socket.on('accepted', function(data) {
        if (data['user']==user){
            var url = "http://"+window.location.host+"/start/play/"+user
            window.location.replace(url)
        }
    });
    socket.emit("requesting", {'user':user})
    
});