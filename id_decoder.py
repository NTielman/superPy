import csv
import os

def id_decoder(trans_id):
    '''returns product data based on provided 
    transaction id'''
    product_info = {}
    is_purchase_id = 'PURCH' in trans_id
    is_sales_id = 'SALE' in trans_id
    dir_path = create_directory('root_files')

    if is_purchase_id:
        purchases_path = os.path.join(dir_path, 'root_purchases.csv')
        with open(purchases_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['id'] == trans_id:
                        product_info[trans_date] = row['purchase_date']
                        product_info[product_name] = row['product']
                        product_info[exp_date] = row['expiry_date']
                        product_info[unit_cost] = row['unit_cost']
                        id_start_index = trans_id.index('H') + 1
                        product_info[purchase_index] = int(trans_id[id_start_index:]) - 1
                        return product_info
    elif is_sales_id:
        sales_path = os.path.join(dir_path, 'root_sales.csv')
        with open(sales_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['id'] == trans_id:
                        product_info[trans_date] = row['sales_date']
                        product_info[product_name] = row['product']
                        product_info[sold_quantity] = row['quantity']
                        product_info[unit_cost] = row['unit_cost']
                        product_info[unit_price] = row['unit_price']
                        id_start_index = trans_id.index('E') + 1
                        product_info[purchase_index] = int(trans_id[id_start_index:]) - 1
                        return product_info
    return False

