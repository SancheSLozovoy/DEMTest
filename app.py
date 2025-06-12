import tkinter as tk
from ui.main import MainFrame
from ui.material import EditFrame
from ui.supply import SupplyFrame


class MaterialApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Учет материалов - Мозаика")
        self.geometry("1200x960")
        self.configure(bg="#FFFFFF")

        # Иконка приложения
        try:
            self.iconbitmap('resources/icon.ico')
        except Exception:
            pass

        self.current_frame = None
        self.show_main_frame()

    def show_main_frame(self):
        """Показать главное окно со списком материалов"""
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = MainFrame(self)
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        self.title("Учет материалов - Мозаика")


    def show_edit_frame(self, material_id=None):
        """Показать окно редактирования/добавления материала"""
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = EditFrame(self, material_id)
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        title = "Редактирование материала" if material_id else "Добавление материала"
        self.title(f"Учет материалов - Мозаика | {title}")


    def show_supply_frame(self, material_id=None):
        """Показать окно поставщиков"""
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = SupplyFrame(self, material_id)
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        self.title(f"Учет материалов - Мозаика | Поставщики")

