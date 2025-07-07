import unittest
import json
import os
from unittest.mock import MagicMock, patch
from telegram import Update, CallbackQuery, Message, Chat, User
from telegram.ext import CallbackContext

# Добавляем родительскую директорию в PYTHONPATH
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import load_test, get_test_keyboard, handle_test_callback

class TestPersonalityTest(unittest.TestCase):
    def setUp(self):
        """Подготовка тестового окружения"""
        self.test_data = {
            "lesson_id": "test_personality_test",
            "title": "Тестовый тест",
            "blocks": [
                {
                    "block_id": 1,
                    "question": "Тестовый вопрос?",
                    "answers": [
                        {
                            "text": "Ответ 1",
                            "points": 1,
                            "next_block": 2
                        },
                        {
                            "text": "Ответ 2",
                            "points": 2,
                            "next_block": "result"
                        }
                    ]
                }
            ],
            "results": [
                {
                    "range": {"min": 1, "max": 1},
                    "title": "Результат 1",
                    "text": "Описание результата 1"
                },
                {
                    "range": {"min": 2, "max": 2},
                    "title": "Результат 2",
                    "text": "Описание результата 2"
                }
            ]
        }
        
        # Создаем тестовый файл
        with open('lessons/test_personality_test.json', 'w', encoding='utf-8') as f:
            json.dump(self.test_data, f, ensure_ascii=False)

    def tearDown(self):
        """Очистка после тестов"""
        if os.path.exists('lessons/test_personality_test.json'):
            os.remove('lessons/test_personality_test.json')

    def test_load_test(self):
        """Тест загрузки теста"""
        test = load_test('test_personality_test')
        self.assertIsNotNone(test)
        self.assertEqual(test['title'], "Тестовый тест")
        self.assertEqual(len(test['blocks']), 1)

    def test_get_test_keyboard(self):
        """Тест создания клавиатуры"""
        keyboard = get_test_keyboard(self.test_data['blocks'][0])
        self.assertIsNotNone(keyboard)
        self.assertEqual(len(keyboard.inline_keyboard), 2)

    @patch('main.TEST_DATA')
    async def test_handle_test_callback(self, mock_test_data):
        """Тест обработки ответа на тест"""
        # Подготовка тестовых данных
        mock_test_data['123'] = {
            'current_block': 0,
            'total_points': 0,
            'test_data': self.test_data
        }

        # Создаем мок-объекты
        update = MagicMock(spec=Update)
        context = MagicMock(spec=CallbackContext)
        query = MagicMock(spec=CallbackQuery)
        message = MagicMock(spec=Message)
        chat = MagicMock(spec=Chat)
        user = MagicMock(spec=User)

        # Настраиваем моки
        user.id = 123
        chat.id = 123
        message.chat = chat
        query.from_user = user
        query.message = message
        query.data = "test_1"
        update.callback_query = query

        # Вызываем тестируемую функцию
        await handle_test_callback(update, context)

        # Проверяем результаты
        self.assertEqual(mock_test_data['123']['total_points'], 1)
        self.assertEqual(mock_test_data['123']['current_block'], 0)

if __name__ == '__main__':
    unittest.main() 