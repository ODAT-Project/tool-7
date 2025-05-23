#Developed by ODAT project
#please see https://odat.info
#please see https://github.com/ODAT-Project
import os
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

class CSVMatcherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CSV Key Matcher")
        self.geometry("700x550")
        self.resizable(False, False)

        #menu Bar with About
        self.menu_bar = tk.Menu(self)
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)
        self.config(menu=self.menu_bar)

        #fetch CSV files
        self.csv_files = [f for f in os.listdir('.') if f.lower().endswith('.csv')]

        #section 1
        section1 = ttk.LabelFrame(self, text="Section 1: Select First CSV File")
        section1.pack(fill="both", padx=10, pady=5, expand=True)

        self.listbox1 = tk.Listbox(section1, height=6, exportselection=False)
        for f in self.csv_files:
            self.listbox1.insert(tk.END, f)
        self.listbox1.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)

        scrollbar1 = ttk.Scrollbar(section1, orient="vertical", command=self.listbox1.yview)
        scrollbar1.pack(side="left", fill="y", pady=10)
        self.listbox1.config(yscrollcommand=scrollbar1.set)

        frame1 = ttk.Frame(section1)
        frame1.pack(side="left", fill="x", padx=10, pady=10, expand=True)
        ttk.Label(frame1, text="Column Name (must match exactly as csv):").pack(anchor="w")
        self.entry_col1 = ttk.Entry(frame1)
        self.entry_col1.pack(fill="x")
        self.entry_col1.insert(0, "enter...")

        #section 2
        section2 = ttk.LabelFrame(self, text="Section 2: Select Second CSV File")
        section2.pack(fill="both", padx=10, pady=5, expand=True)

        self.listbox2 = tk.Listbox(section2, height=6, exportselection=False)
        for f in self.csv_files:
            self.listbox2.insert(tk.END, f)
        self.listbox2.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)

        scrollbar2 = ttk.Scrollbar(section2, orient="vertical", command=self.listbox2.yview)
        scrollbar2.pack(side="left", fill="y", pady=10)
        self.listbox2.config(yscrollcommand=scrollbar2.set)

        frame2 = ttk.Frame(section2)
        frame2.pack(side="left", fill="x", padx=10, pady=10, expand=True)
        ttk.Label(frame2, text="Column Name (must match exactly as csv):").pack(anchor="w")
        self.entry_col2 = ttk.Entry(frame2)
        self.entry_col2.pack(fill="x")
        self.entry_col2.insert(0, "enter...")

        #run and Quit buttons + result
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=10, pady=(0,5))
        self.run_btn = ttk.Button(btn_frame, text="Run", command=self.run_match)
        self.run_btn.pack(side="left", padx=(0,10))
        quit_btn = ttk.Button(btn_frame, text="Quit", command=self.quit)
        quit_btn.pack(side="left")
        self.result_label = ttk.Label(btn_frame, text="")
        self.result_label.pack(side="left", padx=20)

        #about section at bottom
        about_frame = ttk.LabelFrame(self, text="About Tool")
        about_frame.pack(fill="x", padx=10, pady=(5,10))
        about_text = (
            "CSV Key Matcher: Match specific column heading of any two csv files"
        )
        ttk.Label(about_frame, text=about_text, justify="center").pack(padx=5, pady=5)

    def show_about(self):
        messagebox.showinfo(
            "About",
            "Developed by ODAT project."
        )

    def run_match(self):
        #get selections
        try:
            idx1 = self.listbox1.curselection()[0]
            idx2 = self.listbox2.curselection()[0]
        except IndexError:
            messagebox.showerror("Selection Error", "Please select both CSV files.")
            return

        file1 = self.csv_files[idx1]
        file2 = self.csv_files[idx2]
        col1 = self.entry_col1.get().strip()
        col2 = self.entry_col2.get().strip()

        if not col1 or not col2:
            messagebox.showerror("Input Error", "Please enter both column names.")
            return

        #load and process data
        try:
            df1 = pd.read_csv(file1, low_memory=False)
            df2 = pd.read_csv(file2, low_memory=False)
        except FileNotFoundError as e:
            messagebox.showerror("File Error", f"{e}")
            return
        except Exception as e:
            messagebox.showerror("Error", f"Error loading files: {e}")
            return

        #check columns
        if col1 not in df1.columns:
            messagebox.showerror("Column Error", f"Column '{col1}' not found in '{file1}'.")
            return
        if col2 not in df2.columns:
            messagebox.showerror("Column Error", f"Column '{col2}' not found in '{file2}'.")
            return

        #count matches
        keys1 = set(df1[col1].dropna().astype(str))
        keys2 = set(df2[col2].dropna().astype(str))
        match_count = len(keys1.intersection(keys2))

        #display result
        self.result_label.config(text=f"Number of matching keys: {match_count}")

if __name__ == "__main__":
    app = CSVMatcherApp()
    app.mainloop()
