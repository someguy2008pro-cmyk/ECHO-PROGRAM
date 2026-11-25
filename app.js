
const form = document.getElementById("chatForm");
const input = document.getElementById("messageInput");
const messages = document.getElementById("messages");

// Lưu lịch sử trên trình duyệt
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

// Phản hồi mô phỏng
function echoResponse(message) {
  const text = message.toLowerCase();

  if (text.includes("xin chào") || text.includes("hello")) {
    return "Xin chào. Tôi là ECHO. Rất vui được bắt đầu cuộc trò chuyện này.";
  }

  if (text.includes("bạn là ai") || text.includes("giới thiệu")) {
    return "Tôi là ECHO, một hệ thống AI đang trong quá trình xây dựng. Mục tiêu của dự án là phát triển một hệ thống nhất quán, minh bạch và có khả năng quản lý ký ức.";
  }

  if (text.includes("nguyên tắc")) {
    return "Những nguyên tắc cốt lõi của tôi gồm: trung thực, bảo vệ quyền riêng tư, minh bạch, phát triển có kiểm soát và không giả vờ có ý thức.";
  }

  if (text.includes("phát triển")) {
    return "Bước tiếp theo là hoàn thiện hệ thống lưu trữ, kiểm thử và sau đó mới tích hợp mô hình AI thực sự.";
  }

  return "Tôi đã nhận được tin nhắn của bạn. Hiện tại ECHO 0.3 chỉ sử dụng hệ thống phản hồi mô phỏng, chưa kết nối mô hình AI thực sự.";
}

// Gửi tin nhắn
form.addEventListener("submit", function(event) {
  event.preventDefault();

  const message = input.value.trim();

  if (!message) return;

  addMessage(message, "user");
  input.value = "";

  setTimeout(function() {
    const response = echoResponse(message);
    addMessage(response, "echo");
  }, 400);
});

// Khôi phục lịch sử
history.forEach(function(item) {
  addMessage(item.text, item.sender, false);
});
