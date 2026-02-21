import telebot
from telebot import TeleBot

from config import TOKEN
from database import Database
from keyboards import Keyboards

from handlers.comands import register_common_handlers
from handlers.tovar import register_catalog_handlers
from handlers.cart import register_cart_handlers
from handlers.admin import register_admin_handlers

# Инициализация бота и БД
bot = TeleBot(TOKEN)
db = Database()

# Хранилище данных пользователей
user_data = {}

# Регистрация всех обработчиков
register_common_handlers(bot)
register_catalog_handlers(bot, db, user_data)
register_cart_handlers(bot, user_data)
register_admin_handlers(bot, db, user_data)

# Обработчик навигации
@bot.callback_query_handler(func=lambda call: call.data in ['menu', 'back_admin'])
def navigation_callback(call):
    
    if call.data == 'menu':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(
            call.message.chat.id,
            'Главное меню:',
            reply_markup=Keyboards.main_menu()
        )
    elif call.data == 'back_admin':
        
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(
            call.message.chat.id,
            'Админ-панель:',
            reply_markup=Keyboards.admin_menu()
        )
    bot.answer_callback_query(call.id)

# Запуск бота
if __name__ == '__main__':
    print('🚀 Бот запущен!')
    bot.infinity_polling()