#!/usr/bin/env python3
"""Write a small CSV of made-up transactions for trying the Sure CSV import.

All names and amounts are invented. The dates fall in the current month by
default, so the rows show up in this month's budget.

Usage:
  python3 make_transactions_csv.py                 # writes transactions-<YYYY-MM>.csv
  python3 make_transactions_csv.py --month 2026-11 # pick a month
  python3 make_transactions_csv.py -o my.csv       # pick the file name
"""
import argparse
import csv
import datetime

ROWS = [  # (day, name, amount, category, notes)
    (1, "Paycheck - Example Employer", "3200.00", "Income", "Monthly salary"),
    (2, "Rent - Maple Street Apartment", "-1350.00", "Mortgage / Rent", "Monthly rent"),
    (3, "Green Basket Grocery", "-86.40", "Groceries", "Weekly groceries"),
    (5, "City Power and Light", "-74.20", "Utilities", "Electric bill"),
    (6, "Corner Coffee", "-4.75", "Food & Drink", ""),
    (7, "Metro Transit Pass", "-55.00", "Transportation", "Monthly pass"),
    (9, "Green Basket Grocery", "-92.15", "Groceries", "Weekly groceries"),
    (10, "Streaming Service", "-12.99", "Subscriptions", ""),
    (11, "Corner Coffee", "-5.25", "Food & Drink", ""),
    (12, "Movie Night Cinema", "-24.00", "Entertainment", "Two tickets"),
    (13, "Gym Membership", "-35.00", "Sports & Fitness", ""),
    (14, "Green Basket Grocery", "-78.60", "Groceries", "Weekly groceries"),
]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--month", help="YYYY-MM (default: current month)")
    p.add_argument("-o", "--output", help="output file (default: transactions-<YYYY-MM>.csv)")
    a = p.parse_args()
    if a.month:
        year, month = (int(x) for x in a.month.split("-"))
    else:
        today = datetime.date.today()
        year, month = today.year, today.month
    out = a.output or f"transactions-{year:04d}-{month:02d}.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["Date", "Name", "Amount", "Category", "Notes"])
        for day, name, amount, category, notes in ROWS:
            w.writerow([datetime.date(year, month, day).isoformat(), name, amount, category, notes])
    print(f"wrote {len(ROWS)} rows to {out}")


if __name__ == "__main__":
    main()
