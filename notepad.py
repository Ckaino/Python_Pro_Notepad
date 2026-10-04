import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class UltraNotepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Pro Text Workspace")
        self.root.geometry("900x700")
        
        self.dark_mode_active = False
        self.current_font_family = "Arial"
        self.current_font_size = 12
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # --- 1. TOOLBAR PANEL ---
        self.toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED, bg="#f0f0f0")
        self.toolbar.pack(side="top", fill="x")
        
        tk.Label(self.toolbar, text=" Font: ", bg="#f0f0f0").pack(side="left", padx=2)
        self.font_family_var = tk.StringVar(value=self.current_font_family)
        available_fonts = ["Arial", "Courier", "Helvetica", "Times New Roman", "Verdana", "Consolas"]
        self.font_dropdown = ttk.Combobox(self.toolbar, textvariable=self.font_family_var, values=available_fonts, width=15, state="readonly")
        self.font_dropdown.pack(side="left", padx=5, pady=5)
        self.font_dropdown.bind("<<ComboboxSelected>>", self.apply_font_changes)
        
        tk.Label(self.toolbar, text=" Size: ", bg="#f0f0f0").pack(side="left", padx=2)
        self.font_size_var = tk.IntVar(value=self.current_font_size)
        available_sizes = [8, 10, 12, 14, 16, 18, 20, 24, 28, 32, 36, 48]
        self.size_dropdown = ttk.Combobox(self.toolbar, textvariable=self.font_size_var, values=available_sizes, width=5, state="readonly")
        self.size_dropdown.pack(side="left", padx=5, pady=5)
        self.size_dropdown.bind("<<ComboboxSelected>>", self.apply_font_changes)
        
        # --- 2. TEXT AREA ---
        self.text_area = tk.Text(self.root, wrap="word", font=(self.current_font_family, self.current_font_size), undo=True)
        self.text_area.pack(fill="both", expand=True)
        
        self.scroll_bar = tk.Scrollbar(self.text_area)
        self.scroll_bar.pack(side="right", fill="y")
        self.text_area.config(yscrollcommand=self.scroll_bar.set)
        self.scroll_bar.config(command=self.text_area.yview)
        
        # --- 3. STATUS BAR ---
        self.status_bar = tk.Label(self.root, text=" Words: 0 | Characters: 0 ", anchor="e", bd=1, relief=tk.SUNKEN, bg="#f0f0f0")
        self.status_bar.pack(side="bottom", fill="x")
        self.text_area.bind("<<Modified>>", self.update_status_bar)
        
        # --- 4. DROPDOWN MENUS ---
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New File", command=self.new_file)
        self.file_menu.add_command(label="Open File...", command=self.open_file)
        self.file_menu.add_command(label="Save As...", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit App", command=self.root.quit)
        
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=lambda: self.text_area.event_generate("<<Undo>>"))
        self.edit_menu.add_command(label="Redo", command=lambda: self.text_area.event_generate("<<Redo>>"))
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=lambda: self.text_area.event_generate("<<Cut>>"))
        self.edit_menu.add_command(label="Copy", command=lambda: self.text_area.event_generate("<<Copy>>"))
        self.edit_menu.add_command(label="Paste", command=lambda: self.text_area.event_generate("<<Paste>>"))
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Find & Replace...", command=self.launch_find_replace_dialog)
        
        self.format_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Format", menu=self.format_menu)
        self.format_menu.add_command(label="Toggle Dark Mode Theme", command=self.toggle_theme)

    def apply_font_changes(self, event=None):
        self.current_font_family = self.font_family_var.get()
        self.current_font_size = self.font_size_var.get()
        self.text_area.config(font=(self.current_font_family, self.current_font_size))

    def launch_find_replace_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Find and Replace Engine")
        dialog.geometry("400x150")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        
        tk.Label(dialog, text="Search Target:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        find_entry = tk.Entry(dialog, width=25)
        find_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Replace Value:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        replace_entry = tk.Entry(dialog, width=25)
        replace_entry.grid(row=1, column=1, padx=10, pady=5)
        
        def execute_find_replace():
            search_query = find_entry.get()
            substitution = replace_entry.get()
            
            if not search_query:
                messagebox.showwarning("Empty Target", "Please input an active value target to find.")
                return
                
            content = self.text_area.get("1.0", tk.END)
            match_occurrences = content.count(search_query)
            
            if match_occurrences == 0:
                messagebox.showinfo("Zero Results", f"No records matching '{search_query}' discovered.")
                return
                
            updated_content = content.replace(search_query, substitution)
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", updated_content)
            messagebox.showinfo("Success Pipeline", f"Successfully updated {match_occurrences} instances.")
            dialog.destroy()

        submit_btn = tk.Button(dialog, text="Execute Swap", command=execute_find_replace, bg="#0275d8", fg="white")
        submit_btn.grid(row=2, column=1, columnspan=2, pady=15, sticky="e", padx=10)

    def toggle_theme(self):
        if not self.dark_mode_active:
            self.text_area.config(bg="#2d2d2d", fg="#ffffff", insertbackground="white")
            self.status_bar.config(bg="#1e1e1e", fg="#aaaaaa")
            self.toolbar.config(bg="#1e1e1e")
            self.dark_mode_active = True
        else:
            self.text_area.config(bg="#ffffff", fg="#000000", insertbackground="black")
            self.status_bar.config(bg="#f0f0f0", fg="#000000")
            self.toolbar.config(bg="#f0f0f0")
            self.dark_mode_active = False

    def update_status_bar(self, event=None):
        if self.text_area.edit_modified():
            content = self.text_area.get("1.0", "end-1c")
            words = len(content.split())
            characters = len(content)
            self.status_bar.config(text=f" Words: {words} | Characters: {characters} ")
            self.text_area.edit_modified(False)

    def new_file(self):
        self.text_area.delete("1.0", tk.END)
        self.root.title("New File - Python Notepad")

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    self.text_area.delete("1.0", tk.END)
                    self.text_area.insert("1.0", file.read())
                self.root.title(f"{file_path} - Python Notepad")
            except Exception as e: messagebox.showerror("Error", f"Failed file ingestion:\n{e}")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.text_area.get("1.0", tk.END))
                self.root.title(f"{file_path} - Python Notepad")
                messagebox.showinfo("Success", "File configuration saved.")
            except Exception as e: messagebox.showerror("Error", f"Export failure:\n{e}")

if __name__ == "__main__":
    window = tk.Tk()
    app = UltraNotepad(window)
    window.mainloop()
