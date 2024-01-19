$(document).ready(function(){
    $.getJSON($SCRIPT_ROOT + '/clue/'+user,
    {},
    function(data){
        document.getElementById("writeup").textContent=data.hint;
        let img = document.createElement('img');
        img.src = data.image;
        document.getElementById('images').appendChild(img);
    });
});