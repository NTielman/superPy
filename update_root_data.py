import os
import csv

def root_inventory(dir_path, inventory):
    '''updates and re-writes root_inventory.csv'''
    inventory_file_path = os.path.join(dir_path, 'root_inventory.csv')
    with open(inventory_file_path, 'w', newline='') as csvfile:
        headers = ['product_id', 'quantity']
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for prod_id in inventory:
            writer.writerow(
                {'product_id': prod_id, 'quantity': inventory[prod_id]})

def root_expiry(dir_path, expiry_dates):
    '''updates and rewrites root_expiry_dates.csv'''
    expiry_file_path = os.path.join(dir_path, 'root_expiry_dates.csv')
    with open(expiry_file_path, 'w', newline='') as csvfile:
        headers = ['expiry_date', 'product', 'quantity']
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for expiry_date in expiry_dates:
            for product in expiry_dates[expiry_date]:
                writer.writerow({'expiry_date': expiry_date, 'product': product,
                                 'quantity': expiry_dates[expiry_date][product]})

def root_purchases(dir_path, purchase_date, purchase_info):
    '''updates/ appends to root_purchases.csv'''
    purchases_file_path = os.path.join(dir_path, 'root_purchases.csv')
    # unpack purchase info
    product = purchase_info['product']
    quantity = purchase_info['quantity']
    unit_cost = purchase_info['unit_cost']
    total_cost = purchase_info['total_cost']
    exp_date = purchase_info['expiry_date']
    transaction_id = purchase_info['id']

    if os.path.isfile(purchases_file_path):
        with open(purchases_file_path, 'a', newline='') as csvfile:
            headers = ['purchase_date', 'product', 'quantity',
                       'unit_cost', 'total_cost', 'expiry_date', 'id']
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writerow({'purchase_date': purchase_date, 'product': product, 'quantity': quantity,
                             'unit_cost': unit_cost, 'total_cost': total_cost, 'expiry_date': exp_date, 'id': transaction_id})
    else:
        with open(purchases_file_path, 'w', newline='') as csvfile:
            headers = ['purchase_date', 'product', 'quantity',
                       'unit_cost', 'total_cost', 'expiry_date', 'id']
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerow({'purchase_date': purchase_date, 'product': product, 'quantity': quantity,
                             'unit_cost': unit_cost, 'total_cost': total_cost, 'expiry_date': exp_date, 'id': transaction_id})

def root_sales(dir_path, sell_date, sale_info):
    '''updates/ appends to root_sales.csv'''
    sales_file_path = os.path.join(dir_path, 'root_sales.csv')
    # unpack sale info
    product = sale_info['product']
    quantity = sale_info['quantity']
    unit_cost = sale_info['unit_cost']
    unit_price = sale_info['unit_price']
    total_revenue = sale_info['total_revenue']
    transaction_id = sale_info['id']

    if os.path.isfile(sales_file_path):
        with open(sales_file_path, 'a', newline='') as csvfile:
            headers = ['sales_date', 'product', 'quantity',
                       'unit_cost', "unit_price", "total_revenue", 'id']
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writerow({'sales_date': sell_date, 'product': product, 'quantity': quantity, 'unit_cost': unit_cost,
                             "unit_price": unit_price, "total_revenue": total_revenue, 'id': transaction_id})
    else:
        with open(sales_file_path, 'w', newline='') as csvfile:
            headers = ['sales_date', 'product', 'quantity',
                       'unit_cost', "unit_price", "total_revenue", 'id']
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerow({'sales_date': sell_date, 'product': product, 'quantity': quantity, 'unit_cost': unit_cost,
                             "unit_price": unit_price, "total_revenue": total_revenue, 'id': transaction_id})