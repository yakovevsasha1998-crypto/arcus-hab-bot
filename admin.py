from telebot import TeleBot
from database import Database
from keyboards import Keyboards
from validators.validators import Validators
from config import ADMIN_PASSWORD

def register_admin_handlers(bot: TeleBot, db: Database, user_data: dict):
    """Регистрация обработчиков админ-панели"""
    
    @bot.message_handler(commands=['admin'])
    def admin_command(message):
        msg = bot.send_message(message.chat.id, '🔐 Введите пароль администратора:')
        bot.register_next_step_handler(msg, check_admin_password)
    
    def check_admin_password(message):
        try:
            password = int(message.text)
            if password == ADMIN_PASSWORD:
                bot.send_message(
                    message.chat.id, 
                    '✅ Пароль верный! Добро пожаловать в админ-панель.',
                    reply_markup=Keyboards.admin_menu()
                )
            else:
                bot.send_message(message.chat.id, '❌ Неверный пароль!')
        except ValueError:
            bot.send_message(message.chat.id, '❌ Ошибка! Пароль должен быть числом.')
        except Exception as e:
            bot.send_message(message.chat.id, f'❌ Ошибка: {e}')
    
    @bot.message_handler(func=lambda message: message.text == '📦 Добавить товар')
    def add_product_start(message):
        user_id = message.from_user.id
        user_data[user_id] = {}
        
        msg = bot.send_message(message.chat.id, 'Введите НАЗВАНИЕ товара:')
        bot.register_next_step_handler(msg, get_product_name)
    
    def get_product_name(message):
        if message.text == '◀️ Выход' or message.text == '/start':
            from handlers.tovar import start_bot
            start_bot(message)
            return
        
        is_valid, result = Validators.validate_product_name(message.text)
        if not is_valid:
            bot.send_message(message.chat.id, f'❌ {result}')
            msg = bot.send_message(message.chat.id, 'Введите НАЗВАНИЕ товара:')
            bot.register_next_step_handler(msg, get_product_name)
            return
        
        user_id = message.from_user.id
        user_data[user_id]['name'] = result
        
        msg = bot.send_message(message.chat.id, 'Введите ЦЕНУ товара (только цифры):')
        bot.register_next_step_handler(msg, get_product_price)
    
    def get_product_price(message):
        if message.text == '◀️ Выход' or message.text == '/start':
            from handlers.tovar import start_bot
            start_bot(message)
            return
        
        is_valid, result = Validators.validate_price(message.text)
        if not is_valid:
            bot.send_message(message.chat.id, f'❌ {result}')
            msg = bot.send_message(message.chat.id, 'Введите ЦЕНУ товара:')
            bot.register_next_step_handler(msg, get_product_price)
            return
        
        user_id = message.from_user.id
        user_data[user_id]['price'] = result
        
        msg = bot.send_message(message.chat.id, 'Введите ЦВЕТ товара:')
        bot.register_next_step_handler(msg, get_product_color)
    
    def get_product_color(message):
        if message.text == '◀️ Выход' or message.text == '/start':
            from handlers.tovar import start_bot
            start_bot(message)
            return
        
        is_valid, result = Validators.validate_color(message.text)
        if not is_valid:
            bot.send_message(message.chat.id, f'❌ {result}')
            msg = bot.send_message(message.chat.id, 'Введите ЦВЕТ товара:')
            bot.register_next_step_handler(msg, get_product_color)
            return
        
        user_id = message.from_user.id
        user_data[user_id]['color'] = result
        
        try:
            db.add_product(
                user_data[user_id]['name'],
                user_data[user_id]['price'],
                user_data[user_id]['color']
            )
            
            bot.send_message(
                message.chat.id,
                f'✅ Товар успешно добавлен!\n\n'
                f'📦 Название: {user_data[user_id]["name"]}\n'
                f'💰 Цена: {user_data[user_id]["price"]} ₽\n'
                f'🎨 Цвет: {user_data[user_id]["color"]}'
            )
        except Exception as e:
            bot.send_message(message.chat.id, f'❌ Ошибка при сохранении: {e}')
        
        if user_id in user_data:
            del user_data[user_id]
        
        bot.send_message(
            message.chat.id,
            '👋 Возврат в админ-панель',
            reply_markup=Keyboards.admin_menu()
        )
    
    @bot.message_handler(func=lambda message: message.text == '📋 Список товаров')
    def list_products(message):
        products = db.get_all_products()
        
        if not products:
            bot.send_message(message.chat.id, '📭 Товаров пока нет')
        else:
            text = '📋 СПИСОК ТОВАРОВ:\n\n'
            for p in products:
                text += f'🆔 {p[0]}. {p[1]} - {p[2]} ₽ | {p[3]}\n'
            bot.send_message(message.chat.id, text)
    
    @bot.message_handler(func=lambda message: message.text == '🗑 Удалить товар')
    def delete_product_start(message):
        products = db.get_all_products()
        
        if not products:
            bot.send_message(message.chat.id, '📭 Нет товаров для удаления')
            return
        
        bot.send_message(
            message.chat.id, 
            "Выберите товар для удаления:", 
            reply_markup=Keyboards.delete_products_inline(products)
        )
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith('del_'))
    def delete_product_callback(call):
        product_id = int(call.data.split('_')[1])
        
        if db.delete_product(product_id):
            bot.answer_callback_query(call.id, "✅ Товар удален!")
            bot.edit_message_text(
                "✅ Товар успешно удален!",
                call.message.chat.id,
                call.message.message_id
            )
        else:
            bot.answer_callback_query(call.id, "❌ Товар не найден!")
        
        # Показываем обновленный список
        products = db.get_all_products()
        if products:
            bot.send_message(
                call.message.chat.id, 
                "Выберите товар для удаления:", 
                reply_markup=Keyboards.delete_products_inline(products)
            )
        else:
            bot.send_message(call.message.chat.id, "📭 Больше нет товаров для удаления")
    
    @bot.message_handler(func=lambda message: message.text == '◀️ Выход')
    def exit_admin(message):
        bot.send_message(
            message.chat.id, 
            '👋 Вы вышли из админ-панели', 
            reply_markup=Keyboards.main_menu()
        )