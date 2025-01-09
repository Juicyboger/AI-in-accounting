document.getElementById('chat-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const userInput = document.getElementById('user-input').value;
    if (!userInput.trim()) return;

    // 显示用户消息
    const chatMessages = document.getElementById('chat-messages');
    const userMessage = document.createElement('div');
    userMessage.textContent = `You: ${userInput}`;
    chatMessages.appendChild(userMessage);

    // 发送到后端
    const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userInput })
    });

    const data = await response.json();

    // 显示机器人回复
    const botMessage = document.createElement('div');
    botMessage.textContent = `Bot: ${data.response}`;
    chatMessages.appendChild(botMessage);

    // 清空输入框
    document.getElementById('user-input').value = '';
    chatMessages.scrollTop = chatMessages.scrollHeight;
});
