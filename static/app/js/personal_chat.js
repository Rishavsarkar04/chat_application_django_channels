var user_to_username = JSON.parse(document.getElementById('user_to_username').innerText);
var user_to_id = document.getElementById('user_to').innerText;
var user_from_username = JSON.parse(document.getElementById('user_from_username').innerText);

const ws2 = new WebSocket("ws://" + window.location.host +"/ws/" + user_to_id + "/");


ws2.onopen = function(e){
    console.log('websocket connected chat')

};
ws2.onmessage = function(event){
    console.log('recive msg from server chat', event)
    data = JSON.parse(event.data)
    if (data.user_from == user_from_username){
        document.getElementById('conversation').innerHTML += `
        <div class="row message-body">
                    <div class="col-sm-12 message-main-sender">
                        <div class="sender">
                            <div class="message-text">
                                ${data.message}
                            </div>
                            <span class="message-time pull-right">
                                ${data.time}
                            </span>
                        </div>
                    </div>
                </div>`
               
         
    } else { document.getElementById('conversation').innerHTML += `
                <div class="row message-body">
                    <div class="col-sm-12 message-main-receiver">
                    <div class="receiver">
                        <div class="message-text">
                            ${data.message}
                        </div>
                        <span class="message-time pull-right">
                            ${data.time}
                        </span>
                    </div>
                    </div>
                </div>`
               
    }
};



ws2.onclose = function(event){
    console.log('websocket close chat')
};





document.getElementById('chat-btn').addEventListener("click",function(){
        const msg_input = document.getElementById('comment')
        const msg = msg_input.value
        dict = {
        'msg':msg,
        'user_to':user_to_username,
        'user_from':user_from_username
                }
        ws2.send(JSON.stringify(dict));
        msg_input.value ='';
})
   




// for scrolling purpose 
var objDiv = document.getElementById("conversation");
objDiv.scrollTop = objDiv.scrollHeight;