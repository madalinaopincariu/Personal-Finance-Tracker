from tkinter import Tk
from ui.finance_gui import FinanceApp

def main():
    # Create the root window for Tkinter
    root = Tk()
    app = FinanceApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
