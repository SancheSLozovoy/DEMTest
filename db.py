import pymysql
from config import DB_CONFIG


def get_connection():
    """Создать и вернуть соединение с БД"""
    return pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)


def get_materials():
    """Получить список всех материалов"""
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            query = """
                SELECT m.id,
                       mt.material_type AS type_name,
                       m.material_name,
                       m.min_quantity,
                       m.quantity_in_stock,
                       m.unit_price,
                       m.unit,
                       m.package_quantity
                FROM materials m
                         JOIN material_types mt ON m.material_type_id = mt.id
                ORDER BY mt.material_type, m.material_name
            """
            cursor.execute(query)
            return cursor.fetchall()
    except pymysql.MySQLError as err:
        raise Exception(f"Ошибка при загрузке материалов: {err}")
    finally:
        conn.close()


def get_suppliers_by_material(material_id=None):
    """Получить список поставщиков (для конкретного материала или всех)"""
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            if material_id:
                sql = """
                    SELECT s.*
                    FROM suppliers s
                             JOIN materials_suppliers ms ON s.id = ms.supplier_id
                    WHERE ms.material_id = %s
                """
                cursor.execute(sql, (material_id,))
            else:
                sql = "SELECT * FROM suppliers"
                cursor.execute(sql)
            return cursor.fetchall()
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()


def get_material_types():
    """Получить список типов материалов"""
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, material_type FROM material_types ORDER BY material_type")
            return cursor.fetchall()
    except pymysql.MySQLError as err:
        raise Exception(f"Ошибка при загрузке типов материалов: {err}")
    finally:
        conn.close()


def add_material(material_data):
    """Добавить новый материал"""
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM material_types WHERE material_type = %s",
                           (material_data['type_name'],))
            type_id = cursor.fetchone()['id']

            query = """
                INSERT INTO materials
                (material_name, material_type_id, quantity_in_stock, unit, package_quantity,
                 min_quantity, unit_price)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                material_data['material_name'],
                type_id,
                material_data['quantity_in_stock'],
                material_data['unit'],
                material_data['package_quantity'],
                material_data['min_quantity'],
                material_data['unit_price']
            )

            cursor.execute(query, values)
            conn.commit()
    except pymysql.MySQLError as err:
        raise Exception(f"Ошибка при добавлении материала: {err}")
    finally:
        conn.close()


def update_material(material_data):
    """Обновить существующий материал"""
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM material_types WHERE material_type = %s",
                           (material_data['type_name'],))
            type_id = cursor.fetchone()['id']

            query = """
                UPDATE materials
                SET material_name      = %s,
                    material_type_id   = %s,
                    quantity_in_stock  = %s,
                    unit               = %s,
                    package_quantity   = %s,
                    min_quantity       = %s,
                    unit_price         = %s
                WHERE id = %s
            """
            values = (
                material_data['material_name'],
                type_id,
                material_data['quantity_in_stock'],
                material_data['unit'],
                material_data['package_quantity'],
                material_data['min_quantity'],
                material_data['unit_price'],
                material_data['id']
            )

            cursor.execute(query, values)
            conn.commit()
    except pymysql.MySQLError as err:
        raise Exception(f"Ошибка при обновлении материала: {err}")
    finally:
        conn.close()


def get_product_type_by_id(product_type_id):
    """Получить тип продукции по ID"""
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM product_type WHERE id = %s", (product_type_id,))
            return cursor.fetchone()
    except Exception:
        return None
    finally:
        conn.close()


def get_material_type_by_id(material_type_id):
    """Получить тип материала по ID"""
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM material_types WHERE id = %s", (material_type_id,))
            return cursor.fetchone()
    except Exception:
        return None
    finally:
        conn.close()
