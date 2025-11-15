import sqlite3

# اتصال به پایگاه داده (اگر وجود نداشته باشد ایجاد می‌شود)
con = sqlite3.connect('E:/mydata.db')
cur = con.cursor()

# ایجاد جدول در صورت عدم وجود
query_create_table = '''
CREATE TABLE IF NOT EXISTS teacher (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fname TEXT,
    lname TEXT,
    salary INTEGER
)
'''
cur.execute(query_create_table)
con.commit()

# تابع درج داده در جدول
def insert_record(fname, lname, salary):
    cur.execute('INSERT INTO teacher (fname, lname, salary) VALUES (?, ?, ?)', (fname, lname, salary))
    con.commit()
    print('Record inserted')

# --- تست درج داده ---
# insert_record('reza', 'rezayee', 1500)

# --- درج چند رکورد از ورودی ---
# for i in range(3):
#     fname = input('Enter first name: ')
#     lname = input('Enter last name: ')
#     salary = int(input('Enter salary: '))
#     insert_record(fname, lname, salary)
