const socket = io();

document.getElementById("message").addEventListener("keyup", function(event) {
    if (event.key == "Enter") {
        let message = document.getElementById("message").value;
        if (message.length < 1) {return;}
        chatname = document.getElementById("chatname").getAttribute("data-name");
        socket.emit("new_message", chatname, message);
        document.getElementById("message").value = "";
    }
})

socket.on("chat", function(data) {
    let ul = document.getElementById("chat_messages");
    let li = document.createElement("li");
    li.setAttribute("style", "max-width: 500px; word-wrap: break-word;");
    li.appendChild(document.createTextNode(data["login"] + ": " + data["message"]));
    let jinjaNumber = document.getElementById("chat").getAttribute("data-login");
    if (data["login"] == jinjaNumber) {
        let delete_button = document.createElement("li");
        delete_button.setAttribute("style", "width: 15px; height: 7px; background-color: #FF3300;");
        let bar = document.createElement("div");
        bar.setAttribute("style", "display: flex; justify-content: flex-end; align-items: center;");
        bar.appendChild(li);
        bar.appendChild(delete_button);
        ul.appendChild(bar);
    } else {
        ul.appendChild(li);
    }
})