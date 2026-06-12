from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Corporate API Mock - КСЖ ГАК")

# 1. Имитация базы данных (Mock DB)
# В реальной жизни эти данные лежали бы в PostgreSQL или Oracle
MOCK_CLIENTS = {
    "850101400111": {"fullname": "Иванов Иван Иванович", "age": 39, "client_type": "VIP"},
    "900515300222": {"fullname": "Смагулова Айгерим Муратовна", "age": 34, "client_type": "Standard"},
}

MOCK_POLICIES = {
    "850101400111": [
        {
            "policy_number": "ГА-2024-55",
            "type": "Пенсионный аннуитет",
            "status": "Приостановлен",
            "reason": "Требуется актуализация удостоверения личности",
            "monthly_payout": 150000
        }
    ],
    "900515300222": [
        {
            "policy_number": "НС-2023-12",
            "type": "Страхование от несчастных случаев",
            "status": "Активен",
            "reason": "Оплачено",
            "monthly_payout": 0
        }
    ]
}

# 2. Создаем эндпоинты (API Routes)

@app.get("/api/clients/{iin}", summary="Получить профиль клиента по ИИН")
def get_client(iin: str):
    """Возвращает базовую информацию о клиенте."""
    client = MOCK_CLIENTS.get(iin)
    if not client:
        # Важно возвращать ошибку 404, чтобы ИИ-агент понимал, что такого клиента нет
        raise HTTPException(status_code=404, detail="Клиент с таким ИИН не найден")
    return {"iin": iin, **client}

@app.get("/api/policies/{iin}", summary="Получить список полисов клиента")
def get_policies(iin: str):
    """Возвращает все страховые полисы и аннуитеты клиента по его ИИН."""
    # Сначала проверяем, существует ли клиент вообще
    if iin not in MOCK_CLIENTS:
        raise HTTPException(status_code=404, detail="Клиент с таким ИИН не найден")
    
    policies = MOCK_POLICIES.get(iin, [])
    if not policies:
        return {"message": "У клиента нет активных договоров", "policies": []}
    
    return {"iin": iin, "policies": policies}