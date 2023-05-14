var username = JSON.parse(document.getElementById('user_from_username').innerText);

console.log(window.location.host)
const online_status = new WebSocket("ws://" + window.location.host +"/ws/online/");

online_status.onopen = function(e){
    console.log('websocket connected online')
    dict = {'status':'online',
            }
    online_status.send(JSON.stringify(dict))
};

online_status.onmessage = function(event){
    console.log('recive msg from server online', event)
    data = JSON.parse(event.data)

    if(data.username != username ){
        if(data.status == true){
            console.log(data.username)
            document.getElementById(`chat-online-${data.username}`).innerHTML = 
            '<p class="text-success">online</p>'
        } else{
            document.getElementById(`chat-online-${data.username}`).innerHTML = 
            '<p class="text-warning">offline</p>'
        }        
    } 
};


online_status.onclose = function(event){
    console.log('websocket close online ')
};