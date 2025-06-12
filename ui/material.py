import tkinter as tk
from tkinter import messagebox, ttk
from db import get_materials, get_material_types, update_material, add_material


class EditFrame(tk.Frame):
    def __init__(self, master, material_id=None):
        super().__init__(master, bg="#FFFFFF")
        self.master = master
        self.material_id = material_id
        self.is_edit = material_id is not None

        # Заголовок
        title = "Редактирование материала" if self.is_edit else "Добавление материала"
        header = tk.Label(self, text=title,
                          font=("Comic Sans MS", 18),
                          bg="#FFFFFF", fg="#546F94")
        header.pack(pady=10)

        # Основной фрейм для формы
        form_frame = tk.Frame(self, bg="#FFFFFF")
        form_frame.pack(pady=20)

        # Поля формы
        tk.Label(form_frame, text="Наименование:",
                 font=("Comic Sans MS", 12), bg="#FFFFFF").grid(row=0, column=0,
                                                                sticky="e", padx=5, pady=5)
        self.name_entry = tk.Entry(form_frame, font=("Comic Sans MS", 12), width=30)
        self.name_entry.grid(row=0, column=1, sticky="w", pady=5)

        tk.Label(form_frame, text="Тип материала:",
                 font=("Comic Sans MS", 12), bg="#FFFFFF").grid(row=1, column=0,
                                                                sticky="e", padx=5, pady=5)
        self.type_combobox = ttk.Combobox(form_frame, font=("Comic Sans MS", 12),
                                          width=27, state="readonly")
        self.type_combobox.grid(row=1, column=1, sticky="w", pady=5)

        tk.Label(form_frame, text="Количество на складе:",
                 font=("Comic Sans MS", 12), bg="#FFFFFF").grid(row=2, column=0,
                                                                sticky="e", padx=5, pady=5)
        self.stock_entry = tk.Entry(form_frame, font=("Comic Sans MS", 12), width=30)
        self.stock_entry.grid(row=2, column=1, sticky="w", pady=5)

        tk.Label(form_frame, text="Единица измерения:",
                 font=("Comic Sans MS", 12), bg="#FFFFFF").grid(row=3, column=0,
                                                                sticky="e", padx=5, pady=5)
        self.unit_entry = tk.Entry(form_frame, font=("Comic Sans MS", 12), width=30)
        self.unit_entry.grid(row=3, column=1, sticky="w", pady=5)

        tk.Label(form_frame, text="Количество в упаковке:",
                 font=("Comic Sans MS", 12), bg="#FFFFFF").grid(row=4, column=0,
                                                                sticky="e", padx=5, pady=5)
        self.package_entry = tk.Entry(form_frame, font=("Comic Sans MS", 12), width=30)
        self.package_entry.grid(row=4, column=1, sticky="w", pady=5)

        tk.Label(form_frame, text="Минимальное количество:",
                 font=("Comic Sans MS", 12), bg="#FFFFFF").grid(row=5, column=0,
                                                                sticky="e", padx=5, pady=5)
        self.min_entry = tk.Entry(form_frame, font=("Comic Sans MS", 12), width=30)
        self.min_entry.grid(row=5, column=1, sticky="w", pady=5)

        tk.Label(form_frame, text="Цена за единицу:",
                 font=("Comic Sans MS", 12), bg="#FFFFFF").grid(row=6, column=0,
                                                                sticky="e", padx=5, pady=5)
        self.price_entry = tk.Entry(form_frame, font=("Comic Sans MS", 12), width=30)
        self.price_entry.grid(row=6, column=1, sticky="w", pady=5)

        # Кнопки
        btn_frame = tk.Frame(self, bg="#FFFFFF")
        btn_frame.pack(pady=20)

        btn_save = tk.Button(btn_frame, text="Сохранить",
                             font=("Comic Sans MS", 12),
                             bg="#546F94", fg="white",
                             command=self.save_material)
        btn_save.pack(side="left", padx=10)

        btn_cancel = tk.Button(btn_frame, text="Отмена",
                               font=("Comic Sans MS", 12),
                               bg="#ABCFCE",
                               command=lambda: self.master.show_main_frame())
        btn_cancel.pack(side="left", padx=10)

        self.load_material_types()

        # Загрузка данных для редактирования
        if self.is_edit:
            self.load_material_data()


    def load_material_types(self):
        try:
            types = get_material_types()
            self.type_combobox['values'] = [t['material_type'] for t in types]
            if types:
                self.type_combobox.current(0)
        except Exception as e:
            messagebox.showerror("Ошибка",
                                 f"Не удалось загрузить типы материалов:\n{str(e)}")

    def load_material_data(self):
        try:
            materials = get_materials()
            material = next((m for m in materials if m['id'] == self.material_id), None)

            if not material:
                raise Exception("Материал не найден")

            self.name_entry.insert(0, material['material_name'])
            self.stock_entry.insert(0, str(material['quantity_in_stock']))
            self.unit_entry.insert(0, material['unit'])
            self.package_entry.insert(0, str(material['package_quantity']))
            self.min_entry.insert(0, str(material['min_quantity']))
            self.price_entry.insert(0, f"{material['unit_price']:.2f}")

            print(self.type_combobox['values'])
            # Установка типа материала
            if material['type_name'] in self.type_combobox['values']:

                index = self.type_combobox['values'].index(material['type_name'])
                self.type_combobox.current(index)

        except Exception as e:
            messagebox.showerror("Ошибка",
                                 f"Не удалось загрузить данные материала:\n{str(e)}")
            self.master.show_main_frame()

    def validate_fields(self):
        """Проверка валидности полей формы"""
        errors = []

        if not self.name_entry.get().strip():
            errors.append("Не указано наименование материала")

        try:
            stock = float(self.stock_entry.get())
            if stock < 0:
                errors.append("Количество на складе не может быть отрицательным")
        except ValueError:
            errors.append("Некорректное значение количества на складе")

        if not self.unit_entry.get().strip():
            errors.append("Не указана единица измерения")

        try:
            package = int(self.package_entry.get())
            if package <= 0:
                errors.append("Количество в упаковке должно быть положительным числом")
        except ValueError:
            errors.append("Некорректное значение количества в упаковке")

        try:
            min_qty = float(self.min_entry.get())
            if min_qty < 0:
                errors.append("Минимальное количество не может быть отрицательным")
        except ValueError:
            errors.append("Некорректное значение минимального количества")

        try:
            price = float(self.price_entry.get())
            if price <= 0:
                errors.append("Цена должна быть положительным числом")
        except ValueError:
            errors.append("Некорректное значение цены")

        if not self.type_combobox.get().strip():
            errors.append("Не выбран тип материала")

        return errors

    def save_material(self):
        """Сохранение материала в БД"""
        errors = self.validate_fields()
        if errors:
            messagebox.showerror("Ошибка ввода",
                                 "Обнаружены следующие ошибки:\n\n• " + "\n• ".join(errors))
            return

        try:
            material_data = {
                'material_name': self.name_entry.get().strip(),
                'type_name': self.type_combobox.get(),
                'quantity_in_stock': float(self.stock_entry.get()),
                'unit': self.unit_entry.get().strip(),
                'package_quantity': int(self.package_entry.get()),
                'min_quantity': float(self.min_entry.get()),
                'unit_price': float(self.price_entry.get())
            }

            if self.is_edit:
                material_data['id'] = self.material_id
                update_material(material_data)
                messagebox.showinfo("Успешно", "Материал успешно обновлен")
            else:
                add_material(material_data)
                messagebox.showinfo("Успешно", "Материал успешно добавлен")

            self.master.show_main_frame()

        except Exception as e:
            messagebox.showerror("Ошибка",f"Не удалось сохранить материал:\n{str(e)}")