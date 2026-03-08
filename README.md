# 🧬 MFDBA-Lite (v0.31-alpha)

**MFDBA-Lite** — это детерминированный оркестратор для LLM-агентов, спроектированный по принципу «минималистичного ядра». Вместо неявных циклов проект использует строгую логику конечных автоматов (FSM).

---

## 🏗 Архитектурный манифест

Проект следует принципам **Deterministic Execution Path**:
1. **Stateless Engine**: `ExecutionEngine.step()` — это чистая функция перехода состояний.
2. **Contract First**: Провайдеры обязаны соблюдать интерфейс `ABC` и возвращать типизированные ответы.

---

## 🚦 Состояния Системы (FSM)

Логика управления описывается функцией перехода $\delta(S, E) \rightarrow S'$:

| Состояние (`S`) | Описание | Событие (`E`) | След. состояние (`S'`) |
| :--- | :--- | :--- | :--- |
| `INIT` | Точка входа | `start` | `PLANNING` |
| `PLANNING` | Анализ LLM | `requires_tool` | `TOOL_EXECUTION` |
| `PLANNING` | Анализ LLM | `final_answer` | `SUCCESS` |
| `TOOL_EXECUTION` | Вызов инструмента | `execution_done` | `PLANNING` |
| `ANY` | Превышение лимитов | `max_iterations > 8` | `ERROR` |

---

## 🛠 Технические спецификации и лимиты

* **Python:** 3.10+
* **Validation:** Pydantic v2
* **Max Iterations:** 8
* **Context Window:** 32768 tokens

---

## 🤖 Инструкция для LLM

> **IMPORTANT:** При модификации кода MFDBA-Lite:
> 1. Используй только `mfdballm.execution.state.ExecutionState` (Enum).
> 2. Метод `step()` должен быть идемпотентным (принимает `StateContext`, возвращает новый).
> 3. Математические формулы оформляй в LaTeX.

---

**Current Completion:** 35% | **Status:** Foundation Stabilization
