import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

class AutomatedSystemUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Automated System")
        self.root.geometry("1100x750")
        self.root.configure(bg='#f0f4f7')

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Arial', 11), padding=6)
        style.configure('TLabel', background='#f0f4f7')

        self.status_bar = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=('Arial', 10))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)
        self.create_main_menu()

        self.root.bind('<Escape>', lambda e: self.create_main_menu())

    def create_main_menu(self):
        self.clear_main_frame()

        label = ttk.Label(self.main_frame, text="Welcome to the Automated System", font=("Arial", 22, "bold"))
        label.pack(pady=40)

        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)

        manual_btn = ttk.Button(button_frame, text="🔧 Manual Control / Device Overview", command=self.open_device_overview, width=40)
        manual_btn.grid(row=0, column=0, padx=20, pady=15)

        profile_btn = ttk.Button(button_frame, text="📂 Profile Manager", command=self.open_profile_menu, width=40)
        profile_btn.grid(row=1, column=0, padx=20, pady=15)

        exit_btn = ttk.Button(button_frame, text="🚪 Exit", command=self.root.quit, width=40)
        exit_btn.grid(row=2, column=0, padx=20, pady=15)

    def open_profile_menu(self):
        self.clear_main_frame()
        self.update_status("Profile menu opened.")

        ttk.Button(self.main_frame, text="← Back", command=self.create_main_menu).pack(anchor="w", padx=10, pady=10)
        ttk.Label(self.main_frame, text="Select a Profile Manager", font=("Arial", 18, "bold")).pack(pady=10)

        profile_buttons = ttk.Frame(self.main_frame)
        profile_buttons.pack(pady=10)

        ttk.Button(profile_buttons, text="MFC Profile Manager", command=lambda: self.open_tab("MFCs Profile Management"), width=30).grid(row=0, column=0, padx=15, pady=10)
        ttk.Button(profile_buttons, text="Cooling Profile Manager", command=lambda: self.open_tab("Cooling Profile Management"), width=30).grid(row=1, column=0, padx=15, pady=10)
        ttk.Button(profile_buttons, text="Valve Profile Manager", command=lambda: self.open_tab("Valve Profile Management"), width=30).grid(row=2, column=0, padx=15, pady=10)

        ttk.Separator(self.main_frame, orient='horizontal').pack(fill='x', padx=30, pady=15)

        graph_label = ttk.Label(self.main_frame, text="Graph-based Profiles", font=("Arial", 14, "bold"))
        graph_label.pack(pady=5)

        graph_frame = ttk.Frame(self.main_frame)
        graph_frame.pack(pady=10)

        self.onoff_icon = self.load_icon("onoff_graph_icon.png")
        self.diffconc_icon = self.load_icon("diffconc_graph_icon.png")

        if self.onoff_icon:
            tk.Button(graph_frame, image=self.onoff_icon, command=lambda: self.open_tab("On/Off Profile Management"), borderwidth=2, cursor="hand2").grid(row=0, column=0, padx=25)
            ttk.Label(graph_frame, text="On/Off Profile", font=("Arial", 12)).grid(row=1, column=0)

        if self.diffconc_icon:
            tk.Button(graph_frame, image=self.diffconc_icon, command=lambda: self.open_tab("DiffConc Profile Management"), borderwidth=2, cursor="hand2").grid(row=0, column=1, padx=25)
            ttk.Label(graph_frame, text="DiffConc Profile", font=("Arial", 12)).grid(row=1, column=1)

    def open_device_overview(self):
        self.update_status("Device overview opened.")
        self.open_tab("Device Overview")

    def open_tab(self, tab_name):
        self.clear_main_frame()
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        tabs = {
            "Device Overview": self.create_dummy_tab("Device Overview content here."),
            "MFCs Profile Management": self.create_dummy_tab("MFC profile manager UI here."),
            "Cooling Profile Management": self.create_dummy_tab("Cooling profile manager UI here."),
            "Valve Profile Management": self.create_dummy_tab("Valve profile manager UI here."),
            "On/Off Profile Management": self.create_dummy_tab("On/Off profile UI here."),
            "DiffConc Profile Management": self.create_dummy_tab("DiffConc profile UI here.")
        }

        for name, frame in tabs.items():
            self.notebook.add(frame, text=name)

        for idx in range(self.notebook.index("end")):
            if self.notebook.tab(idx, "text") == tab_name:
                self.notebook.select(idx)
                break

        ttk.Button(self.main_frame, text="← Back to Menu", command=self.create_main_menu).pack(pady=10)

    def create_dummy_tab(self, text):
        frame = ttk.Frame(self.notebook)
        ttk.Label(frame, text=text, padding=30).pack()
        return frame

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def load_icon(self, filename):
        try:
            path = os.path.join(os.path.dirname(__file__), filename)
            img = Image.open(path).resize((100, 100))
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading image {filename}: {e}")
            return None

    def update_status(self, message):
        self.status_bar.config(text=message)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutomatedSystemUI(root)
    root.mainloop()
