# libraries
import os
import csv
from datetime import datetime
from colorama import Fore,Style,init
init(autoreset=True)

# Set the base directory for the application
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, 'expenses.txt')
file_path_csv = os.path.join(BASE_DIR, 'expenses.csv')

# Initialize the list to store expenses
expenses = []

# Define the list of categories
categories = [
    "Food",
    "Transport",
    "Bills",
    "Shopping",
    "Health",
    "Education",
    "Entertainment",
    "Other"
]

# _________________________function to display the menu__________________________
def menu_display():
    print(Fore.GREEN +'----Personal Expense Tracker----')
    print('select an option:')
    print('1. Add Expense')
    print('2. View Expenses')
    print('3. View Total Expenses')
    print('4. Filter Expenses by Category')
    print('5. Category-wise Expense Summary')
    print('6. Delete Expense')
    print('7. Update Expense')
    print('8. Save Expenses to CSV')
    print('9. Exit')
    print(Fore.GREEN +'--------------------------------')
    
# _________________________function to generate a unique ID for each expense__________________________
def id_generator():
    if len(expenses) == 0:
        return 1
    highest_ID = 0
    for expense in expenses:
        if expense['id'] > highest_ID:
            highest_ID = expense['id']
    return highest_ID + 1

# _________________________function to add an expense__________________________
def add_expense():
    expense_id = id_generator()
    while True:
        try:
            ammount = float(input('Enter the expense amount: '))
            if ammount < 0:
                print(Fore.YELLOW +'Ammount must be greater then 0.')
                continue
            break
        except ValueError:
            print(Fore.RED +'Invalid input. Please enter a valid number.')
    print(Fore.MAGENTA +'Select a category:')
    count = 1
    for category in categories:
        print(Fore.CYAN +f'{count}. {category}')
        count += 1
    while True:
        try:
            category_choice = int(input('Enter the category number: '))
            if category_choice < 1 or category_choice > len(categories):
                print(Fore.RED +'Invalid choice. Please select a valid category number.')
                continue
            category = categories[category_choice - 1]
            break
        except ValueError:
            print(Fore.RED +'Invalid input. Please enter a valid number.')
    disciption = input(Fore.CYAN +'Enter a description for the expense: ')
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    expense = {
        'id': expense_id,
        'amount': ammount,
        'category': category,
        'description': disciption,
        'date': formatted_time
    }
    expenses.append(expense)
    save_data()
    print(Fore.GREEN +'Expense added successfully.')

# _________________________function to view all expenses__________________________
def view_expenses():
    if not expenses:
        print(Fore.YELLOW +'No expenses recorded.')
        return
    print('='*76)
    print(Fore.MAGENTA +f'{"ID":<5}{"Amount":10}{"Category":15}{"Description":25}{"Date/Time":20}')
    print('='*76)
    for expense in expenses:
         print(f'{expense["id"]:<5}'
              f'{expense["amount"]:<10}'
              f'{expense["category"]:<15}'
              f'{expense["description"]:<25}'
              f'{expense["date"]:<20}')

    print(Fore.MAGENTA +'=' * 76)
        
# _________________________function to view total expenses__________________________
def view_total_expenses():
    if len(expenses) == 0:
        print(Fore.YELLOW +'No expenses recorded.')
        return
    total = 0
    print('='*27)
    print(Fore.MAGENTA +f'{"ID":<5}{"Amount":10}')
    print('='*27)
    for expense in expenses:
        id = expense['id']
        amount = expense['amount']
        total = total + amount
        print(f'{id:<5} : {amount}')
    print(f'Total Expenses: {total}')
    print(Fore.MAGENTA +'='*27)
# _________________________function to filter expenses by category__________________________

def filter_expenses_by_category():
    if not expenses:
        print(Fore.YELLOW +'No expenses recorded.')
        return
    category = input('Enter the category to filter by: ').strip().title()
    found = False
    print('='*76)
    print(Fore.MAGENTA +f'{"ID":<5}{"Amount":10}{"Category":15}{"Description":25}{"Date/Time":20}')
    print('='*76)
    for expense in expenses:
        if expense['category'] == category:
            print(f'{expense["id"]:<5}'
              f'{expense["amount"]:<10}'
              f'{expense["category"]:<15}'
              f'{expense["description"]:<25}'
              f'{expense["date"]:<20}')
            found = True
    print(Fore.MAGENTA +'=' * 76)
    if not found:
        print(Fore.YELLOW +f'No expenses found in the "{category}" category.')

# _________________________function to display category-wise expense summary__________________________
def category_wise_summary():
    if not expenses:
        print(Fore.YELLOW +'No expenses recorded.')
        return
    category_totals = {}
    for expense in expenses:
        category = expense['category']
        amount = expense['amount']
        if category in category_totals:
            category_totals[category] = category_totals[category] + amount
        else:
            category_totals[category] = amount
    for category, category_total in category_totals.items():
        print(f'{category:<15}: {category_total}')

# _________________________function to load expenses from a file__________________________
def load_data():
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line == '':
                    continue
                parts = line.split(',')
                expense = {
                    'id': int(parts[0]),
                    'amount': float(parts[1]),
                    'category': parts[2],
                    'description': parts[3],
                    'date': parts[4]
                }
                expenses.append(expense)
    except FileNotFoundError:
        print(Fore.YELLOW +'No previous expense data found. Starting fresh.')
    except Exception as e:
        print(Fore.RED +f'Error occurred while loading data: {e}')

