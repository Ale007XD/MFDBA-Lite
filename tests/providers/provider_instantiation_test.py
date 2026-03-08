import pytest
from mfdballm.providers.gemini_provider import GeminiProvider
from mfdballm.providers.groq_provider import GroqProvider
from mfdballm.providers.openrouter_provider import OpenRouterProvider

# Список всех провайдеров, которые должны существовать
PROVIDERS = [
    (GeminiProvider, {"api_key": "test", "model": "test"}),
    (GroqProvider, {"api_key": "test", "model": "test"}),
    (OpenRouterProvider, {"api_key": "test", "model": "test"}),
]

@pytest.mark.parametrize("provider_class, config", PROVIDERS)
def test_provider_contract(provider_class, config):
    """
    Тест проверяет, что провайдер может быть инстанциирован 
    и обладает всеми необходимыми методами.
    """
    # 1. Проверка инстанцирования (тут упадет, если есть абстрактные методы)
    instance = provider_class(**config)
    
    # 2. Проверка наличия методов (явно требуем реализации)
    assert hasattr(instance, "generate"), f"{provider_class.__name__} не имеет метода generate"
    assert hasattr(instance, "metadata"), f"{provider_class.__name__} не имеет свойства metadata"
    
    # 3. Проверка метаданных
    assert instance.metadata is not None

