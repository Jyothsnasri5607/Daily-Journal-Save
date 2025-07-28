import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import os
from datetime import datetime

# Constants
JOURNAL_DIR = "journal_entries"
DATE_FORMAT = "%Y-%m-%d"

# Ensure journal directory exists
os.makedirs(JOURNAL_DIR, exist_ok=True)

class JournalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📔 Advanced Daily Journal")
        self.root.geometry("800x600")
        self.root.config(bg="#f0f0f0")

        self.create_widgets()
        self.set_status("Welcome! Ready to journal.")

    def create_widgets(self):
        # 🧾 Top bar: Title and Date/ Search fields
        top_frame = tk.Frame(self.root, bg="#f0f0f0")
        top_frame.pack(pady=10)

        tk.Label(top_frame, text="📅 Date (YYYY-MM-DD):", font=("Arial", 12), bg="#f0f0f0").pack(side=tk.LEFT)
        self.date_entry = tk.Entry(top_frame, font=("Arial", 12), width=15)
        self.date_entry.insert(0, datetime.now().strftime(DATE_FORMAT))
        self.date_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(top_frame, text="🔍 Search:", font=("Arial", 12), bg="#f0f0f0").pack(side=tk.LEFT, padx=(30, 5))
        self.search_entry = tk.Entry(top_frame, font=("Arial", 12), width=20)
        self.search_entry.pack(side=tk.LEFT)
        tk.Button(top_frame, text="Go", command=self.search_entry_file, bg="#dcdcdc", font=("Arial", 11)).pack(side=tk.LEFT, padx=5)

        # 📝 Text area for journal content
        self.text_area = scrolledtext.ScrolledText(self.root, wrap="word", font=("Arial", 12), height=20)
        self.text_area.pack(padx=20, pady=10, fill="both", expand=True)

        # 🧰 Buttons frame
        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        buttons = [
            ("💾 Save", self.save_entry, "#4caf50"),
            ("📂 Load", self.load_entry, "#2196f3"),
            ("🗑️ Delete", self.delete_entry, "#e53935"),
            ("🧹 Clear", self.clear_fields, "#757575")
        ]

        for i, (text, cmd, color) in enumerate(buttons):
            tk.Button(btn_frame, text=text, font=("Arial", 12), bg=color, fg="white",
                      width=12, command=cmd).grid(row=0, column=i, padx=10)

        # ℹ️ Status bar
        self.status_bar = tk.Label(self.root, text="", bd=1, relief=tk.SUNKEN, anchor="w", bg="#eeeeee")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def set_status(self, msg):
        self.status_bar.config(text=msg)

    def get_file_path(self, date):
        return os.path.join(JOURNAL_DIR, f"{date}.txt")

    def save_entry(self):
        date = self.date_entry.get().strip()
        content = self.text_area.get("1.0", tk.END).strip()

        if not date or not content:
            messagebox.showwarning("Missing Info", "Date and journal content are required.")
            return

        with open(self.get_file_path(date), "w", encoding="utf-8") as file:
            file.write(content)

        self.set_status(f"Saved entry for {date}")
        messagebox.showinfo("Saved", f"Entry saved as '{date}.txt'")

    def load_entry(self):
        file_path = filedialog.askopenfilename(initialdir=JOURNAL_DIR,
                                               filetypes=[("Text Files", "*.txt")],
                                               title="Select Journal Entry")
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            date_str = os.path.basename(file_path).replace(".txt", "")
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, date_str)
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, content)
            self.set_status(f"Loaded entry: {date_str}")

    def delete_entry(self):
        date = self.date_entry.get().strip()
        file_path = self.get_file_path(date)

        if os.path.exists(file_path):
            if messagebox.askyesno("Delete Confirmation", f"Delete entry for {date}?"):
                os.remove(file_path)
                self.clear_fields()
                self.set_status(f"Deleted entry: {date}")
        else:
            messagebox.showwarning("Not Found", f"No entry found for {date}")

    def clear_fields(self):
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime(DATE_FORMAT))
        self.text_area.delete("1.0", tk.END)
        self.set_status("Cleared fields")

    def search_entry_file(self):
        keyword = self.search_entry.get().strip().lower()
        if not keyword:
            messagebox.showinfo("Search", "Please enter a keyword to search.")
            return

        for file_name in os.listdir(JOURNAL_DIR):
            if file_name.endswith(".txt"):
                with open(os.path.join(JOURNAL_DIR, file_name), "r", encoding="utf-8") as file:
                    content = file.read().lower()
                    if keyword in content or keyword in file_name.lower():
                        date_str = file_name.replace(".txt", "")
                        self.date_entry.delete(0, tk.END)
                        self.date_entry.insert(0, date_str)
                        self.text_area.delete("1.0", tk.END)
                        self.text_area.insert(tk.END, content)
                        self.set_status(f"Found keyword in {file_name}")
                        return

        messagebox.showinfo("Search", "No matching journal entry found.")
        self.set_status("No matches found.")

# Run Application
if __name__ == "__main__":
    root = tk.Tk()
    app = JournalApp(root)
    root.mainloop()
