import openai

# OpenAI GPT-API 配置
openai.api_key = 'your_openai_api_key'

def chatbot_response(user_input):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"User: {user_input}\nAI:",
        max_tokens=150
    )
    return response.choices[0].text.strip()
