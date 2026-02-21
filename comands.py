from telebot import TeleBot
from keyboards import Keyboards
from config import CONTACTS_TEXT

def register_common_handlers(bot: TeleBot):
    """Регистрация общих обработчиков"""
    
    @bot.message_handler(commands=['start'])
    def start_bot(message):
        try:
            bot.send_message(
                message.chat.id, 
                '👋 Добро пожаловать в ARCUS HAB!\nВыберите действие:',
                reply_markup=Keyboards.main_menu()
            )
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Произошла ошибка: {e}")
    
    @bot.message_handler(func=lambda message: message.text == '📞 Контакты')
    def contacts_handler(message):
        bot.send_message(
            message.chat.id, 
            CONTACTS_TEXT, 
            reply_markup=Keyboards.back_button('menu')
        )