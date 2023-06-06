# Импортируем необходимые библиотеки
import json
import unittest
from abc import ABC, abstractmethod


# Создаем абстрактный базовый класс для взаимодействия с моделями
class ModelInteraction(ABC):

    @abstractmethod
    def configure_model(self, parameters):
        pass

    @abstractmethod
    def create_prompt(self, prompt):
        pass

    @abstractmethod
    def save_settings(self, settings):
        pass


# Реализуем класс ChatGPTInteraction, наследуя от ModelInteraction
class ChatGPTInteraction(ModelInteraction):

    def __init__(self, model):
        # Инициализация класса
        self.model = model  # Указываем модель, с которой будем работать

    def configure_model(self, parameters):
        """
        Настройка параметров модели.
        В данном случае мы просто сохраняем параметры в атрибут класса.
        """
        self.parameters = parameters

    def create_prompt(self, prompt):
        """
        Создание промпта для модели.
        Мы проверяем, что промпт является строкой, и сохраняем его в атрибуте класса.
        """
        assert isinstance(prompt, str), "Промпт должен быть строкой"
        self.prompt = prompt

    def save_settings(self, settings):
        """
        Сохранение настроек промпта и параметров.
        Мы сохраняем эти настройки в файл JSON.
        """
        with open('settings.json', 'w') as f:
            json.dump(settings, f)


# Создаем класс TestChatGPTInteraction для тестирования нашего основного класса
class TestChatGPTInteraction(unittest.TestCase):

    def setUp(self):
        """
        Метод setUp выполняется перед каждым тестом.
        Здесь мы создаем экземпляр класса ChatGPTInteraction.
        """
        self.interaction = ChatGPTInteraction("text-davinci-002")

    def test_configure_model(self):
        """
        Тестирование функции настройки модели.
        Мы устанавливаем параметры и проверяем, что они были корректно установлены.
        """
        parameters = {"max_tokens": 100}
        self.interaction.configure_model(parameters)
        self.assertEqual(self.interaction.parameters, parameters)

    def test_create_prompt(self):
        """
        Тестирование функции создания промпта.
        Мы устанавливаем промпт и проверяем, что он был корректно установлен.
        """
        prompt = "Hello, world!"
        self.interaction.create_prompt(prompt)
        self.assertEqual
