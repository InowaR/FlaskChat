const socket = io();
document.getElementById("message").addEventListener("keyup", function(event) {
    if (event.key == "Enter") {
        let message = document.getElementById("message").value;
        if (message.length < 4) {return;}
        chatname = document.getElementById("chatname").getAttribute("data-name");
        socket.emit("new_message", chatname, message);
        document.getElementById("message").value = "";
    }
})
socket.on("chat", function(data) {
    let ul = document.getElementById("chat_messages");
    let li = document.createElement("li");
    let br = document.createElement("br");
    li.appendChild(document.createTextNode(data["username"] + ": " + data["message"]));
    ul.appendChild(li);
    ul.appendChild(br);
})