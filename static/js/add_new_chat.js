const socket = io();
document.getElementById("create_new_chat").addEventListener("keyup", function(event) {
    if (event.key == "Enter") {
        let message = document.getElementById("create_new_chat").value;
        socket.emit("add_new_chat", message);
        document.getElementById("create_new_chat").value = "";
    }
})
socket.on("add_new_chat", function(data) {
    let message = document.createElement("h1");
    message.textContent = data;
    document.body.appendChild(message);
})