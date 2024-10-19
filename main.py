import tkinter as tk
import time
import random
import keyboard
import mouse
import json
import os
from threading import Thread
import ctypes

class EpyktetoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Epykteto")
        self.root.geometry("300x200")
        self.root.overrideredirect(True)  # Remove a barra de título

        # Configura a janela para não aparecer na barra de tarefas
        self.root.attributes('-toolwindow', True)  

        self.lock_time = 0
        self.start_time = 0
        self.time_left = 0
        self.lock_active = False
        self.time_mode = tk.StringVar(value="seconds")
        self.phrases = [
            "Keep going, you got this!",
            "Focus on the task at hand.",
            "Discipline is freedom.",
            "Embrace the challenge.",
            "Success is the sum of small efforts."
        ]
        
        self.create_widgets()
        self.load_progress()

    def disable_event(self):
        pass  # Função vazia para desativar o fechamento da janela

    def create_widgets(self):
        tk.Label(self.root, text="Set time to lock (min/sec):").pack(pady=10)

        self.time_entry = tk.Entry(self.root)
        self.time_entry.pack(pady=5)

        tk.Radiobutton(self.root, text="Minutes", variable=self.time_mode, value="minutes").pack()
        tk.Radiobutton(self.root, text="Seconds", variable=self.time_mode, value="seconds").pack()

        self.start_button = tk.Button(self.root, text="Start Lock", command=self.start_lock)
        self.start_button.pack(pady=10)

        self.status_label = tk.Label(self.root, text="", fg="red")
        self.status_label.pack(pady=5)

    def start_lock(self):
        try:
            input_time = int(self.time_entry.get())
            if self.time_mode.get() == "minutes":
                self.lock_time = input_time * 60
            else:
                self.lock_time = input_time
            
            self.time_left = self.lock_time
            self.start_time = time.time()
            self.lock_active = True
            self.save_progress()
            
            self.start_button.config(state="disabled")
            self.status_label.config(text="Lock activated")
            
            Thread(target=self.lock_computer).start()
            self.update_timer()
        except ValueError:
            self.status_label.config(text="Invalid time input.")

    def update_timer(self):
        if self.lock_active:
            elapsed = time.time() - self.start_time
            self.time_left = max(0, self.lock_time - int(elapsed))

            if self.time_left > 0:
                mins, secs = divmod(self.time_left, 60)
                timer_display = f"{mins:02}:{secs:02}"
                random_phrase = random.choice(self.phrases)
                self.status_label.config(text=f"Time left: {timer_display}\n{random_phrase}")
                self.root.after(1000, self.update_timer)
            else:
                self.unlock_computer()

    def lock_computer(self):
        keys = [
            'esc', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12',
             'print screen', 'scroll lock', 'pause', 'insert', 'home', 'page up', 'delete', 
             'end', 'page down', 'up', 'down', 'left', 'right',
              'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 
              'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
               '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
              '-', '=', '[', ']', '\\', ';', "'", ',', '.', '/',
               'space', 'tab', 'enter', 'shift', 'ctrl', 'alt', 'caps lock', 'num lock', 
             'scroll lock', 'windows', 'menu'
        ]   


        
        while self.lock_active and self.time_left > 0:
            # Movendo o mouse para o canto para evitar uso
            mouse.move(0, 0, absolute=True, duration=0.1)
            for key in keys:
                    keyboard.block_key(key)
            time.sleep(1)

    def unlock_computer(self):
        self.lock_active = False
        self.start_button.config(state="normal")
        self.status_label.config(text="Unlocked! You are free.")
        # Desbloqueia as teclas específicas
        if 'esc' in keyboard._hooks:
            keyboard.unblock_key('esc')
        if 'f4' in keyboard._hooks:
            keyboard.unblock_key('f4')

    def save_progress(self):
        with open("lock_progress.json", "w") as f:
            json.dump({
                "lock_time": self.lock_time,
                "start_time": self.start_time,
                "time_left": self.time_left,
                "lock_active": self.lock_active
            }, f)

    def load_progress(self):
        if os.path.exists("lock_progress.json"):
            with open("lock_progress.json", "r") as f:
                data = json.load(f)
                self.lock_time = data["lock_time"]
                self.start_time = data["start_time"]
                self.time_left = data["time_left"]
                self.lock_active = data["lock_active"]

                if self.lock_active:
                    self.start_button.config(state="disabled")
                    self.status_label.config(text="Resuming lock")
                    self.update_timer()
                    Thread(target=self.lock_computer).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = EpyktetoApp(root)
    root.mainloop()
