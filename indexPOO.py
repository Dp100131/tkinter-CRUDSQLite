from os import name
from tkinter import *
import sqlite3
from tkinter.messagebox import *
from tkinter.ttk import Treeview

class Product:

    #dbName
    dbName = "database.db"

    def __init__(self, window):

        #init
        self.root = window
        self.root.title('Product application')

        #container
        self.frame = LabelFrame(self.root, text="Register a new product")
        self.frame.grid(row= 0, columnspan=3, pady=20)

        #Name Input
        self.nameLabel = Label(self.frame, text="Name: ").grid(row=1, column=0)
        self.name = Entry(self.frame)
        self.name.grid(row=1, column=1)
        self.name.focus()

        #price Input
        self.priceLabel = Label(self.frame, text="Price: ").grid(row=2, column=0)
        self.price = Entry(self.frame)
        self.price.grid(row=2, column=1)

        #Button add Product
        self.btn = Button(self.frame, text='Save Product', command=self.addProduct)
        self.btn.grid(row=3, columnspan=2, sticky= W + E)

        #Output messages

        self.messageResponse = Label(text="", fg="red")
        self.messageResponse.grid(row=3, column=0, columnspan=2, sticky=W + E)

        #table
        self.table = Treeview(height=10, columns=2)
        self.table.grid(row=4, column=0, columnspan=2)
        self.table.heading('#0', text="Name", anchor=CENTER)
        self.table.heading('#1', text="Price", anchor=CENTER)

        #DELETE and Update

        self.btnDelete = Button(self.root, text='DELETE', command=self.deleteProduct)
        self.btnDelete.grid(row=5, column=0, sticky= W + E)

        self.btnEdit = Button(self.root, text='EDIT', command=self.editProduct)
        self.btnEdit.grid(row=5, column=1, sticky= W + E)

        self.getProductsAndShowInTheTable()
    
    # database conn and queries

    def runQuery(self, query, parameters = ()):

        with sqlite3.connect(self.dbName) as conn:
            
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()

        return result

    def getProductsAndShowInTheTable(self):

        records = self.table.get_children()
        for element in records:
            self.table.delete(element)

        query = 'SELECT * FROM product ORDER BY name DESC'
        dbRows = self.runQuery(query)

        for row in dbRows:
            self.table.insert('', 0, text=row[1],  values=row[2])

    def validate(self):
        
        return ((len(self.name.get()) != 0) and ((len(self.price.get()) != 0)))
    
    def addProduct(self):

        if (self.validate()):

            query = "INSERT INTO product VALUES(NULL, ?, ?)"
            parameters = (self.name.get(), self.price.get())
            self.runQuery(query, parameters)
            self.getProductsAndShowInTheTable()
            self.messageResponse['fg'] = 'green'
            self.messageResponse['text'] = f'Product {self.name.get()} added successfully'
            self.name.delete(0, END)
            self.price.delete(0, END)
            #showinfo("Correct", "All correct.")
        
        else:

            self.messageResponse['text'] = 'Name and price are required.'
            #showwarning("Add data", "Name and price are required.")
        
    def deleteProduct(self):

        self.messageResponse['text'] = ''

        try:

            self.table.item(self.table.selection())['text'][0]

        except IndexError as e:

            showwarning("No has seleccionado ningún elemento", "Please select an item.")
            return
        
        name = self.table.item(self.table.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.runQuery(query, (name, ))
        self.messageResponse['text'] = f'Record {name} deleted successfully'

        self.getProductsAndShowInTheTable()
    
    def editProduct(self):

        self.messageResponse['text'] = ''

        try:

            self.table.item(self.table.selection())['text'][0]

        except IndexError as e:

            showwarning("No has seleccionado ningún elemento", "Please select an item.")
            return
        
        oldName = self.table.item(self.table.selection())['text']
        oldPrice = self.table.item(self.table.selection())['values'][0]
        
        self.editWind = Toplevel()
        self.editWind.title = 'Edit product'

        #oldName

        self.voidLabel = Label(self.editWind, text='')
        self.voidLabel.grid(row=0)

        self.oldNameLabel = Label(self.editWind, text=f'Old Name: {oldName}').grid(row=1, column=1)
        self.oldPriceLabel = Label(self.editWind, text=f'Old Price: {oldPrice}').grid(row=2, column=1)

        #newName

        #container
        self.frameEditWind = LabelFrame(self.editWind, text="Register the new data")
        self.frameEditWind.grid(row= 3, columnspan=3, pady=20)

        #Name Input
        self.newNameLabel = Label(self.frameEditWind, text="New name: ").grid(row=1, column=0)
        self.newName = Entry(self.frameEditWind, textvariable= StringVar(self.editWind, value=oldName))
        self.newName.focus()
        self.newName.grid(row=1, column=1)

        #price Input
        self.newPriceLabel = Label(self.frameEditWind, text="New price: ").grid(row=2, column=0)
        self.newPrice = Entry(self.frameEditWind, textvariable= DoubleVar(self.editWind, value=oldPrice))
        self.newPrice.grid(row=2, column=1)

        #Button edit Product
        self.btnEdit = Button(self.frameEditWind, text='Edit product', command= lambda: self.editRecord(oldName, oldPrice))
        self.btnEdit.grid(row=3, columnspan=2, sticky= W)
    
    def editRecord(self, oldName, oldPrice):
        
        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (self.newName.get(), self.newPrice.get(), oldName, oldPrice)
        self.runQuery(query, parameters)
        self.editWind.destroy()
        self.messageResponse['text'] = f'Record {oldName} update successfully'
        self.getProductsAndShowInTheTable()



if __name__ == '__main__':

    window = Tk()
    application = Product(window)
    window.mainloop()