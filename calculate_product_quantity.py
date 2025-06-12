from decimal import Decimal, getcontext
from db import get_product_type_by_id, get_material_type_by_id


def calculate_product_quantity(product_type_id: int,
                               material_type_id: int,
                               material_amount: int,
                               param1: float,
                               param2: float) -> int:
    """
    Рассчитывает количество продукции, получаемой из заданного количества сырья.

    Параметры:
        product_type_id (int): ID типа продукции
        material_type_id (int): ID типа материала
        material_amount (int): Количество используемого сырья (целое число)
        param1 (float): Первый параметр продукции (вещественное положительное число)
        param2 (float): Второй параметр продукции (вещественное положительное число)

    Возвращает:
        int: Количество получаемой продукции или -1 при ошибке
    """
    # Устанавливаем точность вычислений
    getcontext().prec = 10

    # Проверка входных параметров
    if (material_amount <= 0 or
            param1 <= 0 or
            param2 <= 0 or
            not isinstance(material_amount, int)):
        return -1

    try:
        # Получаем данные о типе продукции
        product_type = get_product_type_by_id(product_type_id)
        if not product_type:
            return -1

        # Получаем данные о типе материала
        material_type = get_material_type_by_id(material_type_id)
        if not material_type:
            return -1

        # Конвертируем все значения в Decimal для точных вычислений
        material_amount_dec = Decimal(str(material_amount))
        param1_dec = Decimal(str(param1))
        param2_dec = Decimal(str(param2))
        product_coefficient = Decimal(str(product_type['coefficient']))
        loss_percentage = Decimal(str(material_type['loss_percentage'])) / Decimal('100')

        # Расчет сырья на единицу продукции
        material_per_unit = param1_dec * param2_dec * product_coefficient

        # Учет потерь - увеличиваем необходимое количество сырья
        effective_material_per_unit = material_per_unit / (Decimal('1') - loss_percentage)

        # Расчет количества продукции
        product_quantity = int(material_amount_dec / effective_material_per_unit)

        return product_quantity if product_quantity >= 0 else 0

    except Exception as e:
        print(f"Ошибка в расчетах: {str(e)}")
        return -1

quantity = calculate_product_quantity(
    product_type_id=1,
    material_type_id=1,
    material_amount=5,
    param1=1.5,
    param2=2.0
)

if quantity == -1:
    print("Ошибка в расчетах")
else:
    print(f"Можно произвести {quantity} единиц продукции")