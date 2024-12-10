import tkinter as tk
from tkinter import messagebox, simpledialog
from service.finance_service import DataService
from domain.income import Income
from domain.expense import Expense
from domain.budget import Budget

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")

        # Initialize the DataService
        self.data_service = DataService()

        # Create tabs for Incomes, Expenses, and Budgets
        self.tabs = tk.Frame(self.root)
        self.tabs.pack()

        self.income_tab = tk.Button(self.tabs, text="Incomes", command=self.show_incomes)
        self.income_tab.grid(row=0, column=0)

        self.expense_tab = tk.Button(self.tabs, text="Expenses", command=self.show_expenses)
        self.expense_tab.grid(row=0, column=1)

        self.budget_tab = tk.Button(self.tabs, text="Budgets", command=self.show_budgets)
        self.budget_tab.grid(row=0, column=2)

        # Create table for displaying data
        self.table = tk.Frame(self.root)
        self.table.pack()

        # Show Incomes by default
        self.show_incomes()

        # Add button for adding records
        self.add_button = tk.Button(self.root, text="Add", command=self.show_add_form)
        self.add_button.pack(side=tk.LEFT, padx=10)

    def show_incomes(self):
        self.clear_table()
        self.show_table("Income", ["ID", "Source", "Amount", "Date", "Description"], self.data_service.get_incomes(), self.delete_income)

    def show_expenses(self):
        self.clear_table()
        self.show_table("Expense", ["ID", "Category", "Amount", "Date", "Description"], self.data_service.get_expenses(), self.delete_expense)

    def show_budgets(self):
        self.clear_table()
        self.show_table("Budget", ["ID", "Category", "Amount"], self.data_service.get_budgets(), self.delete_budget)

    def show_table(self, entity, headers, data, delete_action):
        # Display table headers
        for col, header in enumerate(headers):
            tk.Label(self.table, text=header).grid(row=0, column=col)

        # Display data in the table
        for row_num, item in enumerate(data, 1):
            if entity == "Income":
                values = [item.id, item.source, item.amount, item.date, item.description]
            elif entity == "Expense":
                values = [item.id, item.category, item.amount, item.date, item.description]
            else:  # Budget
                values = [item.id, item.category, item.amount]

            for col, value in enumerate(values):
                tk.Label(self.table, text=value).grid(row=row_num, column=col)

            # Add delete button for each row
            tk.Button(self.table, text="Delete", command=lambda item=item: delete_action(item.id)).grid(row=row_num, column=len(values))

            # Add update button for each row
            tk.Button(self.table, text="Update", command=lambda item=item, entity=entity: self.show_update_form(item, entity)).grid(row=row_num, column=len(values) + 1)

    def clear_table(self):
        for widget in self.table.winfo_children():
            widget.destroy()

    def delete_income(self, income_id):
        self.data_service.delete_income(income_id)
        messagebox.showinfo("Success", "Income deleted successfully.")
        self.show_incomes()

    def delete_expense(self, expense_id):
        self.data_service.delete_expense(expense_id)
        messagebox.showinfo("Success", "Expense deleted successfully.")
        self.show_expenses()

    def delete_budget(self, budget_id):
        self.data_service.delete_budget(budget_id)
        messagebox.showinfo("Success", "Budget deleted successfully.")
        self.show_budgets()

    def add_income(self, source, amount, date, description):
        self.data_service.create_income(source, amount, date, description)
        messagebox.showinfo("Success", "Income added successfully.")
        self.show_incomes()

    def add_expense(self, category, amount, date, description):
        self.data_service.create_expense(category, amount, date, description)
        messagebox.showinfo("Success", "Expense added successfully.")
        self.show_expenses()

    def add_budget(self, category, amount):
        self.data_service.create_budget(category, amount)
        messagebox.showinfo("Success", "Budget added successfully.")
        self.show_budgets()

    def update_income(self, income_id, source, amount, date, description):
        self.data_service.update_income(income_id, source, amount, date, description)
        messagebox.showinfo("Success", "Income updated successfully.")
        self.show_incomes()

    def update_expense(self, expense_id, category, amount, date, description):
        self.data_service.update_expense(expense_id, category, amount, date, description)
        messagebox.showinfo("Success", "Expense updated successfully.")
        self.show_expenses()

    def update_budget(self, budget_id, category, amount):
        self.data_service.update_budget(budget_id, category, amount)
        messagebox.showinfo("Success", "Budget updated successfully.")
        self.show_budgets()

    def show_add_form(self):
        entity = simpledialog.askstring("Input", "Which entity would you like to add (Income, Expense, Budget)?")
        if entity.lower() == "income":
            source = simpledialog.askstring("Input", "Enter income source:")
            amount = simpledialog.askfloat("Input", "Enter income amount:")
            date = simpledialog.askstring("Input", "Enter income date (YYYY-MM-DD):")
            description = simpledialog.askstring("Input", "Enter income description:")
            if source and amount and date and description:
                self.add_income(source, amount, date, description)
        elif entity.lower() == "expense":
            category = simpledialog.askstring("Input", "Enter expense category:")
            amount = simpledialog.askfloat("Input", "Enter expense amount:")
            date = simpledialog.askstring("Input", "Enter expense date (YYYY-MM-DD):")
            description = simpledialog.askstring("Input", "Enter expense description:")
            if category and amount and date and description:
                self.add_expense(category, amount, date, description)
        elif entity.lower() == "budget":
            category = simpledialog.askstring("Input", "Enter budget category:")
            amount = simpledialog.askfloat("Input", "Enter budget amount:")
            if category and amount:
                self.add_budget(category, amount)

    def show_update_form(self, item, entity):
        if entity.lower() == "income":
            source = simpledialog.askstring("Input", f"Enter new source (current: {item.source}):")
            amount = simpledialog.askfloat("Input", f"Enter new amount (current: {item.amount}):")
            date = simpledialog.askstring("Input", f"Enter new date (current: {item.date}):")
            description = simpledialog.askstring("Input", f"Enter new description (current: {item.description}):")
            self.update_income(item.id, source, amount, date, description)
        elif entity.lower() == "expense":
            category = simpledialog.askstring("Input", f"Enter new category (current: {item.category}):")
            amount = simpledialog.askfloat("Input", f"Enter new amount (current: {item.amount}):")
            date = simpledialog.askstring("Input", f"Enter new date (current: {item.date}):")
            description = simpledialog.askstring("Input", f"Enter new description (current: {item.description}):")
            self.update_expense(item.id, category, amount, date, description)
        elif entity.lower() == "budget":
            category = simpledialog.askstring("Input", f"Enter new category (current: {item.category}):")
            amount = simpledialog.askfloat("Input", f"Enter new amount (current: {item.amount}):")
            self.update_budget(item.id, category, amount)
