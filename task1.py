import tkinter as tk
from tkinter import messagebox
import threading
import time

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List ✨")
        self.root.geometry("450x600")
        self.root.configure(bg="#1e1e2f")

        self.tasks = []
        self.title_label = tk.Label(root, text="", font=("Segoe UI", 20, "bold"), bg="#1e1e2f", fg="#00FFAA")
        self.title_label.pack(pady=10)
        threading.Thread(target=self.animate_title, daemon=True).start()

        self.task_entry = tk.Entry(root, font=("Segoe UI", 14), bg="#2e2e4d", fg="white", insertbackground="white", width=30)
        self.task_entry.pack(pady=10)
        self.task_entry.focus()

        self.add_btn = tk.Button(root, text=" Add Task", command=self.add_task, bg="#00FF7F", fg="black", font=("Segoe UI", 12, "bold"), width=20)
        self.add_btn.pack(pady=5)

        list_frame = tk.Frame(root, bg="#1e1e2f")
        list_frame.pack(pady=10)

        self.listbox = tk.Listbox(list_frame, font=("Segoe UI", 12), width=40, height=12, bg="#f0f0f0", fg="#333333", selectbackground="#c0ffee")
        self.listbox.pack(side=tk.LEFT, padx=(10, 0))

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        tk.Button(root, text=" Mark as Done", command=self.mark_done, bg="#00BFFF", fg="white", font=("Segoe UI", 12, "bold"), width=20).pack(pady=5)
        tk.Button(root, text=" Delete Task", command=self.delete_task, bg="#FF4C4C", fg="white", font=("Segoe UI", 12, "bold"), width=20).pack(pady=5)

        
        self.status_label = tk.Label(root, text="Total: 0 | Pending: 0", font=("Segoe UI", 10), bg="#1e1e2f", fg="#aaaaaa")
        self.status_label.pack(pady=10)

    def animate_title(self):
        text = " To-Do List App "
        displayed = ""
        for char in text:
            displayed += char
            self.title_label.config(text=displayed)
            time.sleep(0.1)

    def update_status(self):
        total = len(self.tasks)
        done = sum(1 for task in self.tasks if task.startswith("✔️"))
        self.status_label.config(text=f"Total: {total} | Pending: {total - done}")

    def add_task(self):
        task = self.task_entry.get().strip().capitalize()
        if not task:
            messagebox.showwarning("Input Error", "Task cannot be empty.")
            return
        if task in [t.replace(" ", "") for t in self.tasks]:
            messagebox.showinfo("Duplicate Task", "This task already exists.")
            return
        self.tasks.append(task)
        self.update_list()
        self.task_entry.delete(0, tk.END)

    def mark_done(self):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            task = self.tasks[index]
            if not task.startswith("✔️"):
                self.tasks[index] = "✔️ " + task
                self.update_list()
        else:
            messagebox.showwarning("Selection Error", "Select a task to mark as done.")

    def delete_task(self):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            del self.tasks[index]
            self.update_list()
        else:
            messagebox.showwarning("Selection Error", "Select a task to delete.")

    def update_list(self):
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            self.listbox.insert(tk.END, task)
        self.update_status()


if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
