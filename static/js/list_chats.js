const socket = io();
document.getElementById("find").addEventListener("keyup", function(event) {
    if (event.key == "Enter") {
        let data = document.getElementById("find").value;
        socket.emit("new_find_chat", data);
        document.getElementById("find").value = "";
    }
})
socket.on("list_find_chats", function(data) {
    let ul = document.getElementById("list_find_chat");
    let li = document.createElement("li");
    li.addEventListener("click", function(event) {
        if (event) {
            console.log(data)
            chat_link = document.getElementById("chat_link");
            console.log(chat_link + "?open_chat=" + data)
            window.location.href = chat_link + "?open_chat=" + data;
        }
    });
    li.appendChild(document.createTextNode(data));
    ul.appendChild(li);
})