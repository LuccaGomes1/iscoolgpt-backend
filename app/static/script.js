const form = document.getElementById("chat-form");
const input = document.getElementById("user-input");
const chatWindow = document.getElementById("chat-window");
const sendBtn = document.getElementById("send-btn");

function addMessage(text, sender = "bot") {
  const div = document.createElement("div");
  div.classList.add("message", sender);
  div.textContent = text;
  chatWindow.appendChild(div);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;

  // mensagem do usuário
  addMessage(text, "user");
  input.value = "";

  sendBtn.disabled = true;
  sendBtn.textContent = "Pensando...";

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: text, // <-- bate com o ChatRequest(message: str)
      }),
    });

    if (!response.ok) {
      throw new Error(`Erro da API: ${response.status}`);
    }

    const data = await response.json();
    const answer = data.answer || "[Resposta vazia do servidor]";
    addMessage(answer, "bot");
  } catch (err) {
    console.error(err);
    addMessage("❌ Erro ao falar com o servidor. Veja o console do navegador.", "bot");
  } finally {
    sendBtn.disabled = false;
    sendBtn.textContent = "Enviar";
  }
});
