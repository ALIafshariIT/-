import sqlite3
from tkinter import *
from tkinter import messagebox

# اتصال به پایگاه داده
#کلی یکجا قرار داده شده
class Database:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS persons ( id INTEGER PRIMARY KEY,name TEXT,lname TEXT,national_id TEXT,phone TEXT,address TEXT
            )
        ''')
        self.con.commit()

    def insert(self, name, lname, national_id, phone, address):
        self.cur.execute('INSERT INTO persons VALUES (NULL,?,?,?,?,?)',
                         (name, lname, national_id, phone, address))
        self.con.commit()

    def delete(self, id):
        self.cur.execute('DELETE FROM persons WHERE id=?', (id,))
        self.con.commit()

    def update(self, id, name, lname, national_id, phone, address):
        self.cur.execute('''
            UPDATE persons SET name=?, lname=?, national_id=?, phone=?, address=? WHERE id=?
        ''', (name, lname, national_id, phone, address, id))
        self.con.commit()

    def search(self, keyword):
        self.cur.execute('''
            SELECT * FROM persons WHERE name LIKE ? OR lname LIKE ? OR national_id LIKE ?
        ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
        return self.cur.fetchall()

    def fetch_all(self):
        self.cur.execute('SELECT * FROM persons')
        return self.cur.fetchall()

db = Database('f:/text.db')

#  (ui)رابط کاربری
win = Tk()
win.geometry("1000x600")
win.title("مدیریت اطلاعات")
win.configure(bg="#f0f0f0")

# لیبل‌ها
Label(win,text="*",fg="red").place(x=840, y=50)
Label(win, text=":نام", font="arial 16").place(x=800, y=50)
Label(win,text="*",fg="red").place(x=900, y=90)
Label(win, text=" :نام خانوادگی", font="arial 16").place(x=800, y=90)
Label(win, text=":شماره ملی", font="arial 16").place(x=800, y=130)
Label(win, text=":شماره تماس", font="arial 16").place(x=800, y=170)
Label(win, text=" :آدرس", font="arial 16").place(x=800, y=210)

# ورودی‌ها
ent_name = Entry(win, font="arial 16")
ent_name.place(x=400, y=50)

ent_lname = Entry(win, font="arial 16")
ent_lname.place(x=400, y=90)

ent_nid = Entry(win, font="arial 16")
ent_nid.place(x=400, y=130)

ent_phone = Entry(win, font="arial 16")
ent_phone.place(x=400, y=170)

ent_address = Entry(win, font="arial 16")
ent_address.place(x=400, y=210)

ent_search = Entry(win, font="arial 16")
ent_search.place(x=400, y=260)

scrollbar=Scrollbar(win ,width=20 )
scrollbar.pack(side=RIGHT,fill=X )




listbox = Listbox(win, width=80, height=10, font="arial 12")
listbox.place(x=100, y=320 )

scrollbar.config(command=listbox.yview)
# توابع
def add():
    name = ent_name.get()
    lname = ent_lname.get()
    nid = ent_nid.get()
    phone = ent_phone.get()
    address = ent_address.get()
    if name == "":
        messagebox.showerror("خطا", "نام نمی‌تواند خالی باشد")
        return
    db.insert(name, lname, nid, phone, address)
    messagebox.showinfo("ثبت", "اطلاعات ثبت شد")
    clear()
    show()

def delete():
    try:
        index = listbox.curselection()[0]
        data = listbox.get(index)
        db.delete(data.split()[0])
        listbox.delete(index)
    except:
        messagebox.showerror("خطا", "لطفاً یک رکورد را انتخاب کنید")

def update():
    try:
        index = listbox.curselection()[0]
        data = listbox.get(index).split()
        db.update(data[0], ent_name.get(), ent_lname.get(), ent_nid.get(), ent_phone.get(), ent_address.get())
        messagebox.showinfo("ویرایش", "اطلاعات ویرایش شد")
        clear()
        show()
    except:
        messagebox.showerror("خطا", "لطفاً یک رکورد را انتخاب کنید")

def search():
    keyword = ent_search.get()
    results = db.search(keyword)
    listbox.delete(0, END)
    for r in results:
        listbox.insert(END, f"{r[0]} {r[1]} {r[2]} {r[3]} {r[4]} {r[5]}")

def show():
    listbox.delete(0, END)
    for r in db.fetch_all():
        listbox.insert(END, f"{r[0]} {r[1]} {r[2]} {r[3]} {r[4]} {r[5]}")

def clear():
    ent_name.delete(0, END)
    ent_lname.delete(0, END)
    ent_nid.delete(0, END)
    ent_phone.delete(0, END)
    ent_address.delete(0, END)
    ent_search.delete(0, END)
#(بدون اسم) دکمه‌ها
Button(win, text="جدید", font="arial 14", command=add).place(x=100, y=50)
Button(win, text="پاک", font="arial 14", command=clear).place(x=100, y=90)
Button(win, text="ویرایش", font="arial 14", command=update).place(x=100, y=130)
Button(win, text="حذف", font="arial 14", command=delete).place(x=100, y=170)
Button(win, text="خروج", font="arial 14", command=win.quit).place(x=100, y=210)
Button(win, text="نمایش", font="arial 14", command=show).place(x=100, y=260)
Button(win, text="جست و جو", font="arial 14", command=search).place(x=800, y=260)

win.mainloop()