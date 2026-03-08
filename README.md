Ниже улучшенная версия README v0.33.
Она включает:

архитектурные диаграммы Mermaid

формализованную FSM модель

пример Provider

пример Tool execution

уточнённые контракты слоёв

сохранение принципов Minimal Core Architecture


Готово для прямого сохранения как README.md.


---

🧬 MFDBA-Lite (v0.33-alpha)

MFDBA-Lite — это детерминированный оркестратор LLM-агентов, реализующий строгий цикл принятия решений на основе конечного автомата (FSM).

Главная цель проекта — построение минималистичного и предсказуемого ядра, которое:

детерминирует выполнение

изолирует взаимодействие с LLM

обеспечивает строгую типизацию

предотвращает архитектурный дрейф



---

🏗 Архитектурный манифест

MFDBA-Lite реализует Deterministic Execution Path.

1. Stateless Engine

Метод:

ExecutionEngine.step()

должен быть идемпотентной функцией:

StateContext → StateContext

движок не хранит состояние между вызовами.


---

2. Contract First Architecture

Система строится от контрактов, а не от реализаций.

Ключевые интерфейсы:

BaseProvider
ProviderResponse
ExecutionState
StateContext

Любая реализация обязана соблюдать контракт.


---

3. Canonical Data Model

В системе существует одна каноническая модель ответа LLM:

mfdballm.models.provider_response.ProviderResponse

Любые альтернативные структуры ответа запрещены.


---

4. Adapter Boundary

ExecutionEngine никогда не взаимодействует напрямую с Router.

Используется слой:

RouterAdapter

который:

нормализует ответы

восстанавливает ProviderResponse

предотвращает утечку типов



---

🧩 Архитектура системы

flowchart TD

Provider --> Router
Router --> RouterAdapter
RouterAdapter --> ExecutionEngine
ExecutionEngine --> Tools
Tools --> ExecutionEngine


---

🔧 Контракты компонентов

Компонент	Метод	Возвращаемый тип

Provider	chat()	ProviderResponse
Router	chat()	str
Router	achat()	str
RouterAdapter	call()	ProviderResponse
ExecutionEngine	run()	str



---

🚦 FSM модель

Система управляется функцией перехода:

\delta(S, E) \rightarrow S'

где:

 — текущее состояние

 — событие

 — следующее состояние



---

Состояния системы

Состояние	Назначение

INIT	старт системы
PLANNING	анализ ответа LLM
TOOL_EXECUTION	вызов инструментов
SUCCESS	финальный ответ
ERROR	аварийное завершение



---

Таблица переходов

S	E	S'

INIT	start	PLANNING
PLANNING	requires_tool	TOOL_EXECUTION
PLANNING	final_answer	SUCCESS
TOOL_EXECUTION	execution_done	PLANNING
ANY	max_iterations > 8	ERROR



---

FSM диаграмма

stateDiagram-v2

[*] --> INIT
INIT --> PLANNING

PLANNING --> TOOL_EXECUTION : requires_tool
PLANNING --> SUCCESS : final_answer

TOOL_EXECUTION --> PLANNING : execution_done

PLANNING --> ERROR : max_iterations
TOOL_EXECUTION --> ERROR : max_iterations


---

⚙️ Execution Engine

ExecutionEngine — детерминированный исполнитель FSM.

Основные свойства

Stateless

Idempotent

Async-safe

Deterministic



---

Основной цикл выполнения

INIT
  ↓
PLANNING
  ↓
TOOL_EXECUTION (optional)
  ↓
PLANNING
  ↓
SUCCESS


---

Ограничение итераций

max_iterations = 8

Это предотвращает бесконечные циклы reasoning.


---

🔧 Tool Execution

Инструменты вызываются через модель:

ToolCall

Перед выполнением инструмент сериализуется:

ToolCall → dict


---

Пример Tool

def add(a: int, b: int) -> int:
    return a + b


---

Пример ToolCall

ToolCall(
    name="add",
    arguments={
        "a": 2,
        "b": 3
    }
)


---

🤖 Provider интерфейс

Все LLM-провайдеры должны наследовать:

BaseProvider


---

Пример Provider

class ExampleProvider(BaseProvider):

    async def chat(self, messages, tools=None):

        return ProviderResponse(
            text="Hello from provider",
            tool_calls=[]
        )


---

🛠 Технические спецификации

Компонент	Версия

Python	3.10+
Validation	Pydantic v2
Async runtime	asyncio
Context window	32768 tokens



---

🧪 Тестирование

Целевое состояние тестов:

21 passed
0 failed

Покрытие включает:

Router fallback

Provider адаптацию

FSM transitions

Tool execution

Timeout isolation



---

⚠️ Архитектурные ограничения

Запрещено

❌ Возвращать dict из Router
❌ Использовать альтернативные модели ProviderResponse
❌ Нарушать FSM контракт
❌ Мутировать StateContext


---

Разрешено

✅ Добавлять новых Provider
✅ Расширять Tool систему
✅ Добавлять Middleware в Router


---

🤖 Инструкция для LLM

При модификации MFDBA-Lite:

Использовать только

mfdballm.execution.state.ExecutionState


---

Метод step должен быть идемпотентным

StateContext → StateContext


---

Использовать каноническую модель ответа

ProviderResponse


---

Использовать LaTeX для формальных описаний


---

📊 Текущий статус проекта

Метрика	Значение

Версия	v0.33-alpha
Completion	46%
Статус	Core Architecture Stabilization



---

Основная цель текущего этапа

Stabilize Router / Adapter / ExecutionEngine contracts


---

💡 Следующий архитектурный этап:

Provider Health Monitoring
↓
Dynamic Provider Pool
↓
Adaptive Routing


---
