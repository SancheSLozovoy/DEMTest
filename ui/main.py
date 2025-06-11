import tkinter as tk
from tkinter import messagebox
from math import ceil
from PIL import Image, ImageTk
from db import get_materials

class MainFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FFFFFF")
        self.master = master

        # Логотип
        try:
            logo_img = Image.open('resources/logo.ico')
            logo_img = logo_img.resize((150, 70), Image.ANTIALIAS)
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(self, image=self.logo_photo, bg="#FFFFFF")
            logo_label.pack(pady=10)
        except Exception:
            pass

        # Заголовок
        header = tk.Label(self, text="Список материалов",
                          font=("Comic Sans MS", 18),
                          bg="#FFFFFF", fg="#546F94")
        header.pack(pady=5)

        # Кнопка добавления
        btn_add = tk.Button(self, text="Добавить материал",
                            font=("Comic Sans MS", 12),
                            bg="#546F94", fg="white",
                            command=lambda: self.master.show_edit_frame())
        btn_add.pack(pady=10)

        # Прокручиваемый Canvas
        self.canvas = tk.Canvas(self, bg="#FFFFFF", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical",
                                      command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True,
                         padx=20, pady=10)

        # Фрейм для карточек
        self.cards_frame = tk.Frame(self.canvas, bg="#FFFFFF")
        self.canvas_frame = self.canvas.create_window((0, 0),
                                                      window=self.cards_frame,
                                                      anchor="nw")

        self.cards_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        self.load_materials()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def load_materials(self):
        try:
            materials = get_materials()
        except Exception as e:
            messagebox.showerror("Ошибка",
                                 f"Не удалось загрузить материалы:\n{str(e)}")
            materials = []

        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        if not materials:
            label = tk.Label(self.cards_frame, text="Нет данных о материалах",
                             font=("Comic Sans MS", 14), bg="#FFFFFF")
            label.pack(pady=50)
            return

        for material in materials:
            self.create_material_card(material)

    def create_material_card(self, material):
        card_bg = "#ABCFCE"
        accent_color = "#546F94"
        card = tk.Frame(self.cards_frame, bg=card_bg, bd=2, relief=tk.RIDGE)
        card.pack(fill=tk.X, pady=6, padx=5)

        card.bind("<Button-1>",
                        lambda e, id=material['id']: self.master.show_edit_frame(id))
        font_main = ("Comic Sans MS", 12)
        font_bold = ("Comic Sans MS", 12, "bold")

        # Название материала (кликабельно для редактирования)
        name_label = tk.Label(card,
                              text=f"{material['type_name']} | {material['name']}",
                              font=font_bold, bg=card_bg, fg=accent_color,
                              cursor="hand2")
        name_label.grid(row=0, column=0, sticky="w", padx=8, pady=2)

        # Основная информация
        tk.Label(card,
                 text=f"Минимальное количество: {material['min_quantity']} {material['unit']}",
                 font=font_main, bg=card_bg).grid(row=1, column=0, sticky="w", padx=8)

        tk.Label(card,
                 text=f"Количество на складе: {material['quantity_in_stock']} {material['unit']}",
                 font=font_main, bg=card_bg).grid(row=2, column=0, sticky="w", padx=8)

        tk.Label(card,
                 text=f"Цена: {material['cost']:.2f} / Единица измерения: {material['unit']}",
                 font=font_main, bg=card_bg).grid(row=3, column=0, sticky="w", padx=8)

        # Расчет стоимости минимальной партии
        cost_min_party = self.calculate_minimal_party_cost(material)
        tk.Label(card,
                 text=f"Стоимость партии: {cost_min_party:.2f}",
                 font=font_bold, bg=card_bg, fg=accent_color).grid(row=1, column=1,
                                                                   sticky="w", padx=8)

        card.grid_columnconfigure(0, weight=1)
        card.grid_columnconfigure(1, weight=1)

    def calculate_minimal_party_cost(self, material):
        quantity_in_stock = material['quantity_in_stock']
        min_quantity = material['min_quantity']
        packaging_quantity = material['packaging_quantity']
        cost = material['cost']

        if quantity_in_stock >= min_quantity:
            return 0.00

        difference = min_quantity - quantity_in_stock
        packs_needed = ceil(difference / packaging_quantity)
        minimal_qty = packs_needed * packaging_quantity
        total_cost = minimal_qty * cost
        return round(total_cost, 2)