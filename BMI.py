import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt

# Database setup
def init_db():
    conn = sqlite3.connect('bmi_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bmi_records (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            weight REAL NOT NULL,
            height REAL NOT NULL,
            bmi REAL NOT NULL,
            category TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def store_bmi_record(name, weight, height, bmi, category):
    conn = sqlite3.connect('bmi_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bmi_records (name, weight, height, bmi, category)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, weight, height, bmi, category))
    conn.commit()
    conn.close()

def get_user_bmi_history(name):
    conn = sqlite3.connect('bmi_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT timestamp, bmi FROM bmi_records WHERE name = ?
    ''', (name,))
    records = cursor.fetchall()
    conn.close()
    return records

# BMI Calculator class
class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")

        # Name Entry
        self.name_label = tk.Label(root, text="Name:")
        self.name_label.grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Weight Entry
        self.weight_label = tk.Label(root, text="Weight (kg):")
        self.weight_label.grid(row=1, column=0, padx=10, pady=5)
        self.weight_entry = tk.Entry(root)
        self.weight_entry.grid(row=1, column=1, padx=10, pady=5)

        # Height Entry
        self.height_label = tk.Label(root, text="Height (m):")
        self.height_label.grid(row=2, column=0, padx=10, pady=5)
        self.height_entry = tk.Entry(root)
        self.height_entry.grid(row=2, column=1, padx=10, pady=5)

        # Calculate Button
        self.calc_button = tk.Button(root, text="Calculate BMI", command=self.calculate_bmi)
        self.calc_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Result Labels
        self.result_label = tk.Label(root, text="", font=("Helvetica", 12))
        self.result_label.grid(row=4, column=0, columnspan=2, pady=10)

        # History Button
        self.history_button = tk.Button(root, text="View History", command=self.view_history)
        self.history_button.grid(row=5, column=0, columnspan=2, pady=10)

    def calculate_bmi(self):
        try:
            name = self.name_entry.get()
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            if not name:
                raise ValueError("Name cannot be empty.")
            if weight <= 0 or height <= 0:
                raise ValueError("Weight and height must be positive numbers.")

            bmi = weight / (height ** 2)
            category = self.get_bmi_category(bmi)
            self.result_label.config(text=f"BMI: {bmi:.2f} ({category})")
            store_bmi_record(name, weight, height, bmi, category)

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def get_bmi_category(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"

    def view_history(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Input Error", "Please enter your name to view history.")
            return

        records = get_user_bmi_history(name)
        if not records:
            messagebox.showinfo("No Records", "No history found for this user.")
            return

        dates, bmis = zip(*records)
        plt.plot(dates, bmis, marker='o')
        plt.title(f'BMI History for {name}')
        plt.xlabel('Date')
        plt.ylabel('BMI')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

# Main application
if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()
