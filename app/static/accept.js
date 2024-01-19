var socket;
$(document).ready(function(){
    socket = io.connect(window.location.host);
    socket.on('requested', function(data) {
                const btn = document.createElement('div');
                btn.className += "row"
                btn.innerHTML= '<span>'+data['user']+'</span><input type="submit" class="btn btn-success" name={{p}} value="Admit">'
                const node = document.getElementById("buttons")
                node.appendChild(btn)
    });
});