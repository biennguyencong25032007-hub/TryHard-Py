import tkinter as tk
from tkinter import messagebox

class BankApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Simple Bank App")

        self.balance = 0

        self.label_balance = tk.Label(master, text="Balance: $0")
        self.label_balance.pack()

        self.label_amount = tk.Label(master, text="Amount:")
        self.label_amount.pack()

        self.entry_amount = tk.Entry(master)
        self.entry_amount.pack()

        self.button_deposit = tk.Button(master, text="Deposit", command=self.deposit)
        self.button_deposit.pack()

        self.button_withdraw = tk.Button(master, text="Withdraw", command=self.withdraw)
        self.button_withdraw.pack()

        self.button_check_balance = tk.Button(master, text="Check Balance", command=self.check_balance)
        self.button_check_balance.pack()

        self.button_exit = tk.Button(master, text="Exit", command=master.quit)
        self.button_exit.pack()

    def deposit(self):
        try:
            amount = float(self.entry_amount.get())
            if amount > 0:
                self.balance += amount
                self.update_balance_label()
            else:
                messagebox.showerror("Error", "Invalid amount. Please enter a positive number.")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a number.")

    def withdraw(self):
        try:
            amount = float(self.entry_amount.get())
            if 0 < amount <= self.balance:
                self.balance -= amount
                self.update_balance_label()
            else:
                messagebox.showerror("Error", "Insufficient funds.")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a number.")

    def check_balance(self):
        messagebox.showinfo("Balance", f"Your balance is: ${self.balance:.2f}")

    def update_balance_label(self):
        self.label_balance.config(text=f"Balance: ${self.balance:.2f}")

def main():
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()