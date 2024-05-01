import requests
# подтягиваем константы из config файла
from config import (MAX_GPT_TOKENS, IAM_TOKEN, FOLDER_ID)


# запрос к GPT
def ask_gpt(messages):
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
        'Content-Type': 'application/json'
    }
    out = [{"role": "user", "text": messages}]
    data = {
        'modelUri': f"gpt://{FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.7,
            "maxTokens": MAX_GPT_TOKENS
        },
        "messages": out  # добавляем к системному сообщению предыдущие сообщения
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        # проверяем статус код
        if response.status_code != 200:
            return False, f"Ошибка GPT. Статус код: {response.status_code}", None
        # если всё успешно - считаем кол-во токенов потраченных на ответ возвращаем: статус, ответ, токенов в ответе
        answer = response.json()['result']['alternatives'][0]['message']['text']
        return True, answer
    except Exception as e:
        return False, "Ошибка при обращение к GPT"

def count_tokens_in_dialog(messages, role):
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/tokenizeCompletion'
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
        'Content-Type': 'application/json'
    }
    out = [{"role": role, "text": messages}]
    data = {
       "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite/latest",
       "maxTokens": 100,
       "messages": out
    }
    print(requests.post(url=url, json=data, headers=headers).json())
    return len(requests.post(url=url, json=data, headers=headers).json()['tokens'])

