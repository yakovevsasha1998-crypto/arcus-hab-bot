from telebot import TeleBot
from database import Database
from keyboards import Keyboards
from validators.validators import Validators

def register_catalog_handlers(bot: TeleBot, db: Database, user_data: dict):
    """Регистрация обработчиков каталога"""
    
    @bot.message_handler(func=lambda message: message.text == '🛍 Каталог')
    def catalog_handler(message):
        products = db.get_all_products()
        
        if not products:
            bot.send_message(message.chat.id, "😕 Товаров пока нет")
            return
        
        bot.send_message(
            message.chat.id, 
            "Наши товары:", 
            reply_markup=Keyboards.products_inline(products)
        )
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith('p_'))
    def product_callback(call):
        product_id = int(call.data.split('_')[1])
        product = db.get_product(product_id)
        
        if not product:
            bot.answer_callback_query(call.id, "Товар не найден!")
            return
        
        product_name, product_price, product_color = product
        
        user_id = call.from_user.id
        user_data[user_id] = {
            'temp_product': {
                'name': product_name,
                'price': product_price,
                'color': product_color
            }
        }
        
        size_hint = Validators.get_size_hint()
        msg = bot.send_message(
            call.message.chat.id,
            f"Товар: {product_name}\nЦвет: {product_color}\nЦена: {product_price} ₽\n\n"
            f"📏 Введите нужный вам РАЗМЕР:\n"
            f"Допустимые размеры: {size_hint}"
        )
        bot.register_next_step_handler(msg, get_size_from_user)
        bot.answer_callback_query(call.id)
    
    def get_size_from_user(message):
        # Проверка на выход в главное меню
        if message.text == '◀️ Выход' or message.text == '/start':
            # Импортируем здесь, чтобы избежать циклического импорта
            from handlers.tovar import start_bot
            start_bot(message)
            return
        
        user_id = message.from_user.id
        selected_size = message.text.upper().strip()
        
        if not Validators.validate_size(selected_size):
            size_hint = Validators.get_size_hint()
            bot.send_message(
                message.chat.id, 
                f"❌ Недопустимый размер '{selected_size}'!\n"
                f"📏 Допустимые размеры: {size_hint}\n"
                f"Примеры: S, M, L, XL, 42, 44, 46\n"
                f"Пожалуйста, введите размер еще раз:"
            )
            bot.register_next_step_handler(message, get_size_from_user)
            return
        
        if user_id not in user_data or 'temp_product' not in user_data[user_id]:
            bot.send_message(message.chat.id, "❌ Ошибка! Выберите товар заново.")
            catalog_handler(message)
            return
        
        product = user_data[user_id]['temp_product']
        
        text = f"""
✅ ВЫ ВЫБРАЛИ:

📦 {product['name']}
🎨 Цвет: {product['color']}
📏 Размер: {selected_size}
💰 Цена: {product['price']} ₽

Подтвердите добавление в корзину:
        """
        
        markup = Keyboards.confirm_cart_item()
        bot.send_message(message.chat.id, text, reply_markup=markup)
        
        # Сохраняем выбранный размер
        user_data[user_id]['selected_size'] = selected_size