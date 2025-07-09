import os
import requests
from dotenv import load_dotenv

load_dotenv()
PROXYAPI_KEY = os.getenv("PROXYAPI_KEY")

def test_proxyapi():
    if not PROXYAPI_KEY:
        print("❌ Не найден PROXYAPI_KEY в .env файле!")
        return

    url = "https://api.proxyapi.ru/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {PROXYAPI_KEY}"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Say 'Hello, world!'"}],
        "stream": False,
        "temperature": 0,
        "max_tokens": 10
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        if response.status_code == 200:
            data = response.json()
            print("✅ Успешно! Ответ модели:", data["choices"][0]["message"]["content"].encode('utf-8', errors='replace').decode('utf-8'))
        else:
            print(f"❌ Error! Status code: {response.status_code}")
            print("Ответ сервера:", response.text)
    except Exception as e:
        print(f"❌ Исключение при запросе: {e}")

if __name__ == "__main__":
    test_proxyapi()

