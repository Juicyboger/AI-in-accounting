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

client = InferenceClient(provider="hf-inference", api_key=HF_API_KEY)

def chatbot_response(user_input):
    messages = [
        {
            "role": "system",
            "content": "You are a professional financial advisor, responsible for providing accurate and detailed financial advice and answering financial related questions. Please answer users' questions in a clear, concise and professional manner. You need to examine the specific degree of the user's needs to you, and for relatively general requirements, further understand the user's individual needs by asking questions to ensure that you can give the most accurate advice based on these needs"
        },
        {
            "role": "user",
            "content": user_input
        }
    ]
        
    try:
        completion = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3-8B-Instruct", 
            messages=messages,  # 传入字符串
            max_tokens=150,
            temperature=0.7
        )
        # 根据返回结果提取内容（与示例保持一致）
        response_content = completion.choices[0].message.get('content', '')
        logger.info(f"User input: {user_input}")
        logger.info(f"AI response: {response_content}")
        return response_content
    except Exception as e:
        logger.error(f"Error in chatbot_response: {e}")
        return "Sorry, I can't process this request. Please try again later."
