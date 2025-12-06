import datetime
import os

DATA_FILE = 'expenses.txt'

def ensure_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w'):
            pass

def read_all():
    ensure_file()
    records = []
    with open(DATA_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) < 5:
                continue
            rec = {
                'id': int(parts[0]),
                'name': parts[1],
                'amount': int(parts[2]),
                'category': parts[3],
                'date': parts[4]
            }
            records.append(rec)
    return records

def write_all(records):
    with open(DATA_FILE, 'w') as f:
        for r in records:
            f.write(f"{r['id']},{r['name']},{r['amount']},{r['category']},{r['date']}\n")

def get_next_id(records):
    if not records:
        return 1
    return max(r['id'] for r in records) + 1

def add_expense():
    records = read_all()
    nid = get_next_id(records)

    name = input('Enter expense name: ').strip()

    while True:
        amt = input('Enter amount (numbers only): ').strip()
        if amt.isdigit():
            amt = int(amt)
            break
        else:
            print('Invalid amount. Try again.')

    category = input('Enter category (Food/Travel/Other): ').strip()
    date_in = input('Enter date (YYYY-MM-DD) [leave empty for today]: ').strip()

    if not date_in:
        date_str = str(datetime.date.today())
    else:
        try:
            d = datetime.datetime.strptime(date_in, '%Y-%m-%d').date()
            date_str = str(d)
        except ValueError:
            print('Invalid date. Using today.')
            date_str = str(datetime.date.today())

    new_rec = {
        'id': nid,
        'name': name,
        'amount': amt,
        'category': category,
        'date': date_str
    }

    records.append(new_rec)
    write_all(records)
    print('\nExpense added successfully!\n')

def view_expenses():
    records = read_all()
    if not records:
        print('\nNo expenses found.\n')
        return

    print('\n--- All Expenses ---')
    print('ID | Name | Amount | Category | Date')
    for r in records:
        print(f"{r['id']} | {r['name']} | ₹{r['amount']} | {r['category']} | {r['date']}")
    print('')

def delete_expense():
    records = read_all()
    if not records:
        print('\nNo expenses to delete.\n')
        return

    view_expenses()

    try:
        did = int(input('Enter ID to delete: ').strip())
    except ValueError:
        print('Invalid ID.')
        return

    new_records = [r for r in records if r['id'] != did]

    if len(new_records) == len(records):
        print('ID not found.')
    else:
        write_all(new_records)
        print('Expense deleted successfully.')

def total_expenses():
    records = read_all()
    total = sum(r['amount'] for r in records)
    print(f"\nTotal Expenses: ₹{total}\n")

def category_summary():
    records = read_all()
    if not records:
        print('\nNo data.\n')
        return

    summary = {}
    for r in records:
        summary[r['category']] = summary.get(r['category'], 0) + r['amount']

    print('\n--- Category-wise Summary ---')
    for cat, amt in summary.items():
        print(f"{cat} : ₹{amt}")
    print('')

def monthly_summary(year=None, month=None):
    records = read_all()

    if year is None or month is None:
        today = datetime.date.today()
        year, month = today.year, today.month

    total = 0
    for r in records:
        try:
            d = datetime.datetime.strptime(r['date'], '%Y-%m-%d').date()
            if d.year == year and d.month == month:
                total += r['amount']
        except:
            continue

    print(f"\nTotal for {year}-{str(month).zfill(2)} : ₹{total}\n")

def main_menu():
    while True:
        print('1. Add Expense')
        print('2. View Expenses')
        print('3. Delete Expense')
        print('4. Total Expenses')
        print('5. Category Summary')
        print('6. Monthly Summary')
        print('7. Exit')

        choice = input('Enter choice: ').strip()

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            delete_expense()
        elif choice == '4':
            total_expenses()
        elif choice == '5':
            category_summary()
        elif choice == '6':
            monthly_summary()
        elif choice == '7':
            print('Goodbye!')
            break
        else:
            print('Invalid choice. Try again.')

if __name__ == '__main__':
    main_menu()
