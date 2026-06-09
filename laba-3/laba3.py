import tkinter as tk
from tkinter import messagebox

class NumberSystemCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор систем счисления")
        self.root.geometry("450x550")
        self.root.resizable(False, False)
        
        self.current_base = 10
        self.first_num = None
        self.operation = None
        self.start_new_input = True
        self.disabled_chars = ""
        
        self.base_map = {"BIN": 2, "OCT": 8, "DEC": 10, "HEX": 16}
        
        self.create_widgets()
        self.update_button_states()

    def create_widgets(self):
        self.display = tk.Entry(self.root, font=("Arial", 20), justify="right", bd=10, insertwidth=4, bg="#ffffff")
        self.display.pack(fill="x", padx=10, pady=10)
        self.display.insert(0, "0")
        
        self.base_var = tk.StringVar(value="DEC")
        radio_frame = tk.LabelFrame(self.root, text="Система счисления", font=("Arial", 10))
        radio_frame.pack(fill="x", padx=10, pady=5)
        
        for base_name in self.base_map.keys():
            rb = tk.Radiobutton(radio_frame, text=base_name, variable=self.base_var, value=base_name,
                                font=("Arial", 11, "bold"), command=self.on_base_change)
            rb.pack(side="left", expand=True, pady=5)

        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        button_layout = [
            ('A', 0, 0), ('B', 0, 1), ('C', 0, 2), ('D', 0, 3), ('E', 0, 4), ('F', 0, 5),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('+', 1, 3), ('-', 1, 4), ('CLR', 1, 5),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3), ('/', 2, 4), (' ', 2, 5),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('=', 3, 3), (' ', 3, 4), ('0', 3, 5)
        ]
        
        for i in range(4): self.buttons_frame.rowconfigure(i, weight=1)
        for j in range(6): self.buttons_frame.columnconfigure(j, weight=1)
        
        self.btns = {}
        for text, row, col in button_layout:
            if text == ' ':
                continue
            
            if text in ['+', '-', '*', '/', '=']:
                bg_color = "#ff9500"
                fg_color = "#ffffff"
                active_bg = "#d67d00"
            elif text == 'CLR':
                bg_color = "#ff3b30"
                fg_color = "#ffffff"
                active_bg = "#b3241c"
            else:
                bg_color = "#e5e5ea"
                fg_color = "#000000"
                active_bg = "#d1d1d6"
                
            btn = tk.Button(self.buttons_frame, text=text, font=("Arial", 12, "bold"), 
                            bg=bg_color, fg=fg_color, bd=2,
                            activebackground=active_bg, activeforeground=fg_color,
                            command=lambda t=text: self.on_button_click(t))
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            self.btns[text] = btn

    # def execute_math_division(self, first_val, second_val):
    #     """Изолированное ядро вычислений для проведения Unit-тестирования"""
    #     if type(first_val) is not int or type(second_val) is not int:
    #         raise TypeError("Оба аргумента должны быть строго целыми числами типа int")
    #     if second_val == 0:
    #         raise ZeroDivisionError("Деление на ноль невозможно")
    #     return first_val // second_val


    # Шняга для ошибки
    def execute_math_division(self, first_val, second_val):
        if type(first_val) is not int or type(second_val) is not int:
            raise TypeError("Оба аргумента должны быть строго целыми числами типа int")
        if second_val == 0:
            raise ZeroDivisionError("Деление на ноль невозможно")
        return first_val * second_val


    def on_button_click(self, char):
        if char in self.disabled_chars:
            return

        current_text = self.display.get()
        
        if char == 'CLR':
            self.display.delete(0, tk.END)
            self.display.insert(0, "0")
            self.first_num = None
            self.operation = None
            self.start_new_input = True
            return
            
        if char in "0123456789ABCDEF":
            if self.start_new_input or current_text == "0" or current_text == "Ошибка" or current_text == "Деление на 0!":
                self.display.delete(0, tk.END)
                self.display.insert(0, char)
                self.start_new_input = False
            else:
                if len(current_text) < 15:
                    self.display.insert(tk.END, char)
            return

        if char in ['+', '-', '*', '/']:
            try:
                self.first_num = int(current_text, self.current_base)
                self.operation = char
                self.start_new_input = True
            except ValueError:
                self.show_error("Неверный ввод")
            return

        if char == '=':
            if not self.operation or self.first_num is None:
                return
            try:
                second_num = int(current_text, self.current_base)
                
                if self.operation == '+': 
                    result = self.first_num + second_num
                elif self.operation == '-': 
                    result = self.first_num - second_num
                elif self.operation == '*': 
                    result = self.first_num * second_num
                elif self.operation == '/': 
                    # Вызов безопасного изолированного ядра деления
                    result = self.execute_math_division(self.first_num, second_num)
                
                formatted_result = self.format_output(result, self.current_base)
                self.display.delete(0, tk.END)
                self.display.insert(0, formatted_result)
                
                self.first_num = None
                self.operation = None
                self.start_new_input = True
                
            except ZeroDivisionError:
                self.show_error("Деление на 0!")
            except ValueError:
                self.show_error("Ошибка вычислений")

    def on_base_change(self):
        new_base_name = self.base_var.get()
        new_base = self.base_map[new_base_name]
        current_text = self.display.get()
        
        if current_text and current_text not in ["Ошибка", "Деление на 0!"]:
            try:
                val_dec = int(current_text, self.current_base)
                converted_text = self.format_output(val_dec, new_base)
                self.display.delete(0, tk.END)
                self.display.insert(0, converted_text)
            except ValueError:
                self.display.delete(0, tk.END)
                self.display.insert(0, "0")
                
        self.current_base = new_base
        self.update_button_states()

    def update_button_states(self):
        for char in "0123456789ABCDEF":
            if char in self.btns:
                self.btns[char].config(bg="#e5e5ea", activebackground="#d1d1d6")
                
        if self.current_base == 2:
            self.disabled_chars = "23456789ABCDEF"
        elif self.current_base == 8:
            self.disabled_chars = "89ABCDEF"
        elif self.current_base == 10:
            self.disabled_chars = "ABCDEF"
        else:
            self.disabled_chars = ""
            
        for char in self.disabled_chars:
            if char in self.btns:
                self.btns[char].config(bg="#aeaeae", activebackground="#7a7a7a")

    def format_output(self, value, base):
        if value < 0:
            return "-" + self.format_output(abs(value), base)
            
        if base == 2: return bin(value)[2:].upper()
        if base == 8: return oct(value)[2:].upper()
        if base == 10: return str(value)
        if base == 16: return hex(value)[2:].upper()
        return "0"

    def show_error(self, message):
        self.display.delete(0, tk.END)
        self.display.insert(0, message)
        messagebox.showerror("Ошибка операции", message)
        self.start_new_input = True

if __name__ == "__main__":
    root = tk.Tk()
    app = NumberSystemCalculator(root)
    root.mainloop()