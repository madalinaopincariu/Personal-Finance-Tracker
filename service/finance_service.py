from repository.data_manager import DataManager
from domain.income import Income
from domain.expense import Expense
from domain.budget import Budget
from datetime import datetime

class DataService:
    def __init__(self):
        self.data_manager = DataManager()

    # Income CRUD
    def create_income(self, source, amount, date, description):
        income = Income(self._generate_id(self.data_manager.load_incomes()), source, amount, date, description)
        self.data_manager.create_income(income)

    def update_income(self, income_id, source, amount, date, description):
        updated_income = Income(income_id, source, amount, date, description)
        self.data_manager.update_income(income_id, updated_income)

    def delete_income(self, income_id):
        self.data_manager.delete_income(income_id)

    def get_incomes(self):
        return self.data_manager.load_incomes()

    # Expense CRUD
    def create_expense(self, category, amount, date, description):
        expense = Expense(self._generate_id(self.data_manager.load_expenses()), category, amount, date, description)
        self.data_manager.create_expense(expense)

    def update_expense(self, expense_id, category, amount, date, description):
        updated_expense = Expense(expense_id, category, amount, date, description)
        self.data_manager.update_expense(expense_id, updated_expense)

    def delete_expense(self, expense_id):
        self.data_manager.delete_expense(expense_id)

    def get_expenses(self):
        return self.data_manager.load_expenses()

    # Budget CRUD
    def create_budget(self, category, amount):
        budget = Budget(self._generate_id(self.data_manager.load_budgets()), category, amount)
        self.data_manager.create_budget(budget)

    def update_budget(self, budget_id, category, amount):
        updated_budget = Budget(budget_id, category, amount)
        self.data_manager.update_budget(budget_id, updated_budget)

    def delete_budget(self, budget_id):
        self.data_manager.delete_budget(budget_id)

    def get_budgets(self):
        return self.data_manager.load_budgets()

    # Helper to generate new ID
    def _generate_id(self, data_list):
        if not data_list:
            return 1
        return max(item.id for item in data_list) + 1
    
        # Filtering by attribute
    def filter_incomes(self, key, value):
        return [income for income in self.get_incomes() if getattr(income, key) == value]

    def filter_expenses(self, key, value):
        return [expense for expense in self.get_expenses() if getattr(expense, key) == value]

    def filter_budgets(self, key, value):
        return [budget for budget in self.get_budgets() if getattr(budget, key) == value]

    # Searching by attribute
    def search_incomes(self, key, query):
        return [income for income in self.get_incomes() if query.lower() in str(getattr(income, key)).lower()]

    def search_expenses(self, key, query):
        return [expense for expense in self.get_expenses() if query.lower() in str(getattr(expense, key)).lower()]

    def search_budgets(self, key, query):
        return [budget for budget in self.get_budgets() if query.lower() in str(getattr(budget, key)).lower()]

    # Sorting by attribute
    def sort_incomes(self, key, reverse=False):
        return sorted(self.get_incomes(), key=lambda income: getattr(income, key), reverse=reverse)

    def sort_expenses(self, key, reverse=False):
        return sorted(self.get_expenses(), key=lambda expense: getattr(expense, key), reverse=reverse)

    def sort_budgets(self, key, reverse=False):
        return sorted(self.get_budgets(), key=lambda budget: getattr(budget, key), reverse=reverse)
    
    def generate_monthly_report(self, year, month):
        incomes = self.get_incomes()
        expenses = self.get_expenses()

        # Filtrare venituri și cheltuieli pentru luna specificată
        monthly_incomes = [income for income in incomes if self._is_in_month(income.date, month, year)]
        monthly_expenses = [expense for expense in expenses if self._is_in_month(expense.date, month, year)]

        total_income = sum(income.amount for income in monthly_incomes)
        total_expense = sum(expense.amount for expense in monthly_expenses)
        savings = total_income - total_expense

        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "savings": savings,
            "month": month,
            "year": year
        }

    def _is_in_month(self, date_obj, month, year):
        if date_obj is None:
            print("Date is None")
            return False
 
        print(f"Checking date: {date_obj}, month: {month}, year: {year}")
        return date_obj.year == year and date_obj.month == month
