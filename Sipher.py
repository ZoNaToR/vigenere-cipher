import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
ALPHABETS = {
    "Русский": "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
    "English": "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
}
def vigenere_process(text: str, key: str, alphabet: str, encrypt: bool) -> str:
    if not key or not alphabet:
        return text
    key = ''.join(c.upper() for c in key if c.upper() in alphabet)
    if not key:
        return text
    result = []
    key_index = 0
    alphabet_len = len(alphabet)
    for char in text:
        upper_char = char.upper()
        if upper_char in alphabet:
            key_char = key[key_index % len(key)]
            shift = alphabet.index(key_char) 
            if encrypt:
                new_index = (alphabet.index(upper_char) + shift) % alphabet_len
            else:
                new_index = (alphabet.index(upper_char) - shift) % alphabet_len
            new_char = alphabet[new_index]
            if char.islower():
                new_char = new_char.lower()
            result.append(new_char)
            key_index += 1
        else:
            result.append(char)
    return ''.join(result)
class VigenereApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Шифратор Виженера — Русский + English")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        style = ttk.Style()
        style.theme_use('clam')
        self.language_var = tk.StringVar(value="Русский")
        self.create_widgets()
    def create_widgets(self):
        pad = 10
        title = ttk.Label(self.root, text="Шифратор и дешифратор Виженера", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        lang_frame = ttk.Frame(self.root)
        lang_frame.pack(fill="x", padx=pad, pady=5)
        ttk.Label(lang_frame, text="Язык алфавита:").pack(side="left")
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.language_var,
                                  values=["Русский", "English"], state="readonly", width=15)
        lang_combo.pack(side="left", padx=10)
        lang_combo.bind("<<ComboboxSelected>>", self.on_language_change)
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=pad, pady=pad)
        left_frame = ttk.LabelFrame(main_frame, text="Входные данные")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, pad//2))       
        ttk.Label(left_frame, text="Текст для обработки:").pack(anchor="w", padx=5, pady=(5,0))
        self.input_text = tk.Text(left_frame, height=12, wrap="word", font=("Arial", 11))
        self.input_text.pack(fill="both", expand=True, padx=5, pady=5)        
        ttk.Label(left_frame, text="Ключ:").pack(anchor="w", padx=5)
        self.key_entry = ttk.Entry(left_frame, font=("Arial", 11))
        self.key_entry.pack(fill="x", padx=5, pady=5)       
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill="x", padx=5, pady=5)       
        ttk.Button(btn_frame, text="Зашифровать →", command=self.encrypt).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="← Расшифровать", command=self.decrypt).pack(side="left", padx=5)      
        right_frame = ttk.LabelFrame(main_frame, text="Результат")
        right_frame.pack(side="right", fill="both", expand=True, padx=(pad//2, 0))       
        self.output_text = tk.Text(right_frame, height=12, wrap="word", font=("Arial", 11), state="disabled")
        self.output_text.pack(fill="both", expand=True, padx=5, pady=5)
        file_frame = ttk.Frame(self.root)
        file_frame.pack(fill="x", padx=pad, pady=10)       
        ttk.Button(file_frame, text="Загрузить текст из файла", command=self.load_file).pack(side="left", padx=5)
        ttk.Button(file_frame, text="Сохранить результат в файл", command=self.save_file).pack(side="left", padx=5)
        ttk.Button(file_frame, text="Поменять местами", command=self.swap_texts).pack(side="left", padx=5)
        ttk.Button(file_frame, text="Очистить всё", command=self.clear_all).pack(side="right", padx=5)      
        self.status_var = tk.StringVar(value="Готов к работе")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w")
        status_bar.pack(fill="x", padx=pad, pady=5)
    def get_current_alphabet(self):
        return ALPHABETS[self.language_var.get()]
    def get_other_language(self):
        return "English" if self.language_var.get() == "Русский" else "Русский"
    def validate_input(self, text: str, alphabet: str) -> bool:
        other_alphabet = ALPHABETS[self.get_other_language()]
        for char in text:
            upper = char.upper()
            if upper in other_alphabet:
                return False
        return True
    def on_language_change(self, event=None):
        self.clear_all()
        lang = self.language_var.get()
        self.status_var.set(f"Переключено на {lang} режим")    
    def encrypt(self):
        text = self.input_text.get("1.0", "end-1c")
        key = self.key_entry.get()
        alphabet = self.get_current_alphabet()
        lang = self.language_var.get()       
        if not text.strip():
            messagebox.showwarning("Предупреждение", "Введите текст!")
            return
        if not key.strip():
            messagebox.showwarning("Предупреждение", "Введите ключ!")
            return
        if not self.validate_input(text, alphabet):
            other = self.get_other_language()
            messagebox.showwarning(
                "Предупреждение о языке",
                f"В режиме «{lang}» обнаружены буквы другого языка ({other}).\n"
                f"Шифрование будет выполнено, но результат может быть некорректным.\n"
                f"Рекомендуется переключить режим или очистить текст."
            )
        result = vigenere_process(text, key, alphabet, encrypt=True)
        self.set_output(result)
        self.status_var.set(f"Зашифровано ({lang})")
    def decrypt(self):
        text = self.input_text.get("1.0", "end-1c")
        key = self.key_entry.get()
        alphabet = self.get_current_alphabet()
        lang = self.language_var.get()        
        if not text.strip():
            messagebox.showwarning("Предупреждение", "Введите текст!")
            return
        if not key.strip():
            messagebox.showwarning("Предупреждение", "Введите ключ!")
            return
        if not self.validate_input(text, alphabet):
            other = self.get_other_language()
            messagebox.showwarning(
                "Предупреждение о языке",
                f"В режиме «{lang}» обнаружены буквы другого языка ({other}).\n"
                f"Расшифрование будет выполнено, но результат может быть некорректным.\n"
                f"Рекомендуется переключить режим или очистить текст."
            )       
        result = vigenere_process(text, key, alphabet, encrypt=False)
        self.set_output(result)
        self.status_var.set(f"Расшифровано ({lang})")    
    def set_output(self, text: str):
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", text)
        self.output_text.config(state="disabled")   
    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Выберите текстовый файл",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        if not file_path:
            return
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.input_text.delete("1.0", "end")
            self.input_text.insert("1.0", content)
            self.status_var.set(f"Загружен: {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть файл:\n{str(e)}")  
    def save_file(self):
        content = self.output_text.get("1.0", "end-1c")
        if not content.strip():
            messagebox.showwarning("Предупреждение", "Результат пустой!")
            return
        file_path = filedialog.asksaveasfilename(
            title="Сохранить результат",
            defaultextension=".txt",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        if not file_path:
            return
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            self.status_var.set(f"Сохранено: {os.path.basename(file_path)}")
            messagebox.showinfo("Успех", "Файл успешно сохранён!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")
    def swap_texts(self):
        input_text = self.input_text.get("1.0", "end-1c")
        output_text = self.output_text.get("1.0", "end-1c")
        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", output_text)
        self.set_output(input_text)
        self.status_var.set("Тексты поменяны местами")
    def clear_all(self):
        self.input_text.delete("1.0", "end")
        self.set_output("")
        self.key_entry.delete(0, "end")
        self.status_var.set("Всё очищено")
if __name__ == "__main__":
    root = tk.Tk()
    app = VigenereApp(root)
    root.mainloop()
