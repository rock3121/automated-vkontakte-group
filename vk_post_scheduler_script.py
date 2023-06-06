import vk_api
import schedule
import time
import unittest
from unittest.mock import MagicMock, patch

# Класс VKAPIInteraction отвечает за взаимодействие с API ВКонтакте
class VKAPIInteraction:
    def __init__(self, group_id, access_token):
        """
        Инициализация класса VKAPIInteraction.

        :param group_id: Идентификатор группы ВКонтакте
        :param access_token: Токен для доступа к API ВКонтакте
        """
        self.group_id = group_id
        self.access_token = access_token
        self.vk_session = vk_api.VkApi(token=self.access_token)

    def post_content(self, content):
        """
        Публикация контента в группу ВКонтакте.

        :param content: Сообщение для публикации
        :return: True в случае успешной публикации, False в случае ошибки
        """
        try:
            self.vk_session.method('wall.post', {'owner_id': -self.group_id, 'message': content})
        except vk_api.ApiError as error_msg:
            print(error_msg)
            return False
        return True


def job(interaction, content):
    """
    Задача для публикации контента в группу ВКонтакте.

    :param interaction: Экземпляр класса VKAPIInteraction
    :param content: Сообщение для публикации
    """
    interaction.post_content(content)


# Создание экземпляра класса VKAPIInteraction
interaction = VKAPIInteraction('your_group_id', 'your_access_token')

# Настройка задачи на публикацию сообщения каждые 8 часов
schedule.every(8).hours.do(job, interaction, 'Hello, world!')

# Запуск бесконечного цикла для выполнения задачи
while True:
    schedule.run_pending()
    time.sleep(1)


class VKAPITest(unittest.TestCase):
    @patch('vk_api.VkApi')
    def test_post_content_success(self, mock_vk_api):
        # Создание экземпляра класса VKAPIInteraction для тестирования
        interaction = VKAPIInteraction('your_group_id', 'your_access_token')
        # Имитация успешного вызова метода API ВКонтакте
        interaction.vk_session.method.return_value = None

        # Вызов метода post_content с тестовым сообщением
        result = interaction.post_content('Test message')

        # Проверка, что метод вернул True и был вызван метод API ВКонтакте с правильными параметрами
        self.assertTrue(result)
        interaction.vk_session.method.assert_called_once_with('wall.post', {'owner_id': -interaction.group_id, 'message': 'Test message'})

    @patch('vk_api.VkApi')
    def test_post_content_failure(self, mock_vk_api):
        # Создание экземпляра класса VKAPIInteraction для тестирования
        interaction = VKAPIInteraction('your_group_id', 'your_access_token')
        error_msg = 'API error message'
        # Имитация вызова метода API ВКонтакте, приводящего к ошибке
        interaction.vk_session.method.side_effect = vk_api.ApiError(error_msg)

        # Вызов метода post_content с тестовым сообщением
        result = interaction.post_content('Test message')

        # Проверка, что метод вернул False и был вызван метод API ВКонтакте с правильными параметрами
        # Проверка, что сообщение об ошибке было выведено на экран
        self.assertFalse(result)
        interaction.vk_session.method.assert_called_once_with('wall.post', {'owner_id': -interaction.group_id, 'message': 'Test message'})
        print.assert_called_once_with(error_msg)

    @patch('vk_post_scheduler.VKAPIInteraction')
    def test_job(self, mock_interaction):
        # Создание макета экземпляра класса VKAPIInteraction
        interaction_instance = mock_interaction.return_value
        content = 'Test message'

        # Вызов функции job с макетом экземпляра класса VKAPIInteraction
        job(interaction_instance, content)

        # Проверка, что метод post_content был вызван с правильным аргументом
        interaction_instance.post_content.assert_called_once_with(content)


if __name__ == '__main__':
    unittest.main()
