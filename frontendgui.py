import tkinter as tk 
from tkinter import ttk, messagebox
import requests

API_URL = "http://127.0.0.1:5000/products"

def fetch_products():
    response = requests.get(API_URL)
    return response.json()

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    for item in fetch_products():
        tree.insert("","end",iid=item["id"],values=(item["name"], item["quantity"], item["price"], item["category"]))

def add_product():
    data = {
        "name":name_entry.get(),
        "quantity":int(quantity_entry.get()),
        "price": float(price_entry.get()),
        "category": category_entry.get()
    }
    requests.post(API_URL, json=data)
    refresh_table()

def delete_product():
    selected = tree.selection()
    if selected:
        pid = selected[0]
        requests.delete(f"{API_URL}/{pid}")
        refresh_table()
    else:
        messagebox.showwarning("Warning", "No product selected")

root = tk.Tk()
root.title("Inventory Manager")

tk.Label(root, text="Name").grid(row=0, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)

tk.Label(root, text="Quantity").grid(row=1, column=0)
quantity_entry = tk.Entry(root)
quantity_entry.grid(row=1, column=1)

tk.Label(root, text="Price").grid(row=2, column=0)
price_entry = tk.Entry(root)
price_entry.grid(row=2, column=1)

tk.Label(root, text="Category").grid(row=3, column=0)
category_entry = tk.Entry(root)
category_entry.grid(row=3, column=1)

tk.Button(root, text="Add Product", command=add_product).grid(row=4, column=0, columnspan=2)

tree=ttk.Treeview(root, columns=("Name","Quantity","Price","Category"), show="headings")
for col in ("Name","Quantity","Price","Category"):
    tree.heading(col, text=col)
tree.grid(row=5, column=0, columnspan=2)

tk.Button(root, text="Delete Product", command=delete_product).grid(row=6,column=0, columnspan=2)
refresh_table()

root.mainloop()