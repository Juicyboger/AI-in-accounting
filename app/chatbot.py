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
    try:
        # 直接传入用户输入，不使用多条消息
        completion = client.text2text_generation.create(
            model="facebook/blenderbot-400M-distill",
            inputs=user_input,
            max_new_tokens=150,
            temperature=0.7
        )
        # 根据返回结构提取生成的文本（注意实际返回结构可能需要调整）
        response_content = completion[0]['generated_text']
        logger.info(f"User input: {user_input}")
        logger.info(f"AI response: {response_content}")
        return response_content
    except Exception as e:
        logger.error(f"Error in chatbot_response: {e}")
        return "Sorry, I can't process this request. Please try again later."
