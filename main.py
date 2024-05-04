import tkinter as tk
from tkinter import messagebox
import keyboard
import time
import subprocess
import os

class EpyktetoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Epykteto")
        self.root.geometry("400x200")
        self.root.config(bg="#1f1f1f")
        
        self.label = tk.Label(root, text="Set lock time (seconds):", fg="white", bg="#1f1f1f", font=("Arial", 12))
        self.label.pack(pady=10)

        self.entry = tk.Entry(root, bg="#1f1f1f", fg="white", font=("Arial", 12), insertbackground="white")
        self.entry.pack(pady=5)

        self.button = tk.Button(root, text="Confirm", command=self.start_timer, bg="#2f2f2f", fg="white", font=("Arial", 12), padx=10)
        self.button.pack(pady=10)

        self.duration = 0  # Initialize duration as 0 at the beginning

    def start_timer(self):
        try:
            self.duration = int(self.entry.get())
            self.root.attributes("-fullscreen", True)
            self.root.bind("<Key>", self.block_keyboard)
            self.start_time = time.time()
            self.save_start_time()
            self.root.after(self.duration * 1000, self.check_time)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

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
            messagebox.showinfo("Epykteto", "Time's up. Your device is no longer locked.")

    def block_keyboard(self, event):
        messagebox.showinfo("Locked", "You can't use the keyboard while the device is locked.")
        subprocess.run(["shutdown", "/l"])  # Execute 'shutdown /l' command to log out

    def check_previous_timer(self):
        start_time = self.load_start_time()
        if start_time is not None:
            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time < self.duration:
                remaining_time = self.duration - elapsed_time
                self.root.attributes("-fullscreen", True)
                self.root.bind("<Key>", self.block_keyboard)
                self.start_time = start_time
                self.root.after(int(remaining_time * 1000), self.check_time)
            else:
                self.root.attributes("-fullscreen", False)
                self.root.unbind("<Key>")
                messagebox.showinfo("Epykteto", "Previous time expired. Your device is no longer locked.")
                # If previous time has expired, clear the start time file
                self.clear_previous_timer()

    def clear_previous_timer(self):
        try:
            os.remove("start_time.txt")
        except FileNotFoundError:
            pass  # If file doesn't exist, do nothing

if __name__ == "__main__":
    root = tk.Tk()
    app = EpyktetoApp(root)
    app.check_previous_timer()
    root.mainloop()
