import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os

class ProfilePathManager:
    def __init__(self, default_path="profiles"):
        self.base_path = default_path
        self.sub_paths = {
            "main": "main_profiles",
            "mfc": "mfc_profiles",
            "cooling": "cooling_profiles",
            "valve": "valve_profiles"
        }
        self.ensure_directories()

    def ensure_directories(self):
        for sub in self.sub_paths.values():
            path = os.path.join(self.base_path, sub)
            os.makedirs(path, exist_ok=True)

    def set_new_path(self, new_path):
        self.base_path = new_path
        self.ensure_directories()

    def get_path(self, profile_type):
        return os.path.join(self.base_path, self.sub_paths[profile_type])

class ProfilePathUI(ttk.Frame):
    def __init__(self, parent, path_manager):
        super().__init__(parent)
        self.path_manager = path_manager

        ttk.Label(self, text="Profile Path:").pack(side='left', padx=5)

        self.path_var = tk.StringVar(value=self.path_manager.base_path)
        ttk.Entry(self, textvariable=self.path_var, width=50).pack(side='left', padx=5)

        ttk.Button(self, text="Browse", command=self.browse).pack(side='left', padx=5)
        ttk.Button(self, text="Set Path", command=self.set_path).pack(side='left', padx=5)

    def browse(self):
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            self.path_var.set(selected_dir)

    def set_path(self):
        new_path = self.path_var.get()
        if new_path:
            self.path_manager.set_new_path(new_path)
            messagebox.showinfo("Success", f"Path set to {new_path}")
        else:
            messagebox.showerror("Error", "Please enter a valid path")

# Voorbeeld integratie in je bestaande UI:
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Profile Path Example")

    path_manager = ProfilePathManager()

    # Dit is je path configuratie UI, plaats deze waar jij wilt.
    path_ui = ProfilePathUI(root, path_manager)
    path_ui.pack(pady=20, padx=20)

    root.mainloop()