import sqlite3

class Database:
    def __init__(self, db_name='shop.db'):
        self.db_name = db_name
        self.init_db()
    
    def init_db(self):
        """Инициализация базы данных"""
        try:
            with self.get_connection() as conn:
                cur = conn.cursor()
                cur.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    color TEXT NOT NULL
                )
                ''')
                conn.commit()
            print("✅ База данных инициализирована")
        except Exception as e:
            print(f"❌ Ошибка при инициализации БД: {e}")
    
    def get_connection(self):
        """Получение соединения с БД"""
        return sqlite3.connect(self.db_name)
    
    def add_product(self, name, price, color):
        """Добавление товара"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO products (name, price, color) VALUES (?, ?, ?)",
                (name, price, color)
            )
            conn.commit()
            return cur.lastrowid
    
    def get_all_products(self):
        """Получение всех товаров"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute('SELECT id, name, price, color FROM products')
            return cur.fetchall()
    
    def get_product(self, product_id):
        """Получение товара по ID"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute('SELECT name, price, color FROM products WHERE id = ?', (product_id,))
            return cur.fetchone()
    
    def delete_product(self, product_id):
        """Удаление товара"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM products WHERE id = ?", (product_id,))
            conn.commit()
            return cur.rowcount > 0