let online_user_container = document.getElementById('online-users-container')


let setupChats = async (groupUUID, username) => {
    console.log(groupUUID)
    const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + "/"
        + groupUUID
        + "/"
    );

    chatSocket.onopen = function (e) {
        console.log("The connection was setup successfully !");
    };

    chatSocket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };
    document.querySelector("#id_message_send_input").focus();
    document.querySelector("#id_message_send_input").onkeyup = function (e) {
        if (e.keyCode == 13) {
            document.querySelector("#id_message_send_button").click();
        }
    };
    document.querySelector("#id_message_send_button").onclick = function (e) {
        var messageInput = document.querySelector(
            "#id_message_send_input"
        ).value;
        chatSocket.send(JSON.stringify({message: messageInput, username: username}));
    };
    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        var div = document.createElement("div");
        var innerdiv = document.createElement("div");
        var span = document.createElement("span");
        var para = document.createElement("p");
        div.innerHTML = `<img src="${data.img}" width="50" height="50"> `
        para.style.fontSize = '12px';

        para.innerHTML = `
            <span class="float-left">${data.username}</span>
            <span class="float-right" dir="ltr">${data.datetime}</span>
            `
        span.innerHTML = `${data.message}`


        innerdiv.classList.add('col-md-4', 'card', 'shadow')

        if (username == data.username) {
            div.dir = 'rtl'
            span.dir = "ltr"
            innerdiv.style.backgroundColor = "rgba(130, 243, 183, 0.72)"
        } else {
            innerdiv.style.backgroundColor = "rgba(47, 193, 239, 0.68)"

        }

        innerdiv.appendChild(para)
        innerdiv.appendChild(span)


        div.appendChild(innerdiv)


        div.classList.add('mb-2')
        console.log(div)

        document.querySelector("#id_message_send_input").value = "";
        document.querySelector("#id_chat_item_container").appendChild(div);
    };


}

let getOnlineUsersList = async (group_id) => {
    data = await fetch(`/chats/group_online_users/${group_id}`)
        .then(function (response) {
            return response.json();
        })
        .then(function (json) {
            json.forEach(function (obj) {
                online_user_container.innerHTML += `<img src="${obj[1]}" class="mr-2 " width="50" height="50">` + obj[0] + '<br>'
            })
        });
}