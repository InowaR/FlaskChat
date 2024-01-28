const socket = io();
document.getElementById("create_new_chat").addEventListener("keyup", function(event) {
    if (event.key == "Enter") {
        let message = document.getElementById("create_new_chat").value;
        if (message.length < 4) {return;}
        socket.emit("add_new_chat", message);
        message.value = "";
    }
})
socket.on("add_new_chat", function(data) {
    alert(data);
})