import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# --- Database Setup ---
def setup_db():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            description TEXT,
            amount REAL
        )
    """)
    conn.commit()
    conn.close()

setup_db()

# --- Add Expense ---
def add_expense():
    date = entry_date.get()
    category = combo_category.get()
    description = entry_description.get()
    amount = entry_amount.get()
    if not (date and category and description and amount):
        messagebox.showerror("Input Error", "All fields are required!")
        return

    try:
        amount = float(amount)
        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (date, category, description, amount) VALUES (?, ?, ?, ?)",
                       (date, category, description, amount))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Expense added successfully!")
        clear_inputs()
    except ValueError:
        messagebox.showerror("Input Error", "Amount must be a number!")

# --- View Expenses ---
def view_expenses():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    records = cursor.fetchall()
    conn.close()
    display_records(records)

# --- Clear Inputs ---
def clear_inputs():
    entry_date.delete(0, tk.END)
    combo_category.set("")
    entry_description.delete(0, tk.END)
    entry_amount.delete(0, tk.END)

# --- Display Records ---
def display_records(records):
    for row in tree.get_children():
        tree.delete(row)
    for record in records:
        tree.insert("", tk.END, values=record)

# --- Main App Window ---
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("700x500")
root.config(bg="#f0f8ff")  # Light blue background

# --- Header ---
header = tk.Label(root, text="Expense Tracker", font=("Helvetica", 20, "bold"), bg="#f0f8ff", fg="#4682b4")
header.pack(pady=10)

# --- Input Frame ---
frame_inputs = tk.Frame(root, bg="#f0f8ff")
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Date (YYYY-MM-DD):", bg="#f0f8ff").grid(row=0, column=0, padx=5, pady=5)
entry_date = tk.Entry(frame_inputs)
entry_date.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="Category:", bg="#f0f8ff").grid(row=1, column=0, padx=5, pady=5)
combo_category = ttk.Combobox(frame_inputs, values=["Food", "Transport", "Utilities", "Entertainment", "Others"])
combo_category.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="Description:", bg="#f0f8ff").grid(row=2, column=0, padx=5, pady=5)
entry_description = tk.Entry(frame_inputs)
entry_description.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="Amount (₹):", bg="#f0f8ff").grid(row=3, column=0, padx=5, pady=5)
entry_amount = tk.Entry(frame_inputs)
entry_amount.grid(row=3, column=1, padx=5, pady=5)

btn_add = tk.Button(frame_inputs, text="Add Expense", command=add_expense, bg="#4682b4", fg="white")
btn_add.grid(row=4, column=0, columnspan=2, pady=10)

# --- Records Frame ---
frame_records = tk.Frame(root, bg="#f0f8ff")
frame_records.pack(pady=10, fill="both", expand=True)

columns = ("ID", "Date", "Category", "Description", "Amount")
tree = ttk.Treeview(frame_records, columns=columns, show="headings")
tree.pack(fill="both", expand=True)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

btn_view = tk.Button(root, text="View All Expenses", command=view_expenses, bg="#4682b4", fg="white")
btn_view.pack(pady=10)

# --- Run App ---
root.mainloop()
