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

async function submitFeedback(button, rating) {
    const feedbackBlock = button.parentElement;
    const chatbotAnswerElement = feedbackBlock.parentElement.querySelector('.chatbot-answer');
    const answerText = chatbotAnswerElement ? chatbotAnswerElement.innerText : "";
    if (!answerText) {
        alert("无法获取答案内容");
        return;
    }
    
    try {
        const response = await fetch('/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ rating: rating, answer: answerText })
        });
        const result = await response.json();
        if (response.ok) {
            // 隐藏按钮区域，显示反馈已提交提示
            feedbackBlock.innerHTML = '<span class="feedback-msg text-success">你的反馈已提交</span>';
        } else {
            alert(result.error || '反馈提交失败');
        }
    } catch (error) {
        console.error('Feedback error:', error);
        alert('提交反馈时发生错误');
    }
}
