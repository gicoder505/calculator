import tkinter as tk
from tkinter import messagebox
import math
import json
from datetime import datetime

class ScientificCalculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🧬 Научный калькулятор Pro")
        self.window.geometry("500x700")
        
        self.current_input = ""
        self.memory = 0
        self.history = []
        self.theme_dark = True
        self.last_result = None
        
        self.load_settings()
        self.create_widgets()
        self.setup_layout()
        self.apply_theme()
        
        self.setup_keyboard_shortcuts()
    
    def create_widgets(self):
    
        self.top_frame = tk.Frame(self.window, bg=self.get_color('frame_bg'))
        
        
        self.theme_btn = tk.Button(
            self.top_frame,
            text="🌙" if self.theme_dark else "☀️",
            font=('Arial', 14),
            command=self.toggle_theme,
            bg=self.get_color('button_bg'),
            fg=self.get_color('fg'),
            bd=0,
            relief=tk.FLAT,
            padx=10,
            pady=5
        )
        
        
        self.memory_label = tk.Label(
            self.top_frame,
            text=f"M: {self.memory:.2f}",
            font=('Arial', 12, 'bold'),
            bg=self.get_color('frame_bg'),
            fg=self.get_color('fg')
        )
        
        
        self.display = tk.Entry(
            self.window,
            font=('Consolas', 36, 'bold'),
            justify='right',
            bd=15,
            relief=tk.FLAT,
            bg=self.get_color('entry_bg'),
            fg=self.get_color('fg'),
            insertbackground='white'
        )
        
        
        self.basic_frame = tk.Frame(self.window, bg=self.get_color('frame_bg'))
        
        basic_buttons = [
            ('C', self.clear, '#FF6B6B'), 
            ('⌫', self.backspace, '#4ECDC4'), 
            ('%', self.percent, '#45B7D1'), 
            ('/', lambda: self.add_operation('/'), '#96CEB4'),
            ('7', lambda: self.add_number('7'), '#FFEAA7'), 
            ('8', lambda: self.add_number('8'), '#FFEAA7'), 
            ('9', lambda: self.add_number('9'), '#FFEAA7'), 
            ('×', lambda: self.add_operation('*'), '#96CEB4'),
            ('4', lambda: self.add_number('4'), '#FFEAA7'), 
            ('5', lambda: self.add_number('5'), '#FFEAA7'), 
            ('6', lambda: self.add_number('6'), '#FFEAA7'), 
            ('-', lambda: self.add_operation('-'), '#96CEB4'),
            ('1', lambda: self.add_number('1'), '#FFEAA7'), 
            ('2', lambda: self.add_number('2'), '#FFEAA7'), 
            ('3', lambda: self.add_number('3'), '#FFEAA7'), 
            ('+', lambda: self.add_operation('+'), '#96CEB4'),
            ('±', self.negate, '#4ECDC4'), 
            ('0', lambda: self.add_number('0'), '#FFEAA7'), 
            ('.', lambda: self.add_number('.'), '#4ECDC4'), 
            ('=', self.calculate, '#2ECC71')
        ]
        
        self.basic_buttons = []
        row, col = 0, 0
        
        for text, command, color in basic_buttons:
            btn = tk.Button(
                self.basic_frame,
                text=text,
                font=('Arial', 20, 'bold'),
                command=command,
                bg=color,
                fg='#2C3E50',
                activebackground='#BDC3C7',
                activeforeground='#2C3E50',  
                bd=0,
                relief=tk.FLAT,
                padx=15,
                pady=15
            )
            btn.grid(row=row, column=col, padx=3, pady=3, sticky='nsew')
            self.basic_buttons.append(btn)
            
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        
        self.scientific_frame = tk.Frame(self.window, bg=self.get_color('frame_bg'))
        
        scientific_buttons = [
            ('sin', self.sin_func, '#9B59B6'),
            ('cos', self.cos_func, '#9B59B6'),
            ('tan', self.tan_func, '#9B59B6'),
            ('π', self.add_pi, '#3498DB'),
            ('x²', self.square, '#E67E22'),
            ('√', self.square_root, '#E67E22'),
            ('xʸ', lambda: self.add_operation('^'), '#E67E22'),
            ('log', self.log10_func, '#9B59B6'),
            ('ln', self.ln_func, '#9B59B6'),
            ('e', self.add_e, '#3498DB'),
            ('(', lambda: self.add_number('('), '#3498DB'),
            (')', lambda: self.add_number(')'), '#3498DB'),
            ('M+', self.memory_add, '#1ABC9C'),
            ('MR', self.memory_recall, '#1ABC9C'),
            ('MC', self.memory_clear, '#E74C3C'),
            ('Ans', self.add_ans, '#F39C12')
        ]
        
        row, col = 0, 0
        for text, command, color in scientific_buttons:
            btn = tk.Button(
                self.scientific_frame,
                text=text,
                font=('Arial', 14, 'bold'),
                command=command,
                bg=color,
                fg='white',
                activebackground='#BDC3C7',
                activeforeground='#2C3E50',  
                bd=0,
                relief=tk.FLAT,
                padx=10,
                pady=10
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky='nsew')
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        
        self.converter_frame = tk.Frame(self.window, bg=self.get_color('frame_bg'), bd=2, relief=tk.GROOVE)
        
        
        tk.Label(
            self.converter_frame,
            text="Конвертер валют",
            font=('Arial', 12, 'bold'),
            bg=self.get_color('frame_bg'),
            fg=self.get_color('fg')
        ).grid(row=0, column=0, columnspan=4, pady=5)
        
        
        tk.Label(
            self.converter_frame, 
            text="Рубли:", 
            font=('Arial', 11),
            bg=self.get_color('frame_bg'),
            fg=self.get_color('fg')
        ).grid(row=1, column=0, padx=5, pady=5)
        
        self.rub_entry = tk.Entry(
            self.converter_frame, 
            width=12,
            font=('Arial', 11),
            bg=self.get_color('entry_bg'),
            fg=self.get_color('fg'),
            bd=2,
            relief=tk.SUNKEN
        )
        self.rub_entry.grid(row=1, column=1, padx=5, pady=5)
        self.rub_entry.insert(0, "100")
        
        tk.Label(
            self.converter_frame, 
            text="Доллары:", 
            font=('Arial', 11),
            bg=self.get_color('frame_bg'),
            fg=self.get_color('fg')
        ).grid(row=1, column=2, padx=5, pady=5)
        
        self.usd_label = tk.Label(
            self.converter_frame, 
            text="1.10",
            font=('Arial', 11, 'bold'),
            bg=self.get_color('frame_bg'),
            fg='#2ECC71'
        )
        self.usd_label.grid(row=1, column=3, padx=5, pady=5)
        
        tk.Label(
            self.converter_frame, 
            text="Евро:", 
            font=('Arial', 11),
            bg=self.get_color('frame_bg'),
            fg=self.get_color('fg')
        ).grid(row=2, column=0, padx=5, pady=5)
        
        self.eur_label = tk.Label(
            self.converter_frame, 
            text="0.92",
            font=('Arial', 11, 'bold'),
            bg=self.get_color('frame_bg'),
            fg='#2ECC71'
        )
        self.eur_label.grid(row=2, column=1, padx=5, pady=5)
        
        self.convert_btn = tk.Button(
            self.converter_frame,
            text="Конвертировать",
            font=('Arial', 11, 'bold'),
            command=self.convert_currency,
            bg='#3498DB',
            fg='white',
            activebackground='#2980B9',
            activeforeground='white',
            bd=0,
            relief=tk.FLAT,
            padx=10,
            pady=5
        )
        self.convert_btn.grid(row=2, column=2, columnspan=2, pady=5, padx=5, sticky='nsew')
        
        
        history_frame = tk.Frame(self.window, bg=self.get_color('frame_bg'))
        
        tk.Label(
            history_frame,
            text="📝 История вычислений:",
            font=('Arial', 12, 'bold'),
            bg=self.get_color('frame_bg'),
            fg=self.get_color('fg')
        ).pack(side=tk.LEFT, padx=5)
        
        clear_history_btn = tk.Button(
            history_frame,
            text="Очистить",
            font=('Arial', 10),
            command=self.clear_history,
            bg='#95A5A6',
            fg='white',
            activebackground='#7F8C8D',
            activeforeground='white',
            bd=0,
            relief=tk.FLAT
        )
        clear_history_btn.pack(side=tk.RIGHT, padx=5)
        
        self.history_frame = history_frame
        
        
        history_container = tk.Frame(self.window, bg=self.get_color('frame_bg'))
        
        scrollbar = tk.Scrollbar(history_container, orient=tk.VERTICAL)
        self.history_listbox = tk.Listbox(
            history_container,
            height=6,
            font=('Consolas', 10),
            bg=self.get_color('entry_bg'),
            fg=self.get_color('fg'),
            yscrollcommand=scrollbar.set,
            bd=2,
            relief=tk.SUNKEN
        )
        scrollbar.config(command=self.history_listbox.yview)
        
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_container = history_container
    
    def setup_layout(self):
        
        self.top_frame.pack(pady=10, padx=10, fill=tk.X)
        self.theme_btn.pack(side=tk.LEFT, padx=5)
        self.memory_label.pack(side=tk.RIGHT, padx=5)
        
        self.display.pack(pady=(0, 15), padx=15, fill=tk.X)
        
        self.basic_frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        self.scientific_frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        self.converter_frame.pack(pady=10, padx=10, fill=tk.X)
        
        self.history_frame.pack(pady=(10, 5), padx=10, fill=tk.X)
        self.history_container.pack(pady=(0, 10), padx=10, fill=tk.BOTH, expand=True)
        
        
        for i in range(5):
            self.basic_frame.grid_rowconfigure(i, weight=1)
            self.scientific_frame.grid_rowconfigure(i, weight=1)
            if i < 4:
                self.basic_frame.grid_columnconfigure(i, weight=1)
                self.scientific_frame.grid_columnconfigure(i, weight=1)
    
    def get_color(self, element):
        """Возвращает цвет в зависимости от темы"""
        if self.theme_dark:
            
            colors = {
                'bg': '#000000',           
                'fg': '#FFFFFF',           
                'entry_bg': '#1A1A1A',     
                'frame_bg': '#121212',     
                'button_bg': '#333333'     
            }
        else:
            
            colors = {
                'bg': '#F8F9FA',           
                'fg': '#212529',           
                'entry_bg': '#FFFFFF',     
                'frame_bg': '#E9ECEF',     
                'button_bg': '#DEE2E6'     
            }
        return colors.get(element, '#FFFFFF')
    
    def apply_theme(self):
        """Применяет текущую тему ко всем элементам"""
        
        self.theme_btn.configure(
            text="🌙" if self.theme_dark else "☀️",
            bg=self.get_color('button_bg'),
            fg=self.get_color('fg')
        )
        
        
        self.window.configure(bg=self.get_color('bg'))
        
        
        self.top_frame.configure(bg=self.get_color('frame_bg'))
        self.memory_label.configure(
            bg=self.get_color('frame_bg'),
            fg=self.get_color('fg')
        )
        
        
        self.display.configure(
            bg=self.get_color('entry_bg'),
            fg=self.get_color('fg')
        )
        
        
        self.basic_frame.configure(bg=self.get_color('frame_bg'))
        self.scientific_frame.configure(bg=self.get_color('frame_bg'))
        self.converter_frame.configure(bg=self.get_color('frame_bg'))
        self.history_frame.configure(bg=self.get_color('frame_bg'))
        self.history_container.configure(bg=self.get_color('frame_bg'))
        
        
        self.history_listbox.configure(
            bg=self.get_color('entry_bg'),
            fg=self.get_color('fg')
        )
        
        
        for widget in self.converter_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(
                    bg=self.get_color('frame_bg'),
                    fg=self.get_color('fg')
                )
            elif isinstance(widget, tk.Entry):
                widget.configure(
                    bg=self.get_color('entry_bg'),
                    fg=self.get_color('fg')
                )
        
        
        self.usd_label.configure(bg=self.get_color('frame_bg'))
        self.eur_label.configure(bg=self.get_color('frame_bg'))
        
        
        self.rub_entry.configure(
            bg=self.get_color('entry_bg'),
            fg=self.get_color('fg')
        )
        
        
        for btn in self.basic_buttons:
            if isinstance(btn, tk.Button):
                btn.configure(
                    activebackground='#BDC3C7',
                    activeforeground='#2C3E50'
                )
    
    def toggle_theme(self):
        """Переключает тему"""
        self.theme_dark = not self.theme_dark
        self.apply_theme()
        self.save_settings()
    
    def add_number(self, num):
        """Добавляет число на дисплей"""
        self.current_input += str(num)
        self.update_display()
    
    def add_operation(self, op):
        """Добавляет операцию"""
        
        if op == '×':
            op = '*'
        elif op == '^':
            op = '**'
        
        if self.current_input and self.current_input[-1] not in '+-*/^(':
            self.current_input += op
            self.update_display()
        elif op == '-':  
            self.current_input += op
            self.update_display()
    
    def update_display(self):
        """Обновляет дисплей"""
        
        display_text = self.current_input
        display_text = display_text.replace('**', '^')
        display_text = display_text.replace('*', '×')
        display_text = display_text.replace('/', '÷')
        
        self.display.delete(0, tk.END)
        self.display.insert(0, display_text)
    
    def clear(self):
        """Очищает дисплей"""
        self.current_input = ""
        self.update_display()
    
    def backspace(self):
        """Удаляет последний символ"""
        if self.current_input:
            self.current_input = self.current_input[:-1]
            self.update_display()
    
    def percent(self):
        """Процент"""
        try:
            result = self.safe_eval(self.current_input) / 100
            self.current_input = str(result)
            self.update_display()
        except:
            messagebox.showerror("Ошибка", "Некорректное выражение")
    
    def negate(self):
        """Меняет знак"""
        if self.current_input:
            try:
                value = self.safe_eval(self.current_input)
                self.current_input = str(-value)
                self.update_display()
            except:
                if self.current_input[0] == '-':
                    self.current_input = self.current_input[1:]
                else:
                    self.current_input = '-' + self.current_input
                self.update_display()
    
    def safe_eval(self, expression):
        """Безопасное вычисление выражения"""
        if not expression:
            return 0
            
        expr = expression.replace('×', '*').replace('÷', '/').replace('^', '**')
        
        
        expr = expr.replace('sin(', 'math.sin(math.radians(')
        expr = expr.replace('cos(', 'math.cos(math.radians(')
        expr = expr.replace('tan(', 'math.tan(math.radians(')
        expr = expr.replace('sqrt(', 'math.sqrt(')
        expr = expr.replace('log10(', 'math.log10(')
        expr = expr.replace('log(', 'math.log(')
        
        
        open_count = expr.count('math.sin(math.radians(') * 2 + \
                     expr.count('math.cos(math.radians(') * 2 + \
                     expr.count('math.tan(math.radians(') * 2 + \
                     expr.count('math.sqrt(') + \
                     expr.count('math.log10(') + \
                     expr.count('math.log(')
        
        close_count = expr.count(')')
        for _ in range(open_count - close_count):
            expr += ')'
        
        try:
            return eval(expr, {"__builtins__": {}}, {"math": math})
        except:
            raise ValueError("Некорректное выражение")
    
    def calculate(self):
        """Вычисляет результат"""
        try:
            if self.current_input:
                result = self.safe_eval(self.current_input)
                
                self.last_result = result
                
                timestamp = datetime.now().strftime("%H:%M:%S")
                history_entry = f"{self.current_input} = {result:.6g}"
                self.history_listbox.insert(0, f"{timestamp}: {history_entry}")
                
                if self.history_listbox.size() > 10:
                    self.history_listbox.delete(10, tk.END)
                
                self.current_input = str(result)
                self.update_display()
                
        except ZeroDivisionError:
            messagebox.showerror("Ошибка", "Деление на ноль невозможно!")
            self.clear()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка вычисления: {str(e)}")
    
    def clear_history(self):
        """Очищает историю"""
        self.history_listbox.delete(0, tk.END)
    
    
    def sin_func(self):
        """Синус"""
        self.current_input += "sin("
        self.update_display()
    
    def cos_func(self):
        """Косинус"""
        self.current_input += "cos("
        self.update_display()
    
    def tan_func(self):
        """Тангенс"""
        self.current_input += "tan("
        self.update_display()
    
    def add_pi(self):
        """Добавляет π"""
        self.current_input += str(math.pi)
        self.update_display()
    
    def square(self):
        """Возведение в квадрат"""
        self.current_input += "**2"
        self.update_display()
    
    def square_root(self):
        """Квадратный корень"""
        self.current_input += "sqrt("
        self.update_display()
    
    def log10_func(self):
        """Десятичный логарифм"""
        self.current_input += "log10("
        self.update_display()
    
    def ln_func(self):
        """Натуральный логарифм"""
        self.current_input += "log("
        self.update_display()
    
    def add_e(self):
        """Добавляет e"""
        self.current_input += str(math.e)
        self.update_display()
    
    def add_ans(self):
        """Добавляет последний ответ"""
        if self.last_result is not None:
            self.current_input += str(self.last_result)
            self.update_display()
    
    def memory_add(self):
        """Добавляет в память"""
        try:
            value = self.safe_eval(self.current_input)
            self.memory += value
            self.memory_label.config(text=f"M: {self.memory:.2f}")
        except:
            pass
    
    def memory_recall(self):
        """Вспоминает из памяти"""
        self.current_input += str(self.memory)
        self.update_display()
    
    def memory_clear(self):
        """Очищает память"""
        self.memory = 0
        self.memory_label.config(text=f"M: {self.memory:.2f}")
    
    def convert_currency(self):
        """Конвертирует валюту"""
        try:
            rub = float(self.rub_entry.get())
            usd_rate = 0.011
            eur_rate = 0.010
            
            self.usd_label.config(text=f"{rub * usd_rate:.2f}")
            self.eur_label.config(text=f"{rub * eur_rate:.2f}")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите число в рублях")
    
    def save_settings(self):
        """Сохраняет настройки"""
        settings = {
            'theme_dark': self.theme_dark,
            'memory': self.memory
        }
        try:
            with open('calculator_settings.json', 'w') as f:
                json.dump(settings, f)
        except:
            pass
    
    def load_settings(self):
        """Загружает настройки"""
        try:
            with open('calculator_settings.json', 'r') as f:
                settings = json.load(f)
                self.theme_dark = settings.get('theme_dark', True)
                self.memory = settings.get('memory', 0)
        except:
            pass
    
    def setup_keyboard_shortcuts(self):
        """Настраивает горячие клавиши"""
        self.window.bind('<Return>', lambda e: self.calculate())
        self.window.bind('<Escape>', lambda e: self.clear())
        self.window.bind('<BackSpace>', lambda e: self.backspace())
        
        for i in range(10):
            self.window.bind(str(i), lambda e, num=i: self.add_number(num))
        
        self.window.bind('+', lambda e: self.add_operation('+'))
        self.window.bind('-', lambda e: self.add_operation('-'))
        self.window.bind('*', lambda e: self.add_operation('*'))
        self.window.bind('/', lambda e: self.add_operation('/'))
        self.window.bind('.', lambda e: self.add_number('.'))
        self.window.bind('(', lambda e: self.add_number('('))
        self.window.bind(')', lambda e: self.add_number(')'))
    
    def run(self):
        """Запускает приложение"""
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()
    
    def on_closing(self):
        """Действия при закрытии"""
        self.save_settings()
        self.window.destroy()

if __name__ == "__main__":
    app = ScientificCalculator()
    app.run()