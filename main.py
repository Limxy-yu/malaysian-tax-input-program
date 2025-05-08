# main.py

import functions
import pandas as pd

FILENAME = 'tax_records.csv'

# In-memory user storage during session
registered_users = {}

def display_menu():
    print("\n" + "-" * 36)
    print("  WELCOME TO MALAYSIA TAX PROGRAM  ")
    print("-" * 36)
    print("1. Register")
    print("2. Login")
    print("3. View all the tax records")
    print("4. Exit")

def register_user():
    print("\n--- User Registration ---")
    ic_number = input("Enter your 12-digit IC number: ")
    while len(ic_number) != 12 or not ic_number.isdigit():
        print("Invalid IC number. Please enter a 12-digit number.")
        ic_number = input("Enter your 12-digit IC number: ")

    user_id = input("Create a User ID: ")
    registered_users[user_id] = ic_number
    print("Registration successful! Please login to continue.")

def login_user():
    print("\n--- User Login ---")
    user_id = input("Enter your User ID: ")
    password = input("Enter your password (last 4 digits of IC): ")

    if user_id in registered_users:
        ic_number = registered_users[user_id]
        if functions.verify_user(ic_number, password):
            print("Login successful!")
            return user_id, ic_number
        else:
            print("Incorrect password.")
    else:
        print("User ID not found.")
    return None, None

def view_tax_records():
    records = functions.read_from_csv(FILENAME)
    if records is not None and not records.empty:
        print("\n--- Tax Records ---")
        print(records.to_string(index=False))
    else:
        print("No tax records found.")

def main():
    # Preload users from CSV if any
    data = functions.read_from_csv(FILENAME)
    if data is not None:
        for _, row in data.iterrows():
            registered_users[row['IC Number']] = row['IC Number']

    while True:
        display_menu()
        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            register_user()
        elif choice == '2':
            user_id, ic_number = login_user()
            if user_id is None:
                continue
            try:
                income = float(input("Enter your annual income (RM): "))
                tax_relief = float(input("Enter your total tax relief (RM): "))
            except ValueError:
                print("Invalid input. Please enter numbers.")
                continue

            tax_payable = functions.calculate_tax(income, tax_relief)
            print(f"\nYour calculated tax payable is: RM {tax_payable}")

            user_data = {
                'IC Number': ic_number,
                'Annual Income': income,
                'Tax Relief': tax_relief,
                'Tax Payable': tax_payable
            }
            functions.save_to_csv(user_data, FILENAME)
            print("Your data has been saved successfully!")

        elif choice == '3':
            view_tax_records()
        elif choice == '4':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
