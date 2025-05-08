# functions.py

import pandas as pd
import os

def verify_user(ic_number, password):
    """
    Verifies the IC number is 12 digits and password matches the last 4 digits of IC.
    """
    return len(ic_number) == 12 and password == ic_number[-4:]

def calculate_tax(income, tax_relief):
    """
    Calculates the tax payable based on Malaysia's YA 2024 progressive tax rates.
    """
    brackets = [
        (5000, 0.00),
        (15000, 0.01),
        (15000, 0.03),
        (15000, 0.06),
        (20000, 0.11),
        (30000, 0.19),
        (150000, 0.25),
        (150000, 0.26),
        (200000, 0.28),
        (400000, 0.30),
        (float('inf'), 0.30)  # above 1,000,000
    ]

    chargeable_income = income - tax_relief
    if chargeable_income <= 0:
        return 0.0

    tax = 0.0
    remaining = chargeable_income

    for bracket in brackets:
        bracket_amount = min(remaining, bracket[0])
        tax += bracket_amount * bracket[1]
        remaining -= bracket_amount
        if remaining <= 0:
            break

    return round(tax, 2)

def save_to_csv(data, filename):
    """
    Saves the user's tax data to a CSV file using pandas.
    If the file doesn't exist, it creates it with a header.
    """
    df_new = pd.DataFrame([data])
    if os.path.exists(filename):
        df_existing = pd.read_csv(filename)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_csv(filename, index=False)
    else:
        df_new.to_csv(filename, index=False)

def read_from_csv(filename):
    """
    Reads and prints the tax data from CSV using pandas.
    If the file doesn't exist, it prints an error message.
    """
    if not os.path.exists(filename):
        print("No records found.")
        return

    df = pd.read_csv(filename)
    print("\n📄 Tax Records:")
    print(df.to_string(index=False))
