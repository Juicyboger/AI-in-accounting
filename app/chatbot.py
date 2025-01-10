from huggingface_hub import InferenceClient
import os

# 获取 Hugging Face API Token 从环境变量
HF_API_KEY = os.getenv('HF_API_KEY')
if not HF_API_KEY:
    raise ValueError("HF_API_KEY is not set in environment variables.")

client = InferenceClient(api_key=HF_API_KEY)

def chatbot_response(user_input):
    messages = [
        {
            "role": "user",
            "content": user_input
        }
    ]
    
    try:
        completion = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3-8B-Instruct",  # 确保你有访问权限，或者选择一个免费模型如 'gpt2'
            messages=messages,
            max_tokens=500
        )
        return completion.choices[0].message['content']
    except Exception as e:
        print(f"Error: {e}")
        return "抱歉，我无法处理这个请求。请稍后再试。"
