import requests
from langchain_core.tools import tool

# Базовый URL нашего FastAPI сервера
API_BASE_URL = "http://127.0.0.1:8000/api"

@tool
def get_client_info(iin: str) -> str:
    """
    Используй этот инструмент, чтобы получить базовую информацию о клиенте по его ИИН (например, ФИО или тип клиента).
    Входной параметр: iin (строка из 12 цифр).
    """
    try:
        response = requests.get(f"{API_BASE_URL}/clients/{iin}")
        if response.status_code == 200:
            data = response.json()
            return f"Найден клиент: {data['fullname']}, возраст: {data['age']}, статус: {data['client_type']}."
        elif response.status_code == 404:
            return "Клиент с таким ИИН не найден в базе данных."
        else:
            return f"Ошибка сервера: {response.status_code}"
    except Exception as e:
        return f"Ошибка подключения к корпоративному API: {str(e)}"

@tool
def get_client_policies(iin: str) -> str:
    """
    Используй этот инструмент для получения информации о страховых полисах, пенсионных аннуитетах и статусе их выплат по ИИН клиента.
    Входной параметр: iin (строка из 12 цифр).
    """
    try:
        response = requests.get(f"{API_BASE_URL}/policies/{iin}")
        if response.status_code == 200:
            data = response.json()
            policies = data.get("policies", [])
            if not policies:
                return "У клиента нет активных договоров."
            
            # Формируем читаемый ответ из списка полисов
            result = []
            for p in policies:
                result.append(f"Полис {p['policy_number']} ({p['type']}). Статус: {p['status']}. Причина: {p['reason']}.")
            return " | ".join(result)
        elif response.status_code == 404:
            return "Клиент с таким ИИН не найден в базе данных."
        else:
            return f"Ошибка сервера: {response.status_code}"
    except Exception as e:
        return f"Ошибка подключения к корпоративному API: {str(e)}"

# Собираем инструменты в список
tools = [get_client_info, get_client_policies]

# Тестовый запуск инструмента (чтобы убедиться, что код работает)
if __name__ == "__main__":
    print(get_client_info.invoke("850101400111"))