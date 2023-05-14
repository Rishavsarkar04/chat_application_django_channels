var user_to_username = JSON.parse(document.getElementById('user_to_username').innerText);
var groupnmae = JSON.parse(document.getElementById('groupname').innerText);
var username = JSON.parse(document.getElementById('user_from_username').innerText);
var user_to_username = JSON.parse(document.getElementById('user_to_username').innerText);



const chat_noti = new WebSocket("ws://" + window.location.host +"/ws/noti/");

chat_noti.onopen = function(e){
    console.log('websocket connected chat noti')
    
};


chat_noti.onmessage = function(event){
    console.log('recive msg from server chat', event)
    data = JSON.parse(event.data)
    console.log(data)
    console.log(data.status)
    console.log(data.num)
    console.log(data.form_user)
    console.log(data.current_user , 'data curren')
    console.log(username , 'request user')
    
    if (data.current_user == username){
        
        if (data.status == 'unseen'  && user_to_username!=data.form_user ){document.getElementById(`${data.form_user}_chat_noti`).innerHTML = 
            `${data.num}`}
        else{
            document.getElementById(`${data.form_user}_chat_noti`).innerHTML = ''
        }
        
    }

};



chat_noti.onclose = function(event){
    console.log('websocket close chat noti ')
};