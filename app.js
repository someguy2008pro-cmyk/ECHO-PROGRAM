const API_URL = "https://project-echo-47v2.onrender.com";

async function sendToBackend(message) {
  const response = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message })
  });

  if (!response.ok) {
    throw new Error("Backend connection failed");
  }

  return await response.json();
}
