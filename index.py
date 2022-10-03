from tkinter import *
import sqlite3
from tkinter.ttk import Treeview

dbName = "database.db"

#database

def runQuery(name, query, parameters = ()):

    with sqlite3.connect(name) as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, parameters)
        conn.commit()

    return result

def getProducts(name):

    query = 'SELECT * FROM product ORDER BY name DESC'
    dbRows = runQuery(name, query)
    print(dbRows)

root = Tk()
root.title("Products Application")

#container
frame = LabelFrame(root, text="Register a new product")
frame.grid(row= 0, columnspan=3, pady=20)

#Name Input
nameInput = Label(frame, text="Name: ").grid(row=1, column=0)
name = Entry(frame)
name.grid(row=1, column=1)
name.focus()

#price Input
priceInput = Label(frame, text="Price: ").grid(row=2, column=0)
price = Entry(frame)
price.grid(row=2, column=1)

#Button add Product
btn = Button(frame, text='Save Product')
btn.grid(row=3, columnspan=2, sticky= W + E)


#table
table = Treeview(height=10, columns=2)
table.grid(row=4, column=0, columnspan=2)
table.heading('#0', text="Name", anchor=CENTER)
table.heading('#1', text="Price", anchor=CENTER)

getProducts(dbName)

root.mainloop()