import tkinter as tk
from tkinter import messagebox
from Helper import is_valid_ticker, is_valid_start_date, is_valid_end_date, run_btpy

def on_submit():
    ticker = ticker_entry.get()
    start_date = start_entry.get()
    end_date = end_entry.get()

    if not ticker or not start_date or not end_date:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    if not is_valid_ticker(ticker):
        messagebox.showwarning("Input Error", "Invalid ticker.")
        return

    if not is_valid_start_date(ticker, start_date):
        messagebox.showwarning("Input Error", "Invalid start date.")
        return

    if not is_valid_end_date(ticker, end_date):
        messagebox.showwarning("Input Error", "Invalid end date.")
        return

    if end_date < start_date:
        messagebox.showwarning("Input Error", "End date cannot be before start date.")
        return

    print(f"Ticker: {ticker}")
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")

    run_btpy(ticker, start_date, end_date)

# Create the main window
root = tk.Tk()
root.title("Stock Data Input")
root.geometry("300x200")

# Create and place the widgets
tk.Label(root, text="Stock Ticker:").pack(pady=(10, 0))
ticker_entry = tk.Entry(root)
ticker_entry.pack()

tk.Label(root, text="Start Date (YYYY-MM-DD):").pack(pady=(10, 0))
start_entry = tk.Entry(root)
start_entry.pack()

tk.Label(root, text="End Date (YYYY-MM-DD):").pack(pady=(10, 0))
end_entry = tk.Entry(root)
end_entry.pack()

submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.pack(pady=15)

# Run the main loop
root.mainloop()