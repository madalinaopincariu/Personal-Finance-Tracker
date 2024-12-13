import tkinter as tk
from tkinter import messagebox, simpledialog
from service.finance_service import DataService
from domain.income import Income
from domain.expense import Expense
from domain.budget import Budget
import matplotlib.pyplot as plt

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

        # Create frames for displaying buttons (Sort, Filter, Search) for each tab
        self.income_buttons_frame = tk.Frame(self.root)
        self.expense_buttons_frame = tk.Frame(self.root)
        self.budget_buttons_frame = tk.Frame(self.root)

        # Create button frames for sorting, filtering, and searching
        self.add_sort_filter_search_buttons()

        # Create table for displaying data
        self.table = tk.Frame(self.root)
        self.table.pack()

        # Add button for adding records
        self.add_button = tk.Button(self.root, text="Add", command=self.show_add_form)
        self.add_button.pack(side=tk.LEFT, padx=10)

        # Show Incomes by default
        self.show_incomes()

        self.report_button = tk.Button(self.root, text="Generate Report", command=self.show_report_form)
        self.report_button.pack(side=tk.LEFT, padx=10)

        self.notifications_button = tk.Button(self.root, text="Check Notifications", command=self.show_notifications)
        self.notifications_button.pack(side=tk.LEFT, padx=10)

    def add_sort_filter_search_buttons(self):
        # Buttons for Incomes
        self.income_sort_button = tk.Button(self.income_buttons_frame, text="Sort Incomes", command=lambda: self.show_sort_form("income"))
        self.income_sort_button.pack(side=tk.LEFT, padx=10)

        self.income_filter_button = tk.Button(self.income_buttons_frame, text="Filter Incomes", command=lambda: self.show_filter_form("income"))
        self.income_filter_button.pack(side=tk.LEFT, padx=10)

        self.income_search_button = tk.Button(self.income_buttons_frame, text="Search Incomes", command=lambda: self.show_search_form("income"))
        self.income_search_button.pack(side=tk.LEFT, padx=10)

        # Buttons for Expenses
        self.expense_sort_button = tk.Button(self.expense_buttons_frame, text="Sort Expenses", command=lambda: self.show_sort_form("expense"))
        self.expense_sort_button.pack(side=tk.LEFT, padx=10)

        self.expense_filter_button = tk.Button(self.expense_buttons_frame, text="Filter Expenses", command=lambda: self.show_filter_form("expense"))
        self.expense_filter_button.pack(side=tk.LEFT, padx=10)

        self.expense_search_button = tk.Button(self.expense_buttons_frame, text="Search Expenses", command=lambda: self.show_search_form("expense"))
        self.expense_search_button.pack(side=tk.LEFT, padx=10)

        # Buttons for Budgets
        self.budget_sort_button = tk.Button(self.budget_buttons_frame, text="Sort Budgets", command=lambda: self.show_sort_form("budget"))
        self.budget_sort_button.pack(side=tk.LEFT, padx=10)

        self.budget_filter_button = tk.Button(self.budget_buttons_frame, text="Filter Budgets", command=lambda: self.show_filter_form("budget"))
        self.budget_filter_button.pack(side=tk.LEFT, padx=10)

        self.budget_search_button = tk.Button(self.budget_buttons_frame, text="Search Budgets", command=lambda: self.show_search_form("budget"))
        self.budget_search_button.pack(side=tk.LEFT, padx=10)

    def show_incomes(self):
        self.clear_table()
        self.hide_all_buttons()
        self.show_incomes_buttons()
        self.show_table("Income", ["ID", "Source", "Amount", "Date", "Description"], self.data_service.get_incomes(), self.delete_income)

    def show_expenses(self):
        self.clear_table()
        self.hide_all_buttons()
        self.show_expenses_buttons()
        self.show_table("Expense", ["ID", "Category", "Amount", "Date", "Description"], self.data_service.get_expenses(), self.delete_expense)

    def show_budgets(self):
        self.clear_table()
        self.hide_all_buttons()
        self.show_budgets_buttons()
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

    def hide_all_buttons(self):
        # Hide all button frames
        self.income_buttons_frame.pack_forget()
        self.expense_buttons_frame.pack_forget()
        self.budget_buttons_frame.pack_forget()

    def show_incomes_buttons(self):
        self.income_buttons_frame.pack()

    def show_expenses_buttons(self):
        self.expense_buttons_frame.pack()

    def show_budgets_buttons(self):
        self.budget_buttons_frame.pack()

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
        self.show_notifications()

    def add_expense(self, category, amount, date, description):
        self.data_service.create_expense(category, amount, date, description)
        messagebox.showinfo("Success", "Expense added successfully.")
        self.show_expenses()
        self.show_notifications()

    def add_budget(self, category, amount):
        self.data_service.create_budget(category, amount)
        messagebox.showinfo("Success", "Budget added successfully.")
        self.show_budgets()

    def update_income(self, income_id, source, amount, date, description):
        self.data_service.update_income(income_id, source, amount, date, description)
        messagebox.showinfo("Success", "Income updated successfully.")
        self.show_incomes()
        self.show_notifications()

    def update_expense(self, expense_id, category, amount, date, description):
        self.data_service.update_expense(expense_id, category, amount, date, description)
        messagebox.showinfo("Success", "Expense updated successfully.")
        self.show_expenses()
        self.show_notifications()

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

    # Add a new filter form
    def show_filter_form(self, entity):
        key = simpledialog.askstring("Input", f"Enter attribute to filter {entity} by:")
        value = simpledialog.askstring("Input", f"Enter value for {key}:")
        if key and value:
            if entity.lower() == "income":
                filtered_data = self.data_service.filter_incomes(key, value)
                self.display_filtered_data("Income", ["ID", "Source", "Amount", "Date", "Description"], filtered_data)
            elif entity.lower() == "expense":
                filtered_data = self.data_service.filter_expenses(key, value)
                self.display_filtered_data("Expense", ["ID", "Category", "Amount", "Date", "Description"], filtered_data)
            elif entity.lower() == "budget":
                filtered_data = self.data_service.filter_budgets(key, value)
                self.display_filtered_data("Budget", ["ID", "Category", "Amount"], filtered_data)

    # Add a new search form
    def show_search_form(self, entity):
        key = simpledialog.askstring("Input", f"Enter attribute to search {entity} by:")
        query = simpledialog.askstring("Input", f"Enter query for {key}:")
        if key and query:
            if entity.lower() == "income":
                search_results = self.data_service.search_incomes(key, query)
                self.display_filtered_data("Income", ["ID", "Source", "Amount", "Date", "Description"], search_results)
            elif entity.lower() == "expense":
                search_results = self.data_service.search_expenses(key, query)
                self.display_filtered_data("Expense", ["ID", "Category", "Amount", "Date", "Description"], search_results)
            elif entity.lower() == "budget":
                search_results = self.data_service.search_budgets(key, query)
                self.display_filtered_data("Budget", ["ID", "Category", "Amount"], search_results)

    # Add a new sort form
    def show_sort_form(self, entity):
        key = simpledialog.askstring("Input", f"Enter attribute to sort {entity} by:")
        reverse_input = simpledialog.askstring("Input", "Sort in descending order? (yes/no):").lower()
        
        if reverse_input == "yes":
            reverse = True
        elif reverse_input == "no":
            reverse = False
        else:
            messagebox.showwarning("Invalid Input", "Please enter 'yes' or 'no' to specify the sorting order.")
            return

        if key:
            if entity.lower() == "income":
                sorted_data = self.data_service.sort_incomes(key, reverse)
                self.display_filtered_data("Income", ["ID", "Source", "Amount", "Date", "Description"], sorted_data)
            elif entity.lower() == "expense":
                sorted_data = self.data_service.sort_expenses(key, reverse)
                self.display_filtered_data("Expense", ["ID", "Category", "Amount", "Date", "Description"], sorted_data)
            elif entity.lower() == "budget":
                sorted_data = self.data_service.sort_budgets(key, reverse)
                self.display_filtered_data("Budget", ["ID", "Category", "Amount"], sorted_data)

    # Helper method to display filtered data
    def display_filtered_data(self, entity, headers, data):
        self.clear_table()
        self.show_table(entity, headers, data, self.delete_income if entity == "Income" else self.delete_expense if entity == "Expense" else self.delete_budget)

    # Helper method to display sorted data
    def display_sorted_data(self, entity, headers, data):
        self.clear_table()
        self.show_table(entity, headers, data, self.delete_income if entity == "Income" else self.delete_expense if entity == "Expense" else self.delete_budget)

    def show_report_form(self):
        year = simpledialog.askinteger("Input", "Enter year:")
        month = simpledialog.askinteger("Input", "Enter month (1-12):")
        if year and month:
            report = self.data_service.generate_monthly_report(year, month)
            self.show_report(report)

    def show_report(self, report):
        # Afișare în terminal
        report_text = (
            f"Report for {report['month']}/{report['year']}:\n"
            f"Total Income: {report['total_income']}\n"
            f"Total Expenses: {report['total_expense']}\n"
            f"Savings: {report['savings']}"
        )
        messagebox.showinfo("Monthly Report", report_text)

        # Vizualizare grafică
        self.plot_report(report)

    def plot_report(self, report):
        labels = ["Total Income", "Total Expenses", "Savings"]
        values = [report["total_income"], report["total_expense"], report["savings"]]

        plt.figure(figsize=(8, 6))
        plt.bar(labels, values, color=["green", "red", "blue"])
        plt.title(f"Financial Report for {report['month']}/{report['year']}")
        plt.ylabel("Amount")
        plt.show()

    def show_notifications(self):
        notifications = []
        notifications.extend(self.data_service.check_budget_exceed())
        notifications.extend(self.data_service.detect_unusual_expenses())

        if notifications:
            messagebox.showinfo("Notifications", "\n".join(notifications))
        else:
            messagebox.showinfo("Notifications", "No alerts or unusual expenses.")