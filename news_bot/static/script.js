async function generate() {
  const topic = document.getElementById("topic").value;
  const output = document.getElementById("output");
  output.innerText = "Generating news...";

  const res = await fetch("/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ topic })
  });

  const data = await res.json();
  output.innerText = data.article;
}
