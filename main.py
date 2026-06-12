import os
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage, HumanMessage
from agent import tools
from dotenv import load_dotenv

load_dotenv()
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("Ключ GROQ_API_KEY не найден. Проверьте файл .env")

# 2. Инициализация LLM
llm = ChatGroq(model="llama-3.3-70b-versatile")

# 3. Инициализация агента (строго БЕЗ дополнительных аргументов, которые ломают код)
agent_executor = create_react_agent(llm, tools)

# 4. Сохраняем системную инструкцию в переменную
system_instruction = SystemMessage(content="""
Ты — профессиональный ИИ-ассистент страховой компании.
Твоя задача — помогать менеджерам, предоставляя точную информацию по клиентам и полисам.
ТЫ ОБЯЗАН использовать предоставленные инструменты (tools) для получения данных.
Отвечай вежливо и опирайся только на данные, полученные из инструментов.
""")

def run_agent():
    print("🤖 AI-Ассистент андеррайтера готов. (Введите 'exit' для выхода)")
    print("-" * 50)
    
    while True:
        user_input = input("Менеджер: ").strip()
        if not user_input:
            continue
            
        if user_input.lower() in ['exit', 'выход', 'quit']:
            break
            
        print("Агент думает...")
        
        try:
            # РЕШЕНИЕ: Передаем системную инструкцию и вопрос пользователя единым списком
            response = agent_executor.invoke({
                "messages": [
                    system_instruction, 
                    HumanMessage(content=user_input)
                ]
            })
            
            # Ответ лежит в последнем сообщении
            final_answer = response['messages'][-1].content
            print(f"🤖 Агент: {final_answer}\n")
            print("-" * 50)
            
        except Exception as e:
            print(f"⚠️ Ошибка: {e}")
            print("-" * 50)

if __name__ == "__main__":
    run_agent()