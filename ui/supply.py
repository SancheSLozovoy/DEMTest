import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from db import get_suppliers_by_material


class SupplyFrame(tk.Frame):
    def __init__(self, master, material_id=None):
        super().__init__(master, bg="#FFFFFF")
        self.master = master
        self.material_id = material_id

        # Логотип
        try:
            logo_img = Image.open('resources/logo.png')
            logo_img = logo_img.resize((150, 70), Image.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(self, image=self.logo_photo, bg="#FFFFFF")
            logo_label.image = self.logo_photo
            logo_label.pack(pady=10)
        except Exception:
            pass

        # Заголовок
        title = "Поставщики материала" if material_id else "Список поставщиков"
        header = tk.Label(self, text=title,
                          font=("Comic Sans MS", 18),
                          bg="#FFFFFF", fg="#546F94")
        header.pack(pady=5)

        # Кнопка назад
        btn_back = tk.Button(self, text="Назад",
                            font=("Comic Sans MS", 12),
                            bg="#546F94", fg="white",
                            command=lambda: self.master.show_main_frame())
        btn_back.pack(pady=10)

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

        self.load_suppliers()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def load_suppliers(self):
        try:
            suppliers = get_suppliers_by_material(self.material_id)
        except Exception as e:
            messagebox.showerror("Ошибка",
                               f"Не удалось загрузить поставщиков:\n{str(e)}")
            suppliers = []

        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        if not suppliers:
            text = "Нет поставщиков для этого материала" if self.material_id else "Нет данных о поставщиках"
            label = tk.Label(self.cards_frame, text=text,
                           font=("Comic Sans MS", 14), bg="#FFFFFF")
            label.pack(pady=50)
            return

        for supplier in suppliers:
            self.create_supplier_card(supplier)

    def create_supplier_card(self, supplier):
        card_bg = "#ABCFCE"
        accent_color = "#546F94"
        card = tk.Frame(self.cards_frame, bg=card_bg, bd=2, relief=tk.RIDGE)
        card.pack(fill=tk.X, pady=6, padx=5)

        font_main = ("Comic Sans MS", 12)
        font_bold = ("Comic Sans MS", 12, "bold")

        # Название поставщика
        name_label = tk.Label(card,
                            text=f"{supplier['supplier_type']} | {supplier['supplier_name']}",
                            font=font_bold, bg=card_bg, fg=accent_color)
        name_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=8, pady=2)

        # Основная информация
        tk.Label(card,
                text=f"ИНН: {supplier['inn']}",
                font=font_main, bg=card_bg).grid(row=1, column=0, sticky="w", padx=8)

        tk.Label(card,
                text=f"Дата начала работы: {supplier['start_date']}",
                font=font_main, bg=card_bg).grid(row=2, column=0, sticky="w", padx=8)

        # Рейтинг
        tk.Label(card,
                text=f"Рейтинг: {supplier['rating']}",
                font=font_bold, bg=card_bg, fg=accent_color).grid(row=1, column=1, sticky="e", padx=8)

        card.grid_columnconfigure(0, weight=1)
        card.grid_columnconfigure(1, weight=1)