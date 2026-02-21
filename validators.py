from config import ALLOWED_SIZES, ADMIN_BUTTONS

class Validators:
    @staticmethod
    def validate_size(size):
        """Проверка размера"""
        return size.upper().strip() in ALLOWED_SIZES
    
    @staticmethod
    def validate_product_name(name):
        """Проверка названия товара"""
        if not name or len(name.strip()) < 2:
            return False, "Название должно содержать минимум 2 символа"
        if name.strip() in ADMIN_BUTTONS:
            return False, "Нельзя использовать название кнопки меню"
        return True, name.strip()
    
    @staticmethod
    def validate_price(price_str):
        """Проверка цены"""
        try:
            price = float(price_str.strip())
            if price <= 0:
                return False, "Цена должна быть больше 0"
            if price > 1000000:
                return False, "Цена слишком большая (максимум 1 000 000)"
            return True, price
        except ValueError:
            return False, "Введите корректное число"
    
    @staticmethod
    def validate_color(color):
        """Проверка цвета"""
        if not color or len(color.strip()) < 2:
            return False, "Цвет должен содержать минимум 2 символа"
        return True, color.strip()
    
    @staticmethod
    def get_size_hint():
        """Подсказка по размерам"""
        return ", ".join(ALLOWED_SIZES[:6]) + " и др."