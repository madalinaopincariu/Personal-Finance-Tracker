from repository.data_manager import DataManager
from domain.income import Income
from domain.expense import Expense
from domain.budget import Budget
from datetime import datetime
import tkinter.messagebox as MessageBox

class DataService:
    def __init__(self):
        self.data_manager = DataManager()
    
    def _validate_positive_float(self, value):
        if not isinstance(value, (float, int)) or value <= 0:
            raise ValueError("Amount must be a positive number.")

    def _validate_date(self, date):
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            if date_obj > datetime.today():
                raise ValueError("Date cannot be in the future.")
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")

    def _show_error(self, message):
        MessageBox.showerror("Validation Error", message)

    def create_income(self, source, amount, date, description):
        self._validate_positive_float(amount)
        self._validate_date(date)
        income = Income(self._generate_id(self.data_manager.load_incomes()), source, amount, date, description)
        self.data_manager.create_income(income)

    def update_income(self, income_id, source, amount, date, description):
        self._validate_positive_float(amount)
        self._validate_date(date)
        updated_income = Income(income_id, source, amount, date, description)
        self.data_manager.update_income(income_id, updated_income)

    def create_expense(self, category, amount, date, description):
        self._validate_positive_float(amount)
        self._validate_date(date)
        expense = Expense(self._generate_id(self.data_manager.load_expenses()), category, amount, date, description)
        self.data_manager.create_expense(expense)

    def update_expense(self, expense_id, category, amount, date, description):
        self._validate_positive_float(amount)
        self._validate_date(date)
        updated_expense = Expense(expense_id, category, amount, date, description)
        self.data_manager.update_expense(expense_id, updated_expense)

    def create_budget(self, category, amount):
        self._validate_positive_float(amount)
        budget = Budget(self._generate_id(self.data_manager.load_budgets()), category, amount)
        self.data_manager.create_budget(budget)

    def update_budget(self, budget_id, category, amount):
        self._validate_positive_float(amount)
        updated_budget = Budget(budget_id, category, amount)
        self.data_manager.update_budget(budget_id, updated_budget)

    # Income CRUD
    """def create_income(self, source, amount, date, description):
        income = Income(self._generate_id(self.data_manager.load_incomes()), source, amount, date, description)
        self.data_manager.create_income(income)

    def update_income(self, income_id, source, amount, date, description):
        updated_income = Income(income_id, source, amount, date, description)
        self.data_manager.update_income(income_id, updated_income)"""

    def delete_income(self, income_id):
        self.data_manager.delete_income(income_id)

    def get_incomes(self):
        return self.data_manager.load_incomes()

    # Expense CRUD
    """def create_expense(self, category, amount, date, description):
        expense = Expense(self._generate_id(self.data_manager.load_expenses()), category, amount, date, description)
        self.data_manager.create_expense(expense)

    def update_expense(self, expense_id, category, amount, date, description):
        updated_expense = Expense(expense_id, category, amount, date, description)
        self.data_manager.update_expense(expense_id, updated_expense)"""

    def delete_expense(self, expense_id):
        self.data_manager.delete_expense(expense_id)

    def get_expenses(self):
        return self.data_manager.load_expenses()

    # Budget CRUD
    """def create_budget(self, category, amount):
        budget = Budget(self._generate_id(self.data_manager.load_budgets()), category, amount)
        self.data_manager.create_budget(budget)

    def update_budget(self, budget_id, category, amount):
        updated_budget = Budget(budget_id, category, amount)
        self.data_manager.update_budget(budget_id, updated_budget)"""

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

    def check_budget_exceed(self):
        budgets = self.get_budgets()
        expenses = self.get_expenses()
        notifications = []

        budget_dict = {budget.category: budget.amount for budget in budgets}
        category_totals = {}

    # Calculează totalul cheltuielilor pe fiecare categorie
        for expense in expenses:
            if expense.category not in category_totals:
                category_totals[expense.category] = 0
            category_totals[expense.category] += expense.amount

    # Verifică dacă totalul cheltuielilor depășește bugetul alocat
        for category, total in category_totals.items():
            if category in budget_dict:
                budget = budget_dict[category]
                if total > budget:  # Verifică dacă cheltuielile depășesc complet bugetul
                    notifications.append(f"Alert: You have exceeded the budget in category '{category}'.")

        return notifications

    def detect_unusual_expenses(self):
        expenses = self.get_expenses()
        category_totals = {}

    # Obține bugetele din funcția ta de obținere a bugetelor
        budgets = self.get_budgets()

    # Creează un dicționar cu totalul cheltuielilor pe fiecare categorie
        for expense in expenses:
            if expense.category not in category_totals:
                category_totals[expense.category] = 0
            category_totals[expense.category] += expense.amount

    # Creează un dicționar cu bugetele pe fiecare categorie
        budget_dict = {budget.category: budget.amount for budget in budgets}

    # Detectează depășirea a 90% din buget și adaugă notificări
        notifications = []

        for category, total in category_totals.items():
        # Verifică dacă s-a cheltuit 90% sau mai mult din bugetul alocat pentru categoria respectivă
            if category in budget_dict:
                budget = budget_dict[category]
                if budget > 0 and total >= budget * 0.9 and total < budget:  # 90% din buget
                    notifications.append(f"Warning: You have spent 90% or more of your budget in the '{category}' category.")

        return notifications