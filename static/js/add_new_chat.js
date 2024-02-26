const socket = io();

document.getElementById("create_new_chat").addEventListener("keyup", function(event) {
    if (event.key == "Enter") {
        let message = document.getElementById("create_new_chat").value;
        if (message.length < 4) {
            alert('Название должно иметь более 4 символов');
            return;
        }
        socket.emit("add_new_chat", message);
        document.getElementById("create_new_chat").value = "";
    }
})

socket.on("add_new_chat", function(data) {
    alert(data);
})