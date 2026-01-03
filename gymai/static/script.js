async function send() {
    const input = document.getElementById("input");
    const chat = document.getElementById("chat");
    const msg = input.value.trim();

    if (!msg) return;

    // User message
    const userDiv = document.createElement("div");
    userDiv.className = "msg user";
    userDiv.innerText = msg;
    chat.appendChild(userDiv);

    input.value = "";
    chat.scrollTop = chat.scrollHeight;

    // Typing indicator
    const typing = document.createElement("div");
    typing.className = "msg bot";
    typing.id = "typing";
    typing.innerText = "Typing...";
    chat.appendChild(typing);
    chat.scrollTop = chat.scrollHeight;

    // Send to backend
    const res = await fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: msg })
    });

    const data = await res.json();

    // Remove typing
    typing.remove();

    // Bot reply
    const botDiv = document.createElement("div");
    botDiv.className = "msg bot";
    botDiv.innerText = data.reply;
    chat.appendChild(botDiv);

    chat.scrollTop = chat.scrollHeight;
}

// Send on Enter key
document.getElementById("input").addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        send();
    }
});
