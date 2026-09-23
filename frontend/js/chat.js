const API = "http://localhost:8000";
const userId = "user_" + Date.now();
const messagesDiv = document.getElementById("messages");

async function sendMsg() {
    const input = document.getElementById("userInput");
    const text = input.value.trim();
    if (!text) return;
    appendMessage("user", text);
    input.value = "";
    const loadingId = showLoading();

    try {
        const resp = await fetch(`${API}/api/chat/send`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: userId, message: text })
        });
        const data = await resp.json();
        removeLoading(loadingId);
        appendMessage("bot", data.reply);
        if (data.need_transfer) appendTransferAlert();
    } catch (err) {
        removeLoading(loadingId);
        appendMessage("bot", "⚠️ 服务连接异常，请稍后重试");
    }
}

function sendQuick(text) {
    document.getElementById("userInput").value = text;
    sendMsg();
}

function appendMessage(role, text) {
    const div = document.createElement("div");
    div.className = `message ${role === "user" ? "user" : "bot"}`;
    div.innerHTML = `<div class="msg-avatar">${role === "user" ? "👤" : "🤖"}</div><div class="msg-content">${escapeHtml(text)}</div>`;
    messagesDiv.appendChild(div);
    scrollToBottom();
}

function appendTransferAlert() {
    const div = document.createElement("div");
    div.className = "transfer-alert";
    div.textContent = "⚡ 已触发转人工，客服将稍后接入";
    messagesDiv.appendChild(div);
    scrollToBottom();
}

let loadingCounter = 0;
function showLoading() {
    const id = loadingCounter++;
    const div = document.createElement("div");
    div.className = "message bot";
    div.id = `loading-${id}`;
    div.innerHTML = `<div class="msg-avatar">🤖</div><div class="msg-content"><div class="typing"><span></span><span></span><span></span></div></div>`;
    messagesDiv.appendChild(div);
    scrollToBottom();
    return id;
}

function removeLoading(id) {
    const el = document.getElementById(`loading-${id}`);
    if (el) el.remove();
}

function scrollToBottom() { messagesDiv.scrollTop = messagesDiv.scrollHeight; }

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}
