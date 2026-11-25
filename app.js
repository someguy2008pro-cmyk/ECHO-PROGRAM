
const form = document.getElementById("chatForm");
const input = document.getElementById("messageInput");
const messages = document.getElementById("messages");

const API_URL = "https://project-echo-47v2.onrender.com";

// Lưu lịch sử trò chuyện
let history = JSON.parse(
  localStorage.getItem("echo_history") || "[]"
);

// Hiển thị tin nhắn
function addMessage(text, sender, save = true) {
  const box = document.createElement("div");
  box.className = "message " + sender;

  const name = document.createElement("b");
  name.textContent = sender === "user" ? "BẠN" : "ECHO";

  const content = document.createElement("p");
  content.textContent = text;

  box.appendChild(name);
  box.appendChild(content);
  messages.appendChild(box);

  if (save) {
    history.push({ text, sender });
    localStorage.setItem(
      "echo_history",
      JSON.stringify(history)
    );
  }

  messages.scrollTop = messages.scrollHeight;
}

// Gửi tin nhắn đến Backend
async function sendToBackend(message) {
  const response = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message })
  });

  if (!response.ok) {
    throw new Error("Backend phản hồi lỗi.");
  }

  return await response.json();
}

// Xử lý gửi tin nhắn
form.addEventListener("submit", async function(event) {
  event.preventDefault();

  const message = input.value.trim();

  if (!message) return;

  addMessage(message, "user");
  input.value = "";

  const submitButton = form.querySelector(
    'button[type="submit"]'
  );

  if (submitButton) submitButton.disabled = true;

  try {
    const data = await sendToBackend(message);

    if (!data.response) {
      throw new Error("Không nhận được phản hồi.");
    }

    addMessage(data.response, "echo");

  } catch (error) {
    addMessage(
      "Hiện tại ECHO không thể kết nối Backend. Vui lòng thử lại sau.",
      "echo"
    );

  } finally {
    if (submitButton) submitButton.disabled = false;
    input.focus();
  }
});

// Khôi phục lịch sử trò chuyện
history.forEach(function(item) {
  addMessage(item.text, item.sender, false);
});
