const socket = io();
document.getElementById("message").addEventListener("keyup", function(event) {
    if (event.key == "Enter") {
        let message = document.getElementById("message").value;
        chat_name = document.getElementById("chat_name").getAttribute("data-name");
        console.log(chat_name)
        socket.emit("new_message", chat_name, message);
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