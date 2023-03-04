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

    chatSocket.onopen = function () {
        console.log("The connection was setup successfully !");
    };

    chatSocket.onclose = function () {
        console.error('Chat socket closed unexpectedly');
    };
    document.querySelector("#id_message_send_input").focus();
    document.querySelector("#id_message_send_input").onkeyup = function (e) {
        if (e.keyCode == 13) {
            document.querySelector("#id_message_send_button").click();
        }
    };
    document.querySelector("#id_message_send_button").onclick = function () {
        let messageInput = document.querySelector(
            "#id_message_send_input"
        ).value;

        if (messageInput) {

            chatSocket.send(JSON.stringify({message: messageInput, username: username}));
        }
    };
    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        let div = document.createElement("div");
        let innerdiv = document.createElement("div");
        let MessageContainer = document.createElement("span");
        let usernameAndCreateDateContainer = document.createElement("p");

        usernameAndCreateDateContainer.style.fontSize = '12px';


        MessageContainer.innerHTML = `${data.message}`


        innerdiv.classList.add('col-md-4', 'card', 'shadow')

        if (username == data.username) {
            usernameAndCreateDateContainer.innerHTML = `
                <span class="float-end">${data.username}</span>
                <span class="float-start" dir="ltr">${data.datetime}</span>`
            div.innerHTML = `<img src="${data.img}" class="chat-user-image" alt="user-img"> `
            div.dir = 'rtl'
            innerdiv.id = 'chat-box-this-user';


        } else {
            usernameAndCreateDateContainer.innerHTML = `
                <span class="float-end">${data.username}</span>
                <span class="float-start" >${data.datetime}</span>`
            div.innerHTML = `<img src="${data.img}" class="chat-user-image" alt="user-img"> `
            innerdiv.id = 'chat-box-other-user'

        }

        innerdiv.appendChild(usernameAndCreateDateContainer)
        innerdiv.appendChild(MessageContainer)


        div.appendChild(innerdiv)


        div.classList.add('mb-2')
        console.log(div)

        document.querySelector("#id_message_send_input").value = "";
        document.querySelector("#chat-item-container").appendChild(div);
    };


}

const getOnlineUsersList = async (group_id) => {

    $.ajax({
            'type': 'GET',
            'url': `/chats/group_online_users/${group_id}`,
            success: (res) => {
                const data = res;

                if (Array.isArray(data)) {
                    data.forEach(function (obj) {
                        console.log(obj);
                        online_user_container.innerHTML += `<img src="${obj[1]}" class="mr-2 chat-user-image"  alt="user-img">`
                            + obj[0] + '<br>'
                    })
                }

            }
        }
    )
}




