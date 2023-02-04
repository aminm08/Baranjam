let setupChats = async (groupName, groupSlug, username) => {

    const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + "/"
        + groupSlug
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

        div.innerHTML = `<img src="${data.img}" width="50" height="50">  ` + data.username + " : " + data.message;
        div.classList.add('mb-2')

        document.querySelector("#id_message_send_input").value = "";
        document.querySelector("#id_chat_item_container").appendChild(div);
    };


}