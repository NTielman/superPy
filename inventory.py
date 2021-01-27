from datetime import date, timedelta, datetime
from create_directory import create_directory
from id_decoder import id_decoder
import csv
import os
from print_report import print_report
from rich.console import Console
from output_styling import superpy_theme

console = Console(theme=superpy_theme)

class Supermarket():
    purchases = {}
    sales = {} 
    expiry_dates = {}
    inventory = {}

    def __init__(self):
        '''checks if an inventory already exists 
        and initialises inventory'''
        dir_path = create_directory('root_files')
        self.dir_path = dir_path

        inventory_path = os.path.join(dir_path, 'root_inventory.csv')
        expiry_path = os.path.join(dir_path, 'root_expiry_dates.csv')
        purchases_path = os.path.join(dir_path, 'root_purchases.csv')
        sales_path = os.path.join(dir_path, 'root_sales.csv')

        if os.path.isfile(inventory_path):
            #initialise self.inventory
            with open(inventory_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    product = row['product']
                    quantity = float(row['quantity'])
                    # add product to inventory
                    self.inventory[product] = quantity
        if os.path.isfile(expiry_path):
            #initialise self.expiry_dates
            with open(expiry_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    expiry_date = row['expiry_date']
                    product = row['product']
                    quantity = float(row['quantity'])
                    # if expiry_date not yet in expiry dates
                    if not (expiry_date in self.expiry_dates):
                        # create a dict
                        self.expiry_dates[expiry_date] = {}
                    self.expiry_dates[expiry_date][product] = quantity
        if os.path.isfile(purchases_path):
            #initialise self.purchases
            with open(purchases_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    purchase_date = row['purchase_date']
                    product = row['product']
                    quantity = float(row['quantity'])
                    unit_cost = float(row['unit_cost'])
                    total_cost = float(row['total_cost'])
                    expiry_date = row['expiry_date']
                    purch_id = row['id']
                    # if purchase date not yet in purchases
                    if not (purchase_date in self.purchases):
                        # create a transaction (purchases) list
                        self.purchases[purchase_date] = []
                    # add purchase info to purchase date
                    purchase_info = {
                        "product": product,
                        "quantity": quantity,
                        "unit_cost": unit_cost,
                        "total_cost": total_cost,
                        "expiry_date": expiry_date,
                        "id": purch_id
                    }
                    self.purchases[purchase_date].append(purchase_info)
        if os.path.isfile(sales_path):
            #initialise self.sales
            with open(sales_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    sales_date = row['sales_date']
                    product = row['product']
                    quantity = float(row['quantity'])
                    unit_cost = float(row['unit_cost'])
                    unit_price = float(row['unit_price'])
                    total_income = float(row['total_income'])
                    sale_id = row['id']
                    # if transaction date not yet in sales
                    if not (sales_date in self.sales):
                        # create a transaction (sales) list
                        self.sales[sales_date] = []
                    # add sale info to transaction date
                    sale_info = {
                        "product": product,
                        "quantity": quantity,
                        "unit_cost": unit_cost,
                        "unit_price": unit_price,
                        "total_income": total_income,
                        "id": sale_id
                    }
                    self.sales[sales_date].append(sale_info)

    def discard(self, purch_id, quantity=1):
        '''removes item(s) from inventory 
        (bijv, if item is: defect, expired) '''
        product_info = id_decoder(purch_id)
        if not product_info:
            console.print('Failure: could not discard item(s)', style='failure')
            return None
        
        product = product_info['product_name']
        exp_date = product_info['exp_date']

        if quantity >= self.inventory[product]:
            del self.inventory[product]
        else:
            self.inventory[product] -= quantity
        #update and write inventory.csv
        inventory_file_path = os.path.join(self.dir_path, 'root_inventory.csv')
        #could change below to a function update_root_inventory()
        with open(inventory_file_path, 'w', newline='') as csvfile:
            headers = ['product', 'quantity']
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            for product_name in self.inventory:
                writer.writerow({'product': product_name, 'quantity': self.inventory[product_name]})

        # remove items from expiry dates
        if quantity >= self.expiry_dates[exp_date][product]:
            del self.expiry_dates[exp_date][product]
        else:
            self.expiry_dates[exp_date][product] -= quantity
        #update and write expiry.csv
        expiry_file_path = os.path.join(self.dir_path, 'root_expiry_dates.csv')
        with open(expiry_file_path, 'w', newline='') as csvfile:
            headers = ['expiry_date', 'product', 'quantity']
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            for expiry_date in self.expiry_dates:
                for product_name in self.expiry_dates[expiry_date]:
                    writer.writerow({'expiry_date': expiry_date, 'product': product_name, 'quantity': self.expiry_dates[expiry_date][product_name]})
        console.print(f'Success: discarded [highlight]{quantity} {product}[/highlight] from inventory', style='success')

    def buy(self, product, quantity, cost_per_unit, exp_date, purchase_date):
        '''adds a product to inventory and
        adds product info to purchase records '''
        #updates csvfiles: inventory change virtual inv kaba write , purchases (append) i expiry change self.expiry kaba write to exp.csv
        if product in self.inventory:
            self.inventory[product] += quantity
        else:
            # add product to inventory
            self.inventory[product] = quantity
        #update and write inventory.csv
        inventory_file_path = os.path.join(self.dir_path, 'root_inventory.csv')
        with open(inventory_file_path, 'w', newline='') as csvfile:
            headers = ['product', 'quantity']
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            for product_name in self.inventory:
                writer.writerow({'product': product_name, 'quantity': self.inventory[product_name]})

        # if exp_date not yet in expiry dates
        if not (exp_date in self.expiry_dates):
            # create a dict
            self.expiry_dates[exp_date] = {}
        # if product not yet in dict
        if not (product in self.expiry_dates[exp_date]):
            # add products and prod quantities to expiry date
            self.expiry_dates[exp_date][product] = quantity
        else:
            self.expiry_dates[exp_date][product] += quantity
        #update and write expiry.csv
        expiry_file_path = os.path.join(self.dir_path, 'root_expiry_dates.csv')
        with open(expiry_file_path, 'w', newline='') as csvfile:
            headers = ['expiry_date', 'product', 'quantity']
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            for expiry_date in self.expiry_dates:
                for product_name in self.expiry_dates[expiry_date]:
                    writer.writerow({'expiry_date': expiry_date, 'product': product_name, 'quantity': self.expiry_dates[expiry_date][product_name]})
            
        # if purchase date is empty, set current date as purch date
        # if not purchase_date:
        #     purchase_date = current.isoformat()
        # if purchase date not yet in purchases
        if not (purchase_date in self.purchases):
            # create a transaction (purchases) list
            self.purchases[purchase_date] = []
        # add purchase info to purchase date
        trans_date = date.fromisoformat(purchase_date)
        transaction_id = f'#SUP{trans_date.strftime("%y%m%d")}PURCH0{len(self.purchases[purchase_date]) + 1}'
        purchase_info = {
            "product": product,
            "quantity": quantity,
            "unit_cost": cost_per_unit,
            "total_cost": round((cost_per_unit*quantity), 2),
            "expiry_date": exp_date,
            "id": transaction_id
        }
        self.purchases[purchase_date].append(purchase_info)
        #update root_purchases.csv
        purchases_file_path = os.path.join(self.dir_path, 'root_purchases.csv')
        if os.path.isfile(purchases_file_path):
            #file exists append new info
            with open(purchases_file_path, 'a', newline='') as csvfile:
                headers = ['purchase_date', 'product', 'quantity', 'unit_cost', 'total_cost', 'expiry_date', 'id']
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writerow({'purchase_date': purchase_date, 'product': product, 'quantity': quantity, 'unit_cost': cost_per_unit, 'total_cost': round((cost_per_unit*quantity), 2), 'expiry_date': exp_date, 'id': transaction_id})
        else:
            #file doesn't exist yet. write headers and create file 
            with open(purchases_file_path, 'w', newline='') as csvfile:
                headers = ['purchase_date', 'product', 'quantity', 'unit_cost', 'total_cost', 'expiry_date', 'id']
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                writer.writerow({'purchase_date': purchase_date, 'product': product, 'quantity': quantity, 'unit_cost': cost_per_unit, 'total_cost': round((cost_per_unit * quantity), 2), 'expiry_date': exp_date, 'id': transaction_id})
        console.print(f'Success: [highlight]{quantity} {product}[/highlight] added to inventory. Transaction ID: [highlight]{transaction_id}[/highlight]', style='success')

    def sell(self, product, quantity, price_per_unit, purchase_id, sell_date):
        '''removes a product from inventory and
        adds product info to sales records '''
        product_info = id_decoder(purchase_id)

        if not (product in self.inventory):
            console.print(f'Failure: "{product}" is not in stock', style='failure')
            return None
        elif not product_info:
            console.print(f'Failure: could not sell {product}', style='failure')
            return None
        # elif quantity > self.inventory[product]:
        #     return "not enough in stock to complete transaction"
        
        # product = product_info['product_name']
        exp_date = product_info['exp_date']
        purchase_date = product_info['trans_date']
        purchase_index = product_info['purchase_index']
        unit_cost = product_info['unit_cost']

        # extract product info from purchase id
        # id_date = datetime.strptime(purchase_id[4:10], "%y%m%d")
        # purchase_index = int(purchase_id[15:17]) - 1
        # purchase_date = id_date.strftime("%Y-%m-%d")
        # exp_date = self.purchases[purchase_date][purchase_index]["expiry_date"]
        # unit_cost = self.purchases[purchase_date][purchase_index]["unit_cost"]
        #if quantity higher than the quantity associated with purchase id 
        if quantity > self.expiry_dates[exp_date][product]:
            console.print(f'Failure: incorrect quantity or incorrect purchase ID provided', style='failure')
            return None

        # reduce product inventory quantities
        self.inventory[product] -= quantity
        products_left = self.inventory[product]
        if products_left == 0:
            del self.inventory[product]
        #update and write inventory.csv
        inventory_file_path = os.path.join(self.dir_path, 'root_inventory.csv')
        #could change below to a function update_root_inventory()
        with open(inventory_file_path, 'w', newline='') as csvfile:
            headers = ['product', 'quantity']
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            for product_name in self.inventory:
                writer.writerow({'product': product_name, 'quantity': self.inventory[product_name]})

        # remove products and prod quantities from expiry date
        if quantity >= self.expiry_dates[exp_date][product]:
            del self.expiry_dates[exp_date][product]
        else:
            self.expiry_dates[exp_date][product] -= quantity
        #update and write expiry.csv
        expiry_file_path = os.path.join(self.dir_path, 'root_expiry_dates.csv')
        with open(expiry_file_path, 'w', newline='') as csvfile:
            headers = ['expiry_date', 'product', 'quantity']
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            for expiry_date in self.expiry_dates:
                for product_name in self.expiry_dates[expiry_date]:
                    writer.writerow({'expiry_date': expiry_date, 'product': product_name, 'quantity': self.expiry_dates[expiry_date][product_name]})

        # if transaction date not yet in sales
        # current_date = current.isoformat()
        if not (sell_date in self.sales):
            # create a transaction (sales) list
            self.sales[sell_date] = []
        # add sale info to transaction date
        trans_date = date.fromisoformat(sell_date)
        transaction_id = f'#SUP{trans_date.strftime("%y%m%d")}SALE0{len(self.sales[sell_date]) + 1}'
        sale_info = {
            "product": product,
            "quantity": quantity,
            "unit_cost": unit_cost,
            "unit_price": price_per_unit,
            "total_income": round((price_per_unit*quantity), 2),
            "id": transaction_id
        }
        self.sales[sell_date].append(sale_info)
        #update root_sales.csv
        sales_file_path = os.path.join(self.dir_path, 'root_sales.csv')
        if os.path.isfile(sales_file_path):
            #file exists append new info
            with open(sales_file_path, 'a', newline='') as csvfile:
                headers = ['sales_date', 'product', 'quantity', 'unit_cost', "unit_price", "total_income", 'id']
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writerow({'sales_date': sell_date, 'product': product, 'quantity': quantity, 'unit_cost': unit_cost, "unit_price": price_per_unit, "total_income": round((price_per_unit*quantity), 2), 'id': transaction_id})
        else:
            #file doesn't exist yet. write headers and create file 
            with open(sales_file_path, 'w', newline='') as csvfile:
                headers = ['sales_date', 'product', 'quantity', 'unit_cost', "unit_price", "total_income", 'id']
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                writer.writerow({'sales_date': sell_date, 'product': product, 'quantity': quantity, 'unit_cost': unit_cost, "unit_price": price_per_unit, "total_income": round((price_per_unit*quantity), 2), 'id': transaction_id})
        console.print(f'Success: sold [highlight]{quantity} {product}[/highlight] from inventory. Transaction ID: [highlight]{transaction_id}[/highlight]', style='success')
        # if products_left <= 5:
        #     self.warn("low_stock")

    def warn(self, message):
        #set timeout function 2/ 3 seconds so iot prints warning after report?
        if message == "low_stock":
            console.print('Warning: some items are low on stock', style='error')
            answer = input(
                "Would you like to print a [highlight]low-stock report[/highlight]? (y/n)\n")
            if answer == 'y':
                print_report(self.get_low_stock_report())
        elif message == "expires_soon":
            console.print('Warning: some items are close to expiring', style='error')
            answer = input("Would you like to print an [highlight]expiry report[/highlight]? (y/n)\n")
            if answer == 'y':
                print_report(self.get_expiry_report())
        elif message == "expired_items":
            console.print('Warning: some items have expired, consider [highlight]discarding[/highlight] the items from inventory', style='error')

    def get_inventory_report(self):
        '''returns a list of products and product quantities
        that the supermarket currently holds'''
        csv_report = [['Product Name', 'Amount In Stock']]
        terminal_report = [f'{"Product Name":<20}| Amount In Stock']
        for product in self.inventory:
            quantity = self.inventory[product]
            terminal_report.append(
                f'{product:<20}| {quantity}')
            csv_report.append([product, quantity])
        if len(csv_report) <= 1:
            console.print(f'Failure: no items found in inventory', style='failure')
            return False
        return [terminal_report, 'inventory', csv_report]

    def get_products_report(self):
        '''returns a list of all products the supermarket offers'''
        terminal_report = []
        csv_report = [['Product Name']]
        for product in self.inventory:
            terminal_report.append(f'{product}')
            csv_report.append([product])
        if len(csv_report) <= 1:
            console.print(f'Failure: no items found in inventory', style='failure')
            return False
        return [terminal_report, 'products', csv_report]

    def get_purchase_report(self, purchase_date='all'):
        '''returns all purchase transactions 
        or all purchases made on a specific date '''
        terminal_report = [
            f'{"Date":<11}| {"Product":<10}| {"Amnt":<8}| {"Unit Cost":<10}| {"Total":<8}| {"Exp Date":<11}| Transaction ID']
        csv_report = [['Date', 'Product', 'Amnt', 'Unit Cost',
                       'Total', 'Exp Date', 'Transaction ID']]
        total_cost = 0
        if purchase_date == 'all': #change purrchase date to '-' character ku tei aanwezig in all dates
            for date in self.purchases:
                for purchase_num in range(len(self.purchases[date])):
                    product = self.purchases[date][purchase_num]["product"]
                    quantity = self.purchases[date][purchase_num]["quantity"]
                    unit_cost = self.purchases[date][purchase_num]["unit_cost"]
                    total_spent = self.purchases[date][purchase_num]["total_cost"]
                    expiry_date = self.purchases[date][purchase_num]["expiry_date"]
                    trans_id = self.purchases[date][purchase_num]["id"]
                    total_cost += total_spent
                    terminal_report.append(
                        f'{date:<11}| {product:<10}| {quantity:<8}| {unit_cost:<10}| {total_spent:<8}| {expiry_date:<11}| {trans_id}')
                    csv_report.append(
                        [date, product, quantity, unit_cost, total_spent, expiry_date, trans_id])
        else: #if date = '-' use below for loop so
            for date in self.purchases:
                # if date contains specific year bijv:'2021' or '2021-01'
                if purchase_date in date:
                    for purchase_num in range(len(self.purchases[date])):
                        product = self.purchases[date][purchase_num]["product"]
                        quantity = self.purchases[date][purchase_num]["quantity"]
                        unit_cost = self.purchases[date][purchase_num]["unit_cost"]
                        total_spent = self.purchases[date][purchase_num]["total_cost"]
                        expiry_date = self.purchases[date][purchase_num]["expiry_date"]
                        trans_id = self.purchases[date][purchase_num]["id"]
                        total_cost += total_spent
                        terminal_report.append(
                            f'{date:<11}| {product:<10}| {quantity:<8}| {unit_cost:<10}| {total_spent:<8}| {expiry_date:<11}| {trans_id}')
                        csv_report.append(
                            [date, product, quantity, unit_cost, total_spent, expiry_date, trans_id])
        # elif is_day_report and purchase_date in self.purchases:
        #     for purchase_num in range(len(self.purchases[purchase_date])):
        #         product = self.purchases[purchase_date][purchase_num]["product"]
        #         quantity = self.purchases[purchase_date][purchase_num]["quantity"]
        #         unit_cost = self.purchases[purchase_date][purchase_num]["unit_cost"]
        #         total_spent = self.purchases[purchase_date][purchase_num]["total_cost"]
        #         expiry_date = self.purchases[purchase_date][purchase_num]["expiry_date"]
        #         trans_id = self.purchases[purchase_date][purchase_num]["id"]
        #         total_cost += total_spent
        #         terminal_report.append(
        #             f'{purchase_date:<11}| {product:<10}| {quantity:<8}| {unit_cost:<10}| {total_spent:<10}| {expiry_date:<10}| {trans_id}')
        #         csv_report.append(
        #             [purchase_date, product, quantity, unit_cost, total_spent, expiry_date, trans_id])
        if len(csv_report) <= 1:
            console.print(f'Failure: No purchase records found for date: [highlight]{purchase_date}[/highlight]', style='failure')
            return False
            # terminal_report.append(
            #     f'No purchase records found for date: {purchase_date}')
            # csv_report.append(
            #     [f'No purchase records found for date: {purchase_date}'])
        terminal_report.append(f'Total Cost: ${round(total_cost, 2)}')
        csv_report.append([f'Total Cost: ${round(total_cost, 2)}'])
        return [terminal_report, 'purchases', csv_report, purchase_date]

    def get_sales_report(self, sell_date='all'):
        '''returns all sales transactions 
        or all sales made on a specific date'''
        terminal_report = [
            f'{"Date":<11}| {"Product":<15}| {"Amnt":<10}| {"Unit Price":<13}| {"Total":<10}| Transaction ID']
        csv_report = [['Date', 'Product', 'Amnt',
                       'Unit Price', 'Total', 'Transaction ID']]
        total_revenue = 0
        if sell_date == 'all':
            for date in self.sales:
                for sale_num in range(len(self.sales[date])):
                    product = self.sales[date][sale_num]["product"]
                    quantity = self.sales[date][sale_num]["quantity"]
                    unit_price = self.sales[date][sale_num]["unit_price"]
                    total_income = self.sales[date][sale_num]["total_income"]
                    trans_id = self.sales[date][sale_num]["id"]
                    total_revenue += total_income
                    terminal_report.append(
                        f'{date:<11}| {product:<15}| {quantity:<10}| {unit_price:<13}| {total_income:<10}| {trans_id}')
                    csv_report.append(
                        [date, product, quantity, unit_price, total_income, trans_id])
        else: #if date = '-' use below for loop so
            for date in self.sales:
                # if date contains specific year bijv:'2021' or '2021-01'
                if sell_date in date:
                    for sale_num in range(len(self.sales[date])):
                        product = self.sales[date][sale_num]["product"]
                        quantity = self.sales[date][sale_num]["quantity"]
                        unit_price = self.sales[date][sale_num]["unit_price"]
                        total_income = self.sales[date][sale_num]["total_income"]
                        trans_id = self.sales[date][sale_num]["id"]
                        total_revenue += total_income
                        terminal_report.append(
                            f'{date:<11}| {product:<15}| {quantity:<10}| {unit_price:<13}| {total_income:<10}| {trans_id}')
                        csv_report.append(
                            [date, product, quantity, unit_price, total_income, trans_id])
        # elif sell_date in self.sales:
        #     for sale_num in range(len(self.sales[sell_date])):
        #         product = self.sales[sell_date][sale_num]["product"]
        #         quantity = self.sales[sell_date][sale_num]["quantity"]
        #         unit_price = self.sales[sell_date][sale_num]["unit_price"]
        #         total_income = self.sales[sell_date][sale_num]["total_income"]
        #         trans_id = self.sales[sell_date][sale_num]["id"]
        #         total_revenue += total_income
        #         terminal_report.append(
        #             f'{sell_date:<11}| {product:<15}| {quantity:<10}| {unit_price:<13}| {total_income:<10}| {trans_id}')
        #         csv_report.append(
        #             [sell_date, product, quantity, unit_price, total_income, trans_id])
        if len(csv_report) <= 1:
            console.print(f'Failure: no sale records found for date: [highlight]{sell_date}[/highlight]', style='failure')
            return False
        # else:
        #     terminal_report.append(
        #         f'No sale records found for date: {sell_date}')
        #     csv_report.append([f'No sale records found for date: {sell_date}'])
        terminal_report.append(f'Total Revenue: ${round(total_revenue, 2)}')
        csv_report.append([f'Total Revenue: ${round(total_revenue, 2)}'])
        return [terminal_report, 'sales', csv_report, sell_date]

    def get_profit_report(self, profit_date='all'):
        '''returns total profit made over time 
        or profit made on a specific date '''
        is_day_report = len(profit_date) == 10
        terminal_report = []
        csv_report = []
        total_profit = 0
        if is_day_report and profit_date in self.sales:
            terminal_report.append(
                f'{"Date":<11}| {"Amnt x Product":<20}| {"Total Cost":<15}| {"Total Revenue":<15}| Total Profit')
            csv_report.append(
                ['Date', 'Amnt x Product', 'Total Cost', 'Total Revenue', 'Total Profit'])
            for sale_num in range(len(self.sales[profit_date])):
                sale_id = self.sales[profit_date][sale_num]["id"]
                product_info = id_decoder(sale_id)
                product = product_info['product_name'] 
                quantity = product_info['sold_quantity'] 
                unit_cost = product_info['unit_cost']
                product_cost = product_info['total_cost'] 
                product_revenue = product_info['total_revenue'] 
                product_profit = product_info['total_profit'] 
                # product = self.sales[profit_date][sale_num]["product"]
                # quantity = self.sales[profit_date][sale_num]["quantity"]
                # unit_cost = self.sales[profit_date][sale_num]["unit_cost"]
                # product_cost = unit_cost * quantity
                # product_revenue = self.sales[profit_date][sale_num]["total_income"]
                # product_profit = product_revenue - product_cost
                total_profit += product_profit
                terminal_report.append(
                    f'{profit_date:<11}| {str(quantity) + " x " + product:<20}| {product_cost:<15}| {product_revenue:<15}| {product_profit}')
                csv_report.append(
                    [profit_date, f'{quantity} x {product}', product_cost, product_revenue, product_profit])
        else:
            terminal_report.append(
                f'{"Date":<11}| {"Total Cost":<15}| {"Total Revenue":<15}| Total Profit')
            csv_report.append(
                ['Date', 'Total Cost', 'Total Revenue', 'Total Profit'])
            for date in self.sales:
                day_profit = 0
                day_revenue = 0
                day_cost = 0
                if profit_date in date:
                    for sale_num in range(len(self.sales[date])):
                        sale_id = self.sales[date][sale_num]["id"]
                        product_info = id_decoder(sale_id)
                        quantity = product_info['sold_quantity'] 
                        unit_cost = product_info['unit_cost']
                        product_cost = product_info['total_cost'] 
                        product_revenue = product_info['total_revenue'] 
                        product_profit = product_info['total_profit'] 
                        # quantity = self.sales[date][sale_num]["quantity"]
                        # unit_cost = self.sales[date][sale_num]["unit_cost"]
                        # product_cost = unit_cost * quantity
                        # product_revenue = self.sales[date][sale_num]["total_income"]
                        # product_profit = product_revenue - product_cost
                        day_cost += product_cost
                        day_revenue += product_revenue
                        day_profit += product_profit
                    total_profit += day_profit
                    terminal_report.append(
                        f'{date:<11}| {day_cost:<15}| {day_revenue:<15}| {day_profit}')
                    csv_report.append([date, day_cost, day_revenue, day_profit])
        # elif profit_date in self.sales:
        #     terminal_report.append(
        #         f'{"Date":<11}| {"Amnt x Product":<20}| {"Total Cost":<15}| {"Total Revenue":<15}| Total Profit')
        #     csv_report.append(
        #         ['Date', 'Amnt x Product', 'Total Cost', 'Total Revenue', 'Total Profit'])
        #     for sale_num in range(len(self.sales[profit_date])):
        #         product = self.sales[profit_date][sale_num]["product"]
        #         quantity = self.sales[profit_date][sale_num]["quantity"]
        #         unit_cost = self.sales[profit_date][sale_num]["unit_cost"]
        #         product_cost = unit_cost * quantity
        #         product_revenue = self.sales[profit_date][sale_num]["total_income"]
        #         product_profit = product_revenue - product_cost
        #         total_profit += product_profit
        #         terminal_report.append(
        #             f'{profit_date:<11}| {str(quantity) + " x " + product:<20}| {product_cost:<15}| {product_revenue:<15}| {product_profit}')
        #         csv_report.append(
        #             [profit_date, f'{quantity} x {product}', product_cost, product_revenue, product_profit])
        if len(csv_report) <= 1:
            console.print(f'Failure: no sale records found for date: [highlight]{profit_date}[/highlight]', style='failure')
            return False
        # else:
        #     terminal_report.append(
        #         f'No sale records found for date: {profit_date}')
        #     csv_report.append(
        #         [f'No sale records found for date: {profit_date}'])
        terminal_report.append(f'Total Profit: ${round(total_profit, 2)}')
        csv_report.append([f'Total Profit: ${round(total_profit, 2)}'])
        return [terminal_report, 'profit', csv_report, profit_date]

    def get_low_stock_report(self, max_stock_amount=2):
        '''returns a list of products that are out of stock 
        or running low on stock'''
        terminal_report = [f'{"Product":<20}| Quantity']
        csv_report = [["Product", "Quantity"]]
        for product in self.inventory:
            prod_quantity = self.inventory[product]
            # if products remaining is less than max stock amount
            if prod_quantity == 0:
                terminal_report.append(
                    f'{product:<20}| OUT OF STOCK')
                csv_report.append([product, 'OUT OF STOCK'])
            elif prod_quantity <= max_stock_amount:
                terminal_report.append(
                    f'{product:<20}| {prod_quantity}')
                csv_report.append([product, prod_quantity])
        if len(csv_report) <= 1:
            console.print(f'No items found with quantities lower than [highlight]{max_stock_amount}[/highlight]', style='success')
            return False
        return [terminal_report, 'low stock', csv_report]

    def get_expiry_report(self, current_day, num_of_days=7):
        '''returns a list of expired items or 
        items that expire a specific set of days from now'''
        terminal_report = [
            f'{"Product":<15}| {"Quantity":<10}| Days till expiry']
        csv_report = [["Product", "Quantity", "Days till expiry"]]
        expired_items = 0
        for exp_date in self.expiry_dates:
            # convert expiry date into date object
            expiry_date = date.fromisoformat(exp_date)
            current_date = date.fromisoformat(current_day)
            max_date = current_date + timedelta(days=num_of_days)
            # if product already expired
            if expiry_date < current_date:
                for product in self.expiry_dates[exp_date]:
                    quantity = self.expiry_dates[exp_date][product]
                    terminal_report.append(
                        f'{product:<15}| {quantity:<10}| EXPIRED on {exp_date}')
                    csv_report.append(
                        [product, quantity, f'EXPIRED on {exp_date}'])
                    expired_items += 1
            # if expiry date within specific amount of days
            elif expiry_date <= max_date:
                for product in self.expiry_dates[exp_date]:
                    quantity = self.expiry_dates[exp_date][product]
                    time_till_expiry = abs(expiry_date - current_date)
                    terminal_report.append(
                        f'{product:<15}| {quantity:<10}| {time_till_expiry.days} days')
                    csv_report.append(
                        [product, quantity, f'{time_till_expiry.days} days'])
        # if expired_items > 0:
        #     self.warn("expired_items")
        if len(csv_report) <= 1:
            console.print(f'There are no items that expire within [highlight]{num_of_days}[/highlight] days', style='success')
            return False
        return [terminal_report, 'expiry', csv_report]

    def get_bestselling_days(self, date='all'):
        '''returns days with most sales transactions (most products sold) of all times
        or days with most sales transactions of a specific month and year '''
        terminal_report = ['Best selling day(s)']
        csv_report = [['Best selling day(s)']]
        num_of_sales = 0
        highest_day_profit = 0
        if date == 'all':
            # return bestselling days of all time
            # find the highest num of daily sales
            #find highest profit day
            for sales_date in self.sales:
                day_profit = 0
                day_sales = len(self.sales[sales_date])
                if day_sales > num_of_sales:
                    num_of_sales = day_sales
                for sale_num in range(len(self.sales[sales_date])):
                    sale_id = self.sales[sales_date][sale_num]["id"]
                    product_info = id_decoder(sale_id)
                    # quantity = self.sales[sales_date][sale_num]["quantity"]
                    # unit_cost = self.sales[sales_date][sale_num]["unit_cost"]
                    # product_cost = unit_cost * quantity
                    # product_revenue = self.sales[sales_date][sale_num]["total_income"]
                    # product_profit = product_revenue - product_cost
                    product_profit = product_info['total_profit']
                    day_profit += product_profit
                if day_profit > highest_day_profit: #if > reset highest profit + highest prof day list = [date]
                    highest_day_profit = day_profit #if == highest prof day list.append date
            # find dates with this number of sales
            for sales_date in self.sales:
                if len(self.sales[sales_date]) == num_of_sales:
                    terminal_report.append(sales_date)
                    csv_report.append([sales_date])
            terminal_report.append('Highest Profit day(s)')
            csv_report.append(['Highest Profit day(s)'])
            for sales_date in self.sales:
                day_profit = 0
                for sale_num in range(len(self.sales[sales_date])):
                    sale_id = self.sales[sales_date][sale_num]["id"]
                    product_info = id_decoder(sale_id)
                    # quantity = self.sales[sales_date][sale_num]["quantity"]
                    # unit_cost = self.sales[sales_date][sale_num]["unit_cost"]
                    # product_cost = unit_cost * quantity
                    # product_revenue = self.sales[sales_date][sale_num]["total_income"]
                    # product_profit = product_revenue - product_cost
                    product_profit = product_info['total_profit']
                    day_profit += product_profit
                if day_profit == highest_day_profit:
                    terminal_report.append(sales_date)
                    csv_report.append([sales_date])
        else:
            # return bestselling days of specific year and month
            for sales_date in self.sales:
                if date in sales_date:
                    day_profit = 0
                    day_sales = len(self.sales[sales_date])
                    if day_sales > num_of_sales:
                        num_of_sales = day_sales
                    for sale_num in range(len(self.sales[sales_date])):
                        sale_id = self.sales[sales_date][sale_num]["id"]
                        product_info = id_decoder(sale_id)
                        # quantity = self.sales[sales_date][sale_num]["quantity"]
                        # unit_cost = self.sales[sales_date][sale_num]["unit_cost"]
                        # product_cost = unit_cost * quantity
                        # product_revenue = self.sales[sales_date][sale_num]["total_income"]
                        # product_profit = product_revenue - product_cost
                        product_profit = product_info['total_profit']
                        day_profit += product_profit
                    if day_profit > highest_day_profit: #if > reset highest profit + highest prof day list = [date]
                        highest_day_profit = day_profit #if == highest prof day list.append date
            for sales_date in self.sales:
                if date in sales_date:
                    if len(self.sales[sales_date]) == num_of_sales:
                        terminal_report.append(sales_date)
                        csv_report.append([sales_date])
            terminal_report.append('Highest Profit day(s)')
            csv_report.append(['Highest Profit day(s)'])
            for sales_date in self.sales:
                if date in sales_date:
                    day_profit = 0
                    for sale_num in range(len(self.sales[sales_date])):
                        sale_id = self.sales[sales_date][sale_num]["id"]
                        product_info = id_decoder(sale_id)
                        # quantity = self.sales[sales_date][sale_num]["quantity"]
                        # unit_cost = self.sales[sales_date][sale_num]["unit_cost"]
                        # product_cost = unit_cost * quantity
                        # product_revenue = self.sales[sales_date][sale_num]["total_income"]
                        # product_profit = product_revenue - product_cost
                        product_profit = product_info['total_profit']
                        day_profit += product_profit
                    if day_profit == highest_day_profit:
                        terminal_report.append(sales_date)
                        csv_report.append([sales_date])
        # elif year or month:
        #     # return bestselling days for specific year or month
        #     for sales_date in self.sales:
        #         sales_year = sales_date[:4]
        #         sales_month = sales_date[5:7]
        #         if sales_year == year or sales_month == month:
        #             day_sales = len(self.sales[sales_date])
        #             if day_sales > num_of_sales:
        #                 num_of_sales = day_sales
        #     for sales_date in self.sales:
        #         sales_year = sales_date[:4]
        #         sales_month = sales_date[5:7]
        #         if sales_year == year or sales_month == month:
        #             if len(self.sales[sales_date]) == num_of_sales:
        #                 terminal_report.append(sales_date)
        #                 csv_report.append([sales_date])
        if len(csv_report) <= 2:
            console.print(f'Failure: no sale records found for date: [highlight]{date}[/highlight]', style='failure')
            return False
        terminal_report.append(
            f'Total transactions made per day: {num_of_sales}')
        csv_report.append([f'Total transactions made per day: {num_of_sales}'])
        # if month:
        #     month_num = int(month)
        #     month = date(1900, month_num, 1).strftime('%B')
        #change returned val di year month. {false}{false}
        return [terminal_report, 'best-selling-days', csv_report, date]

    def get_bestselling_products(self, date='all'):
        '''returns the best selling products of all times
        or best selling products of a specific date'''
        terminal_report = []
        csv_report = []
        num_of_sales = 0
        products_sold = {}
        if date == 'all':
            # return bestselling products of all time
            for sales_date in self.sales:
                # find all products sold and quantities sold
                for sale_index in range(len(self.sales[sales_date])):
                    product = self.sales[sales_date][sale_index]["product"]
                    quantity = self.sales[sales_date][sale_index]["quantity"]
                    if not (product in products_sold):
                        products_sold[product] = quantity
                    else:
                        products_sold[product] += quantity
        else:
            # return bestselling products of specific year and month
            for sales_date in self.sales:
                if date in sales_date:
                    # find all products sold and quantities sold
                    for sale_index in range(len(self.sales[sales_date])):
                        product = self.sales[sales_date][sale_index]["product"]
                        quantity = self.sales[sales_date][sale_index]["quantity"]
                        if not (product in products_sold):
                            products_sold[product] = quantity
                        else:
                            products_sold[product] += quantity
        # elif year or month:
        #     # return bestselling products for specific year or month
        #     for sales_date in self.sales:
        #         sales_year = sales_date[:4]
        #         sales_month = sales_date[5:7]
        #         if sales_year == year or sales_month == month:
        #             # find all products sold and quantities sold
        #             for sale_index in range(len(self.sales[sales_date])):
        #                 product = self.sales[sales_date][sale_index]["product"]
        #                 quantity = self.sales[sales_date][sale_index]["quantity"]
        #                 if not (product in products_sold):
        #                     products_sold[product] = quantity
        #                 else:
        #                     products_sold[product] += quantity
        # find highest product quantity | por do this gelijk save highest num i i highest products bijv. if quantity == num of sales append to products list. else if quantity higher reinitialise product list to list = [product]
        for product in products_sold:
            product_quantity = products_sold[product]
            if product_quantity > num_of_sales:
                num_of_sales = product_quantity
        # find products with this number of sales 
        for product in products_sold:
            product_quantity = products_sold[product]
            if product_quantity == num_of_sales:
                terminal_report.append(product)
                csv_report.append([product])
        if len(csv_report) <= 1:
            console.print(f'Failure: no sale records found for date: [highlight]{date}[/highlight]', style='failure')
            return False
        terminal_report.append(
            f'Total amount of product(s) sold: {num_of_sales}')
        csv_report.append([f'Total amount of product(s) sold: {num_of_sales}'])
        # if month:
        #     month_num = int(month)
        #     month = date(1900, month_num, 1).strftime('%B')
            #change returned val di year month. {false}{false}
        return [terminal_report, 'best-selling products', csv_report, date]

superpy = Supermarket()
# superpy.buy(product='mango\'s', quantity=16,
#             exp_date="2020-01-01", cost_per_unit=3)
# print_report(superpy.get_low_stock_report(4))
# superpy.buy('bananas', 2, 0.2, "2021-05-01")
# superpy.buy('kiwi\'s', 6, 1, "2022-06-01")
# superpy.buy('bananas', 7, 0.2, "2021-05-03")
# superpy.sell(product='mango\'s', quantity=10,
#              purchase_id="#SUP210121PURCH01", price_per_unit=10)
# superpy.sell(product='bananas', quantity=5,
#              purchase_id="#SUP210121PURCH04", price_per_unit=2)
# superpy.sell(product='bananas', quantity=2,
#              purchase_id="#SUP210121PURCH04", price_per_unit=3)
# superpy.sell(product='kiwi\'s', quantity=3,
#              purchase_id="#SUP210121PURCH03", price_per_unit=5)
# print_report(superpy.get_purchase_report('2021-01-19'))
# print_report(superpy.get_sales_report())
# superpy.discard(product='bananas', exp_date="2021-05-01", quantity=2)
# print_report(superpy.get_inventory_report())
# print_report(superpy.get_profit_report(profit_date="2021-01-19"))
# print_report(superpy.get_expiry_report())
# print_report(superpy.get_products_report())
# print_report(superpy.get_bestselling_days(year="2021"))
# print_report(superpy.get_bestselling_products())