# _________________________function to save expenses to a file__________________________
def save_data():
    try:
        with open(file_path, 'w') as file:
            for expense in expenses:
                id = expense['id']
                amount = expense['amount']
                category = expense['category']
                description = expense['description']
                date_time = expense['date']
                line = f'{id},{amount},{category},{description},{date_time}\n'
                file.write(line)
    except Exception as e:
        print(Fore.RED +f'Error occurred while saving data: {e}')

# _________________________function to delete an expense by ID__________________________
def delete_expense():
    if not expenses:
        print(Fore.YELLOW +'No expenses recorded.')
        return
    try:
        expense_id = int(input('Enter the ID of the expense to delete: '))
        found = False
        for expense in expenses:
            if expense['id'] == expense_id:
                expenses.remove(expense)
                save_data()
                print(Fore.GREEN +f'Expense with ID {expense_id} deleted successfully.')
                found = True
                break
        if not found:
            print(Fore.YELLOW +f'Expense with ID {expense_id} not found.')
    except ValueError:
        print(Fore.RED +'Invalid input. Please enter a valid number.')
    except Exception as e:
        print(Fore.RED +f'Error occurred while deleting expense: {e}')

# _________________________function to save expenses to a CSV__________________________
def save_data_csv():
    try:
        with open(file_path_csv, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Amount', 'Category', 'Description', 'Date/Time'])
            for expense in expenses:
                id = expense['id']
                amount = expense['amount']
                category = expense['category']
                description = expense['description']
                date_time = expense['date']
                line = [id, amount, category, description, date_time]
                writer.writerow(line)
    except Exception as e:
        print(Fore.RED +f'Error occurred while saving data: {e}')

# _________________________function to update an expense by ID__________________________
def update_expense():
    if not expenses:
        print(Fore.YELLOW +'No expenses recorded.')
        return
    try:
        print(Fore.MAGENTA +'='*28,'Availible Expenses','='*28)
        view_expenses()
        expense_id = int(input('Enter the ID of the expense to update: '))
        found = False
        for expense in expenses:
            if expense['id'] == expense_id:
                found = True
                print(Fore.GREEN +'----Update Expense----')
                print(Fore.CYAN +'Select the field to update:')
                print('1. Amount')
                print('2. Category')
                print('3. Description')
                print('4. Cancel')
                choice = input('Enter your choice (1-4): ')
                # Uptade amount
                if choice == '1':
                    while True:
                        try:
                            new_amount = float(input('Enter the new amount: '))
                            if new_amount <= 0:
                                print(Fore.RED +'Amount must be greater than 0.')
                                continue
                            expense['amount'] = new_amount
                            save_data()
                            print(Fore.GREEN +'Expense updated successfully.')
                            break
                        except ValueError:
                            print(Fore.RED +'Invalid input. Please enter a valid number.')
                        return
                # Update category
                elif choice == '2':
                    while True:
                        new_category = input('Enter the new category: ').strip().title()
                        if new_category not in categories:
                            print(Fore.RED +'Invalid category. Please choose from the following:\n' 
                                  f'{", ".join(categories)}')
                            continue
                        expense['category'] = new_category
                        save_data()
                        print(Fore.GREEN +'Expense updated successfully.')
                        return
                # update description
                elif choice == '3':
                    new_description = input('Enter the new description: ')
                    expense['description'] = new_description
                    save_data()
                    print(Fore.GREEN +'Expense updated successfully.')
                    return
                # Cancel
                elif choice == '4':
                    return
                else:
                    print(Fore.RED +'Invalid choice. Please enter a number between 1 and 4.')
        if not found:
            print(Fore.YELLOW +f'Expense with ID {expense_id} not found.')
    except ValueError:
        print(Fore.RED +'Invalid input. Please enter a valid number.')
    except Exception as e:
        print(Fore.RED +f'Error occurred while updating expense: {e}')


# _________________________main function to run the program__________________________
def main():
    load_data()
    # main loop to display the menu and handle user input
    while True:
        menu_display()
        try:
            choice = int(input('Enter your choice (1-9): '))

            # Add Expense
            if choice == 1:
                a = ''
                while True:
                    print(Fore.MAGENTA +'----Add Expense----')
                    add_expense()
                    a = input('Enter "e" to exit or any other key to add another expense: ')    
                    if a == 'e':
                        break
            
            # View Expenses
            elif choice == 2:
                    print(Fore.MAGENTA +'----View Expenses----')
                    view_expenses()
            
            # View Total Expenses
            elif choice == 3:
                    print(Fore.MAGENTA +'----View Total Expenses----')
                    view_total_expenses()
            
            # Filter Expenses by Category
            elif choice == 4:
                    print(Fore.MAGENTA +'----Filter Expenses by Category----')
                    filter_expenses_by_category()
            
            # Category-wise Expense Summary
            elif choice == 5:
                    print(Fore.MAGENTA +'----Category-wise Expense Summary----')
                    category_wise_summary()
            
            # Delete Expense
            elif choice == 6:
                    while True:
                        print(Fore.MAGENTA +'----Delete Expense----')
                        delete_expense()
                        a = input('Enter "e" to exit or any other key to delete another expense: ')    
                        if a == 'e':
                            break
            
            # Update Expense
            elif choice == 7:
                    while True:
                        print(Fore.MAGENTA +'----Update Expense----')
                        update_expense()
                        break
            
            # Export to CSV
            elif choice == 8:
                save_data_csv()
                print(Fore.GREEN +'Expenses exported to CSV successfully.')
            
            # Exit
            elif choice == 9:
                print(Fore.GREEN +'Exiting the program.')
                break
            else:
                print(Fore.YELLOW +'Feature is under development. Please select another option.')
        except ValueError:
            print(Fore.RED +'Invalid input. Please enter a number between 1 and 8.')

if __name__ == '__main__':
    main()