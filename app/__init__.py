from huggingface_hub import InferenceClient
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 获取 Hugging Face API Token 从环境变量
HF_API_KEY = os.getenv('HF_API_KEY')
if not HF_API_KEY:
    raise ValueError("HF_API_KEY is not set in environment variables.")

client = InferenceClient(api_key=HF_API_KEY)

def chatbot_response(user_input):
    # 添加系统提示，设置模型角色为财务顾问
    messages = [
        {
            "role": "system",
            "content": "You are a professional financial advisor, responsible for providing accurate and detailed financial advice and answering financial related questions. Please answer users' questions in a clear, concise and professional manner."
        },
        {
            "role": "user",
            "content": user_input
        }
    ]
    
    try:
        # 使用适合聊天的模型，例如 'microsoft/DialoGPT-medium'
        completion = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3-8B-Instruct",  # 确保该模型支持中文并且你有访问权限
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        
        # 根据模型的响应结构提取内容
        response_content = completion.choices[0].message['content']
        
        logger.info(f"User input: {user_input}")
        logger.info(f"AI response: {response_content}")
        
        return response_content
    except Exception as e:
        logger.error(f"Error in chatbot_response: {e}")
        return "Sorry, I can't process this request. Please try again later."
