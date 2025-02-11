from huggingface_hub import InferenceClient
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 从环境变量中读取 Hugging Face API Token
HF_API_KEY = os.getenv('HF_API_KEY')
if not HF_API_KEY:
    raise ValueError("HF_API_KEY is not set in environment variables.")

# 初始化 InferenceClient，使用 'together' provider
client = InferenceClient(
    provider="together",
    api_key=HF_API_KEY
)

def chatbot_response(user_input):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a professional financial advisor, responsible for "
                "providing accurate and detailed financial advice and answering "
                "financial related questions. Please answer users' questions in "
                "a clear, concise and professional manner. You need to examine "
                "the specific degree of the user's needs to you, and for "
                "relatively general requirements, further understand the user's "
                "individual needs by asking questions to ensure that you can "
                "give the most accurate advice based on these needs. Please reply me in English."
            )
        },
        {
            "role": "user",
            "content": user_input
        }
    ]
    
    try:
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1",
            messages=messages,
            max_tokens=1500,   # 可根据需求进行调节
            temperature=0.7   # 可根据需求进行调节
        )
        # 从响应结果中获取聊天回复内容
        response_content = completion.choices[0].message.get('content', '')
        logger.info(f"User input: {user_input}")
        logger.info(f"AI response: {response_content}")
        return response_content
    except Exception as e:
        logger.error(f"Error in chatbot_response: {e}")
        return "Sorry, I can't process this request. Please try again later."