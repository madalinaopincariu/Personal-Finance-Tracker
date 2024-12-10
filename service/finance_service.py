from repository.data_manager import DataManager
from domain.income import Income
from domain.expense import Expense
from domain.budget import Budget

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
