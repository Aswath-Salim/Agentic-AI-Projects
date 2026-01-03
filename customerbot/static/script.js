async function send() {
  const input = document.getElementById("input");
  const chat = document.getElementById("chat");
  const message = input.value.trim();
  if (!message) return;

  const userDiv = document.createElement("div");
  userDiv.className = "msg user";
  userDiv.innerText = message;
  chat.appendChild(userDiv);

  input.value = "";
  chat.scrollTop = chat.scrollHeight;

  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  });

  const data = await res.json();

  const botDiv = document.createElement("div");
  botDiv.className = "msg bot";
  botDiv.innerText = data.reply;
  chat.appendChild(botDiv);

  chat.scrollTop = chat.scrollHeight;
}
