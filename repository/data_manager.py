import csv
from domain.income import Income
from domain.expense import Expense
from domain.budget import Budget
from datetime import datetime 

class DataManager:
    def __init__(self):
        self.income_file = "data/incomes.csv"
        self.expense_file = "data/expenses.csv"
        self.budget_file = "data/budgets.csv"

    # Load data
    def load_incomes(self):
        incomes = []
        try:
            with open(self.income_file, mode='r', newline='') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if row:
                        date_obj = datetime.strptime(row[3], '%Y-%m-%d').date() if row[3] else None
                        incomes.append(Income(int(row[0]), row[1], float(row[2]), date_obj, row[4]))
        except FileNotFoundError:
            print(f"{self.income_file} not found.")
        return incomes

    def load_expenses(self):
        expenses = []
        try:
            with open(self.expense_file, mode='r', newline='') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if row:
                        date_obj = datetime.strptime(row[3], '%Y-%m-%d').date() if row[3] else None
                        expenses.append(Expense(int(row[0]), row[1], float(row[2]), date_obj, row[4]))
        except FileNotFoundError:
            print(f"{self.expense_file} not found.")
        return expenses

    def load_budgets(self):
        budgets = []
        try:
            with open(self.budget_file, mode='r', newline='') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if row:
                        budgets.append(Budget(int(row[0]), row[1], float(row[2])))
        except FileNotFoundError:
            print(f"{self.budget_file} not found.")
        return budgets

    # Save data
    def save_incomes(self, incomes):
        with open(self.income_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["id", "source", "amount", "date", "description"])  # Header row
            for income in incomes:
                writer.writerow([income.id, income.source, income.amount, income.date, income.description])

    def save_expenses(self, expenses):
        with open(self.expense_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["id", "category", "amount", "date", "description"])  # Header row
            for expense in expenses:
                writer.writerow([expense.id, expense.category, expense.amount, expense.date, expense.description])

    def save_budgets(self, budgets):
        with open(self.budget_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["id", "category", "amount"])  # Header row
            for budget in budgets:
                writer.writerow([budget.id, budget.category, budget.amount])

    # CRUD Operations for Income
    def create_income(self, income):
        incomes = self.load_incomes()
        incomes.append(income)
        self.save_incomes(incomes)

    def update_income(self, income_id, updated_income):
        incomes = self.load_incomes()
        for i, income in enumerate(incomes):
            if income.id == income_id:
                incomes[i] = updated_income
                break
        self.save_incomes(incomes)

    def delete_income(self, income_id):
        incomes = self.load_incomes()
        incomes = [income for income in incomes if income.id != income_id]
        self.save_incomes(incomes)

    # CRUD Operations for Expense
    def create_expense(self, expense):
        expenses = self.load_expenses()
        expenses.append(expense)
        self.save_expenses(expenses)

    def update_expense(self, expense_id, updated_expense):
        expenses = self.load_expenses()
        for i, expense in enumerate(expenses):
            if expense.id == expense_id:
                expenses[i] = updated_expense
                break
        self.save_expenses(expenses)

    def delete_expense(self, expense_id):
        expenses = self.load_expenses()
        expenses = [expense for expense in expenses if expense.id != expense_id]
        self.save_expenses(expenses)

    # CRUD Operations for Budget
    def create_budget(self, budget):
        budgets = self.load_budgets()
        budgets.append(budget)
        self.save_budgets(budgets)

    def update_budget(self, budget_id, updated_budget):
        budgets = self.load_budgets()
        for i, budget in enumerate(budgets):
            if budget.id == budget_id:
                budgets[i] = updated_budget
                break
        self.save_budgets(budgets)

    def delete_budget(self, budget_id):
        budgets = self.load_budgets()
        budgets = [budget for budget in budgets if budget.id != budget_id]
        self.save_budgets(budgets)
