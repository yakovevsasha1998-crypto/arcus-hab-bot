from telebot import types

class Keyboards:
    @staticmethod
    def main_menu():
        """Главное меню"""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton('🛍 Каталог')
        btn2 = types.KeyboardButton('🛒 Корзина')
        btn3 = types.KeyboardButton('📞 Контакты')
        markup.add(btn1, btn2, btn3)
        return markup
    
    @staticmethod
    def admin_menu():
        """Меню администратора"""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton('📦 Добавить товар')
        btn2 = types.KeyboardButton('📋 Список товаров')
        btn3 = types.KeyboardButton('🗑 Удалить товар')
        btn4 = types.KeyboardButton('◀️ Выход')
        markup.add(btn1, btn2, btn3, btn4)
        return markup
    
    @staticmethod
    def products_inline(products):
        """Инлайн клавиатура с товарами"""
        markup = types.InlineKeyboardMarkup(row_width=1)
        for product in products:
            btn = types.InlineKeyboardButton(
                text=f"{product[1]} - {product[3]} - {product[2]} ₽",
                callback_data=f"p_{product[0]}"
            )
            markup.add(btn)
        return markup
    
    @staticmethod
    def cart_actions():
        """Кнопки для корзины"""
        markup = types.InlineKeyboardMarkup(row_width=2)
        clear_btn = types.InlineKeyboardButton("🗑 Очистить корзину", callback_data="clear")
        order_btn = types.InlineKeyboardButton("📦 Оформить предзаказ", callback_data="order")
        markup.add(clear_btn, order_btn)
        return markup
    
    @staticmethod
    def back_button(callback_data='menu'):
        """Кнопка назад"""
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton('◀️ Назад', callback_data=callback_data)
        markup.add(btn)
        return markup
    
    @staticmethod
    def delete_products_inline(products):
        """Инлайн клавиатура для удаления товаров"""
        markup = types.InlineKeyboardMarkup(row_width=1)
        for p in products:
            btn = types.InlineKeyboardButton(
                text=f"❌ {p[1]} - {p[2]} ₽ | {p[3]}",
                callback_data=f"del_{p[0]}"
            )
            markup.add(btn)
        
        back_btn = types.InlineKeyboardButton("◀️ Отмена", callback_data="back_admin")
        markup.add(back_btn)
        return markup
    
    @staticmethod
    def support_button():
        """Кнопка поддержки"""
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn = types.InlineKeyboardButton(
            text='📱 Написать в поддержку!', 
            url='https://t.me/Yashkin_1'
        )
        markup.add(btn)
        return markup
    
    @staticmethod
    def confirm_cart_item():
        """Кнопка подтверждения добавления в корзину"""
        markup = types.InlineKeyboardMarkup()
        confirm_btn = types.InlineKeyboardButton(
            "✅ Добавить в корзину", 
            callback_data="confirm_add"
        )
        markup.add(confirm_btn)
        return markup