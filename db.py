# db.py (обновленная версия)
import mysql.connector
from config import DB_CONFIG


def get_connection():
    """Создать и вернуть соединение с БД"""
    return mysql.connector.connect(**DB_CONFIG)


def get_materials():
    """Получить список всех материалов"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT m.id, \
                       mt.name AS type_name, \
                       m.name, \
                       m.min_quantity,
                       m.quantity_in_stock, \
                       m.cost, \
                       m.unit, \
                       m.packaging_quantity
                FROM materials m
                         JOIN material_types mt ON m.type_id = mt.id
                ORDER BY mt.name, m.name; \
                """
        cursor.execute(query)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        raise Exception(f"Ошибка при загрузке материалов: {err}")
    finally:
        cursor.close()
        conn.close()


def get_material_types():
    """Получить список типов материалов"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name FROM material_types ORDER BY name")
        return cursor.fetchall()
    except mysql.connector.Error as err:
        raise Exception(f"Ошибка при загрузке типов материалов: {err}")
    finally:
        cursor.close()
        conn.close()


def add_material(material_data):
    """Добавить новый материал"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Сначала получаем ID типа материала
        cursor.execute("SELECT id FROM material_types WHERE name = %s",
                       (material_data['type_name'],))
        type_id = cursor.fetchone()[0]

        query = """
                INSERT INTO materials
                (name, type_id, quantity_in_stock, unit, packaging_quantity,
                 min_quantity, cost)
                VALUES (%s, %s, %s, %s, %s, %s, %s) \
                """
        values = (
            material_data['name'],
            type_id,
            material_data['quantity_in_stock'],
            material_data['unit'],
            material_data['packaging_quantity'],
            material_data['min_quantity'],
            material_data['cost']
        )

        cursor.execute(query, values)
        conn.commit()
    except mysql.connector.Error as err:
        raise Exception(f"Ошибка при добавлении материала: {err}")
    finally:
        cursor.close()
        conn.close()


def update_material(material_data):
    """Обновить существующий материал"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Получаем ID типа материала
        cursor.execute("SELECT id FROM material_types WHERE name = %s",
                       (material_data['type_name'],))
        type_id = cursor.fetchone()[0]

        query = """
                UPDATE materials
                SET name               = %s,
                    type_id            = %s,
                    quantity_in_stock  = %s,
                    unit               = %s,
                    packaging_quantity = %s,
                    min_quantity       = %s,
                    cost               = %s
                WHERE id = %s \
                """
        values = (
            material_data['name'],
            type_id,
            material_data['quantity_in_stock'],
            material_data['unit'],
            material_data['packaging_quantity'],
            material_data['min_quantity'],
            material_data['cost'],
            material_data['id']
        )

        cursor.execute(query, values)
        conn.commit()
    except mysql.connector.Error as err:
        raise Exception(f"Ошибка при обновлении материала: {err}")
    finally:
        cursor.close()
        conn.close()