import tkinter as tk
from tkinter import messagebox
import keyboard
import time
import subprocess

class EpyktetoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Epykteto")
        self.root.geometry("300x100")
        
        self.label = tk.Label(root, text="Defina o horário (segundos):")
        self.label.pack()

        self.entry = tk.Entry(root)
        self.entry.pack()

        self.button = tk.Button(root, text="Confirmar", command=self.start_timer)
        self.button.pack()

        self.duration = 0  # Inicialize a duração como 0 no início

    def start_timer(self):
        try:
            self.duration = int(self.entry.get())
            self.root.attributes("-fullscreen", True)
            self.root.bind("<Key>", self.block_keyboard)
            self.start_time = time.time()
            self.save_start_time()
            self.root.after(self.duration * 1000, self.check_time)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um número válido.")

    def save_start_time(self):
        with open("start_time.txt", "w") as file:
            file.write(str(self.start_time))

    def load_start_time(self):
        try:
            with open("start_time.txt", "r") as file:
                return float(file.read())
        except FileNotFoundError:
            return None

    def check_time(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        if elapsed_time < self.duration:
            self.root.after(1000, self.check_time)
        else:
            self.root.attributes("-fullscreen", False)
            self.root.unbind("<Key>")
            messagebox.showinfo("Epykteto", "Tempo esgotado. Seu dispositivo não está mais bloqueado.")

    def block_keyboard(self, event):
        messagebox.showinfo("Bloqueado", "Você não pode usar o teclado enquanto o dispositivo estiver bloqueado.")
        subprocess.run(["shutdown", "/l"])  # Executa o comando 'shutdown /l' para fazer logout

    def check_previous_timer(self):
        start_time = self.load_start_time()
        if start_time is not None:
            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time < self.duration:
                self.root.attributes("-fullscreen", True)
                self.root.bind("<Key>", self.block_keyboard)
                self.start_time = start_time
                self.root.after(int((self.duration - elapsed_time) * 1000), self.check_time)

if __name__ == "__main__":
    root = tk.Tk()
    app = EpyktetoApp(root)
    app.check_previous_timer()
    root.mainloop()
