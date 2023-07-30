import requests
from pprint import pprint
import json

api_url = 'https://api.telegram.org/bot6348992336:AAFYCy0mXyAyZebEA9D9LkybeiCCOvHd8jQ/getUpdates'

response = requests.get(api_url)   # Отправляем GET-запрос и сохраняем ответ в переменной response

if response.status_code == 200:    # Если код ответа на запрос - 200, то смотрим, что пришло в ответе
    print(response.text)
else:
    print(response.status_code)    # При другом коде ответа выводим этот код