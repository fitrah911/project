#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sqlite3

class Transaction:
    def __init__(self):
        self.items = []
    
    def add_item(self, item):
        self.items.append(item)
    
    def update_item_name(self, item_name, new_name):
        for item in self.items:
            if item[0] == item_name:
                item[0] = new_name
                break
    
    def update_item_qty(self, item_name, new_qty):
        for item in self.items:
            if item[0] == item_name:
                item[1] = new_qty
                break
    
    def update_item_price(self, item_name, new_price):
        for item in self.items:
            if item[0] == item_name:
                item[2] = new_price
                break
    
    def delete_item(self, item_name):
        self.items = [item for item in self.items if item[0] != item_name]
    
    def reset_transaction(self):
        self.items = []
    
    def check_order(self):
        valid = True
        for item in self.items:
            if '' in item:
                valid = False
                break
        if valid:
            print("Pemesanan sudah benar")
        else:
            print("Terdapat kesalahan input data")
    
    def check_out(self):
        total = 0
        for item in self.items:
            total += item[1] * item[2]
        
        if total > 500000:
            discount = 0.07
        elif total > 300000:
            discount = 0.06
        elif total > 200000:
            discount = 0.05
        else:
            discount = 0
        
        total_after_discount = total - (total * discount)
        
        print("Total pembelian: Rp", total_after_discount)
        self.insert_to_table()
    
    def insert_to_table(self):
        conn = sqlite3.connect('transaction.db')
        cursor = conn.cursor()
        
        cursor.execute('CREATE TABLE IF NOT EXISTS transaction (no_id INTEGER PRIMARY KEY AUTOINCREMENT, nama_item TEXT, jumlah_item INTEGER, harga INTEGER, total_harga INTEGER, diskon REAL, harga_diskon REAL)')
        
        for item in self.items:
            nama_item, jumlah_item, harga = item
            total_harga = jumlah_item * harga
            cursor.execute('INSERT INTO transaction (nama_item, jumlah_item, harga, total_harga, diskon, harga_diskon) VALUES (?, ?, ?, ?, ?, ?)', (nama_item, jumlah_item, harga, total_harga, discount, total_harga * (1 - discount)))
        
        conn.commit()
        conn.close()

# Contoh penggunaan
trnsct_123 = Transaction()
trnsct_123.add_item(["mobil", 2, 100000])
trnsct_123.add_item(["tempe", 3, 3])

trnsct_123.update_item_name("tempe", "mie")
trnsct_123.update_item_qty("mie", 1)
trnsct_123.update_item_price("mie", 5000)

trnsct_123.delete_item("mie")

trnsct_123.check_order()
trnsct_123.check_out()

