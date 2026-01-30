import tkinter as tk
from tkinter import messagebox
import math
import json
from datetime import datetime

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🧮 Калькулятор Pro")
        self.window.geometry("400x550")
        
        self.current_input = ""
        self.last_result = None
        self.history = []
        self.theme_dark = True
        
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
        
        
        self.clear_history_btn = tk.Button(
            self.top_frame,
            text="🗑️",
            font=('Arial', 12),
            command=self.clear_history,
            bg=self.get_color('button_bg'),
            fg=self.get_color('fg'),
            bd=0,
            relief=tk.FLAT,
            padx=8
        )
        
        
        self.display = tk.Entry(
            self.window,
            font=('Consolas', 32, 'bold'),
            justify='right',
            bd=10,
            relief=tk.FLAT,
            bg=self.get_color('entry_bg'),
            fg=self.get_color('fg'),
            insertbackground='white'
        )
        
        
        self.buttons_frame = tk.Frame(self.window, bg=self.get_color('frame_bg'))
        
        
        buttons = [
            ('C', '#FF6B6B', self.clear), 
            ('⌫', '#45B7D1', self.backspace), 
            ('%', '#45B7D1', self.percent), 
            ('/', '#F39C12', lambda: self.add_operation('/')),
            
            ('7', self.get_button_color(), lambda: self.add_number('7')), 
            ('8', self.get_button_color(), lambda: self.add_number('8')), 
            ('9', self.get_button_color(), lambda: self.add_number('9')), 
            ('×', '#F39C12', lambda: self.add_operation('*')),
            
            ('4', self.get_button_color(), lambda: self.add_number('4')), 
            ('5', self.get_button_color(), lambda: self.add_number('5')), 
            ('6', self.get_button_color(), lambda: self.add_number('6')), 
            ('-', '#F39C12', lambda: self.add_operation('-')),
            
            ('1', self.get_button_color(), lambda: self.add_number('1')), 
            ('2', self.get_button_color(), lambda: self.add_number('2')), 
            ('3', self.get_button_color(), lambda: self.add_number('3')), 
            ('+', '#F39C12', lambda: self.add_operation('+')),
            
            ('±', '#45B7D1', self.negate), 
            ('0', self.get_button_color(), lambda: self.add_number('0')), 
            ('.', self.get_button_color(), lambda: self.add_number('.')), 
            ('=', '#2ECC71', self.calculate)
        ]
        
        self.button_widgets = []
        row, col = 0, 0
        
        for text, color, command in buttons:
            btn = tk.Button(
                self.buttons_frame,
                text=text,
                font=('Arial', 18, 'bold'),
                command=command,
                bg=color,
                fg=self.get_button_text_color(color),
                activebackground=self.get_active_bg_color(color),
                activeforeground=self.get_button_text_color(color),
                bd=0,
                relief=tk.FLAT,
                padx=20,
                pady=15
            )
            btn.grid(row=row, column=col, padx=3, pady=3, sticky='nsew')
            self.button_widgets.append(btn)
            
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        
        history_frame = tk.Frame(self.window, bg=self.get_color('frame_bg'))
        
        tk.Label(
            history_frame,
            text="📝 История:",
            font=('Arial', 11, 'bold'),
            bg=self.get_color('frame_bg'),
            fg=self.get_color('fg')
        ).pack(side=tk.LEFT, padx=5)
        
        self.history_frame = history_frame
        
        
        self.history_listbox = tk.Listbox(
            self.window,
            height=4,
            font=('Consolas', 9),
            bg=self.get_color('entry_bg'),
            fg=self.get_color('fg'),
            bd=2,
            relief=tk.SUNKEN
        )
    
    def setup_layout(self):
        
        self.top_frame.pack(pady=10, padx=10, fill=tk.X)
        self.theme_btn.pack(side=tk.LEFT, padx=5)
        self.clear_history_btn.pack(side=tk.RIGHT, padx=5)
        
        self.display.pack(pady=(0, 10), padx=15, fill=tk.X)
        self.buttons_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.history_frame.pack(pady=(10, 5), padx=10, fill=tk.X)
        self.history_listbox.pack(pady=(0, 10), padx=10, fill=tk.BOTH, expand=True)
        
        
        for i in range(5):
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.buttons_frame.grid_columnconfigure(i, weight=1)
    
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
                'bg': '#F0F0F0',           
                'fg': '#000000',           
                'entry_bg': '#FFFFFF',     
                'frame_bg': '#E8E8E8',     
                'button_bg': '#FFFFFF'     
            }
        return colors.get(element, '#FFFFFF')
    
    def get_button_color(self):
        """Возвращает цвет для кнопок с цифрами"""
        if self.theme_dark:
            return '#7F8C8D'  
        else:
            return '#FFFFFF'  
    
    def get_button_text_color(self, button_color):
        """Возвращает цвет текста для кнопки"""
        if button_color in ['#FF6B6B', '#45B7D1', '#F39C12', '#2ECC71']:
            return '#FFFFFF'  
        else:
            return '#000000' if not self.theme_dark else '#FFFFFF'
    
    def get_active_bg_color(self, button_color):
        """Возвращает цвет активной кнопки"""
        if button_color == '#FFFFFF':
            return '#E0E0E0'  
        elif button_color == '#7F8C8D':
            return '#95A5A6'  
        elif button_color == '#FF6B6B':
            return '#FF5252'  
        elif button_color == '#45B7D1':
            return '#5DADE2'  
        elif button_color == '#F39C12':
            return '#F7DC6F'  
        elif button_color == '#2ECC71':
            return '#58D68D'  
        else:
            return button_color
    
    def apply_theme(self):
        """Применяет текущую тему ко всем элементам"""
        
        self.theme_btn.configure(
            text="🌙" if self.theme_dark else "☀️",
            bg=self.get_color('button_bg'),
            fg=self.get_color('fg'),
            activebackground=self.get_active_bg_color(self.get_color('button_bg')),
            activeforeground=self.get_color('fg')
        )
        
        
        self.clear_history_btn.configure(
            bg=self.get_color('button_bg'),
            fg=self.get_color('fg'),
            activebackground=self.get_active_bg_color(self.get_color('button_bg')),
            activeforeground=self.get_color('fg')
        )
        
        
        self.window.configure(bg=self.get_color('bg'))
        
        
        self.top_frame.configure(bg=self.get_color('frame_bg'))
        
        
        self.display.configure(
            bg=self.get_color('entry_bg'),
            fg=self.get_color('fg')
        )
        
        
        self.buttons_frame.configure(bg=self.get_color('frame_bg'))
        self.history_frame.configure(bg=self.get_color('frame_bg'))
        
        
        self.history_listbox.configure(
            bg=self.get_color('entry_bg'),
            fg=self.get_color('fg')
        )
        
        
        for btn in self.button_widgets:
            text = btn.cget('text')
            current_color = btn.cget('bg')
            
            
            if text in ['C']:
                new_color = '#FF6B6B'
            elif text in ['⌫', '%', '±']:
                new_color = '#45B7D1'
            elif text in ['/', '×', '-', '+']:
                new_color = '#F39C12'
            elif text in ['=']:
                new_color = '#2ECC71'
            elif text in ['.']:
                new_color = self.get_button_color()
            elif text.isdigit() or text == '0':
                new_color = self.get_button_color()
            else:
                new_color = current_color
            
            btn.configure(
                bg=new_color,
                fg=self.get_button_text_color(new_color),
                activebackground=self.get_active_bg_color(new_color),
                activeforeground=self.get_button_text_color(new_color)
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
        
        if self.current_input and self.current_input[-1] not in '+-*/(':
            self.current_input += op
            self.update_display()
        elif op == '-':  
            self.current_input += op
            self.update_display()
    
    def update_display(self):
        """Обновляет дисплей"""
        
        display_text = self.current_input
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
            
        expr = expression.replace('×', '*').replace('÷', '/')
        
        try:
            
            allowed_chars = set('0123456789+-*/.() ')
            if not all(c in allowed_chars for c in expr):
                raise ValueError("Недопустимые символы")
            
            return eval(expr, {"__builtins__": {}}, {})
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
    
    def save_settings(self):
        """Сохраняет настройки"""
        settings = {
            'theme_dark': self.theme_dark
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
    
    def run(self):
        """Запускает приложение"""
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()
    
    def on_closing(self):
        """Действия при закрытии"""
        self.save_settings()
        self.window.destroy()

if __name__ == "__main__":
    app = Calculator()
    app.run()