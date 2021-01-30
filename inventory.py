import os
import csv
import update_root_data
from rich.console import Console
from datetime import date, timedelta, datetime
from create_directory import create_directory
from print_report import print_report
from id_decoder import id_decoder
from current_date import current

console = Console()
current_day = current.current_date.isoformat()

class Super_inventory():
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

        # initialise inventory
        if os.path.isfile(inventory_path):
            with open(inventory_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    product = row['product']
                    quantity = float(row['quantity'])
                    self.inventory[product] = quantity

        # initialise expiry dates
        if os.path.isfile(expiry_path):
            with open(expiry_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    expiry_date = row['expiry_date']
                    product = row['product']
                    quantity = float(row['quantity'])
                    if not (expiry_date in self.expiry_dates):
                        self.expiry_dates[expiry_date] = {}
                    self.expiry_dates[expiry_date][product] = quantity

        # initialise purchase records
        if os.path.isfile(purchases_path):
            with open(purchases_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    purchase_date = row['purchase_date']
                    purchase_info = {
                        "product": row['product'],
                        "quantity": float(row['quantity']),
                        "unit_cost": float(row['unit_cost']),
                        "total_cost": float(row['total_cost']),
                        "expiry_date": row['expiry_date'],
                        "id": row['id']
                    }
                    if not (purchase_date in self.purchases):
                        self.purchases[purchase_date] = []
                    self.purchases[purchase_date].append(purchase_info)

        # initialise sales records
        if os.path.isfile(sales_path):
            with open(sales_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    sales_date = row['sales_date']
                    sale_info = {
                        "product": row['product'],
                        "quantity": float(row['quantity']),
                        "unit_cost": float(row['unit_cost']),
                        "unit_price": float(row['unit_price']),
                        "total_revenue": float(row['total_revenue']),
                        "id": row['id']
                    }
                    if not (sales_date in self.sales):
                        self.sales[sales_date] = []
                    self.sales[sales_date].append(sale_info)

        if self.inventory:
            self.check_inventory_health()

    def discard(self, purchase_id, quantity):
        '''removes item(s) from inventory 
        without affecting sale/profit records'''
        product_info = id_decoder(purchase_id)
        # check for errors
        if not product_info:
            console.print(f'Failure: no match found for ID: {purchase_id}')
            return None
        product = product_info['product_name']
        exp_date = product_info['exp_date']
        if (not (exp_date in self.expiry_dates)) or (not (product in self.expiry_dates[exp_date])):
            console.print(
                f'Failure: product not found or incorrect ID: {purchase_id}')
            return None

        # update inventory
        self.inventory[product] -= quantity
        if self.inventory[product] <= 0:
            del self.inventory[product]
        update_root_data.root_inventory(self.dir_path, self.inventory)

        # update expiry dsates
        self.expiry_dates[exp_date][product] -= quantity
        if self.expiry_dates[exp_date][product] <= 0:
            del self.expiry_dates[exp_date][product]
        update_root_data.root_expiry(self.dir_path, self.expiry_dates)

        console.print(
            f'Success: discarded {quantity} {product} from inventory')

    def buy(self, product, quantity, cost_per_unit, exp_date, purchase_date):
        '''adds a product to inventory and
        adds product info to purchase records'''
        # update inventory
        if product in self.inventory:
            self.inventory[product] += quantity
        else:
            self.inventory[product] = quantity
        update_root_data.root_inventory(self.dir_path, self.inventory)

        # update expiry dates
        if not (exp_date in self.expiry_dates):
            self.expiry_dates[exp_date] = {}
        if not (product in self.expiry_dates[exp_date]):
            self.expiry_dates[exp_date][product] = quantity
        else:
            self.expiry_dates[exp_date][product] += quantity
        update_root_data.root_expiry(self.dir_path, self.expiry_dates)

        # update purchase records
        if not (purchase_date in self.purchases):
            self.purchases[purchase_date] = []
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
        update_root_data.root_purchases(
            self.dir_path, purchase_date, purchase_info)

        console.print(
            f'Success: {quantity} {product} added to inventory. Transaction ID: {transaction_id}')

    def sell(self, product, quantity, price_per_unit, purchase_id, sell_date):
        '''removes a product from inventory and
        adds product info to sales records'''
        product_info = id_decoder(purchase_id)
        # check for errors
        if not product_info:
            console.print(f'Failure: no match found for ID: {purchase_id}')
            return None
        if product_info['product_name'] != product:
            console.print('Failure: product does not match purchase ID')
            return None
        if not (product in self.inventory):
            console.print(f'Failure: "{product}" is no longer in stock')
            return None
        exp_date = product_info['exp_date']
        unit_cost = product_info['unit_cost']
        if (not (exp_date in self.expiry_dates)) or (not (product in self.expiry_dates[exp_date])):
            console.print(f'Failure: "{product}" is no longer in stock')
            return None
        if quantity > self.expiry_dates[exp_date][product]:
            console.print(
                f'Failure: quantity is too high or incorrect purchase ID provided')
            return None

        # update inventory
        self.inventory[product] -= quantity
        products_left = self.inventory[product]
        if products_left <= 0:
            del self.inventory[product]
        update_root_data.root_inventory(self.dir_path, self.inventory)

        # update expiry dates
        self.expiry_dates[exp_date][product] -= quantity
        if self.expiry_dates[exp_date][product] <= 0:
            del self.expiry_dates[exp_date][product]
        update_root_data.root_expiry(self.dir_path, self.expiry_dates)

        # update sales records
        if not (sell_date in self.sales):
            self.sales[sell_date] = []
        trans_date = date.fromisoformat(sell_date)
        transaction_id = f'#SUP{trans_date.strftime("%y%m%d")}SALE0{len(self.sales[sell_date]) + 1}'
        sale_info = {
            "product": product,
            "quantity": quantity,
            "unit_cost": unit_cost,
            "unit_price": price_per_unit,
            "total_revenue": round((price_per_unit*quantity), 2),
            "id": transaction_id
        }
        self.sales[sell_date].append(sale_info)
        update_root_data.root_sales(self.dir_path, sell_date, sale_info)

        console.print(
            f'Success: sold {quantity} {product} from inventory. Transaction ID: {transaction_id}')

    def check_inventory_health(self):
        console.print('Running "Inventory Health" scan...')
        has_low_stock = self.get_low_stock_report()
        has_expired_stock = self.get_expiry_report()
        if has_low_stock:
            console.print('Warning: some items are low on stock')
        if has_expired_stock:
            console.print(
                'Warning: some items have expired or are close to expiring')

    def get_inventory_report(self):
        '''returns a list of products and product quantities
        currently in stock'''
        report = []
        headers = ['Product Name', 'Quantity In Stock']
        report.append(headers)

        for product in self.inventory:
            quantity = self.inventory[product]
            report.append([product, quantity])

        if len(report) <= 1:  # if report only contains headers
            console.print('No items found in inventory')
            return False
        return ['inventory', report]

    def get_products_report(self):
        '''returns a list of all available products'''
        report = []
        headers = ['Product Name']
        report.append(headers)

        for product in self.inventory:
            report.append([product])

        if len(report) <= 1:
            console.print('No items found in inventory')
            return False
        return ['products', report]

    def get_purchase_report(self, purchase_date):
        '''returns all purchase transactions or 
        all purchases for a specific year/ month/ date'''
        report = []
        headers = ['Date', 'Product', 'Qty', 'Unit Cost',
                   'Total', 'Exp Date', 'Transaction ID']
        report.append(headers)
        total_cost = 0

        for trans_date in self.purchases:
            if purchase_date in trans_date:  # if trans_date contains specific string, bijv:'2021' or '2021-01-14'
                for purchase_index in range(len(self.purchases[trans_date])):
                    product = self.purchases[trans_date][purchase_index]["product"]
                    quantity = self.purchases[trans_date][purchase_index]["quantity"]
                    unit_cost = self.purchases[trans_date][purchase_index]["unit_cost"]
                    total_spent = self.purchases[trans_date][purchase_index]["total_cost"]
                    expiry_date = self.purchases[trans_date][purchase_index]["expiry_date"]
                    trans_id = self.purchases[trans_date][purchase_index]["id"]
                    total_cost += total_spent
                    report.append([trans_date, product, quantity,
                                   unit_cost, total_spent, expiry_date, trans_id])

        if len(report) <= 1:
            console.print(
                f'No purchase records found for date: {purchase_date}')
            return False
        # add report footer info
        report.append([f'Total Cost: ${round(total_cost, 2)}'])
        return ['purchases', report, purchase_date]

    def get_sales_report(self, sell_date):
        '''returns all sales transactions or
        all sales for a specific year/ month/ date'''
        report = []
        headers = ['Date', 'Product', 'Qty',
                   'Unit Price', 'Total', 'Transaction ID']
        report.append(headers)
        total_revenue = 0

        for trans_date in self.sales:
            if sell_date in trans_date:  # check if date contains specific string, bijv:'2021-02' or '-'
                for sale_index in range(len(self.sales[trans_date])):
                    product = self.sales[trans_date][sale_index]["product"]
                    quantity = self.sales[trans_date][sale_index]["quantity"]
                    unit_price = self.sales[trans_date][sale_index]["unit_price"]
                    total_earned = self.sales[trans_date][sale_index]["total_revenue"]
                    trans_id = self.sales[trans_date][sale_index]["id"]
                    total_revenue += total_earned
                    report.append([trans_date, product, quantity,
                                   unit_price, total_earned, trans_id])

        if len(report) <= 1:
            console.print(f'No sale records found for date: {sell_date}')
            return False
        report.append([f'Total Revenue: ${round(total_revenue, 2)}'])
        return ['sales', report, sell_date]

    def get_profit_report(self, profit_date):
        '''returns total profit made over all time 
        or profit for a specific year/ month/ date'''
        is_day_report = len(profit_date) == 10
        report = []
        total_profit = 0

        if is_day_report and profit_date in self.sales:
            headers = ['Date', 'Qty x Product', 'Total Cost',
                       'Total Revenue', 'Total Profit']
            report.append(headers)
            for sale_index in range(len(self.sales[profit_date])):
                sale_id = self.sales[profit_date][sale_index]["id"]
                product_info = id_decoder(sale_id)
                product = product_info['product_name']
                quantity = product_info['sold_quantity']
                product_cost = product_info['total_cost']
                product_revenue = product_info['total_revenue']
                product_profit = product_info['total_profit']
                total_profit += product_profit
                report.append(
                    [profit_date, f'{quantity} x {product}', product_cost, product_revenue, product_profit])
        else:
            headers = ['Date', 'Total Cost', 'Total Revenue', 'Total Profit']
            report.append(headers)
            for trans_date in self.sales:
                if profit_date in trans_date:
                    day_profit = 0
                    day_revenue = 0
                    day_cost = 0
                    for sale_index in range(len(self.sales[trans_date])):
                        sale_id = self.sales[trans_date][sale_index]["id"]
                        product_info = id_decoder(sale_id)
                        product_cost = product_info['total_cost']
                        product_revenue = product_info['total_revenue']
                        product_profit = product_info['total_profit']
                        day_cost += product_cost
                        day_revenue += product_revenue
                        day_profit += product_profit
                    total_profit += day_profit
                    report.append(
                        [trans_date, day_cost, day_revenue, day_profit])

        if len(report) <= 1:
            console.print(f'No sale records found for date: {profit_date}')
            return False
        report.append([f'Total Profit: ${round(total_profit, 2)}'])
        return ['profit', report, profit_date]

    def get_low_stock_report(self, minimum_qty=10):
        '''returns a list of products that are low on stock'''
        report = []
        headers = ['Product Name', 'Quantity In Stock']
        report.append(headers)

        for product in self.inventory:
            quantity = self.inventory[product]
            if quantity <= minimum_qty:
                report.append([product, quantity])

        if len(report) <= 1:
            console.print(
                f'No items found with quantities lower than {minimum_qty}')
            return False
        return ['low stock', report]

    def get_expiry_report(self, current_inventory_date=current_day, num_of_days=7):
        '''returns a list of expired items or items 
        that expire within a specific num of days from now'''
        report = []
        headers = ["Product", "Quantity", "Days till expiry"]
        report.append(headers)

        for expiry_date in self.expiry_dates:
            # convert expiry date into date object
            product_exp_date = date.fromisoformat(expiry_date)
            current_date = date.fromisoformat(current_inventory_date)
            max_date = current_date + timedelta(days=num_of_days)
            if product_exp_date < current_date:  # if expiration date already passed
                for product in self.expiry_dates[expiry_date]:
                    quantity = self.expiry_dates[expiry_date][product]
                    report.append(
                        [product, quantity, f'EXPIRED on {expiry_date}'])
            elif product_exp_date <= max_date:  # if expiry date within specific amount of days
                for product in self.expiry_dates[expiry_date]:
                    quantity = self.expiry_dates[expiry_date][product]
                    time_till_expiry = abs(product_exp_date - current_date)
                    report.append(
                        [product, quantity, f'{time_till_expiry.days} days'])

        if len(report) <= 1:
            console.print(
                f'No items found that expire within {num_of_days} days')
            return False
        return ['expiry', report]

    def get_bestselling_days(self, trans_date):
        '''returns day(s) with most sales of all times
        or day(s) with most sales of a specific year / month '''
        report = []
        headers = ['Date', 'Total number of sales']
        report.append(headers)
        num_of_sales = 0
        best_selling_days = []

        for sales_date in self.sales:
            if trans_date in sales_date:
                day_sales = 0
                for sale_index in range(len(self.sales[sales_date])):
                    quantity = self.sales[sales_date][sale_index]["quantity"]
                    day_sales += quantity
                if day_sales > num_of_sales:
                    num_of_sales = day_sales
                    best_selling_days = [sales_date]
                elif day_sales == num_of_sales:
                    best_selling_days.append(sales_date)

        if best_selling_days:
            for day in best_selling_days:
                report.append([day, num_of_sales])

        if len(report) <= 1:
            console.print(f'No sale records found for date: {trans_date}')
            return False
        return ['best-selling days', report, trans_date]

    def get_bestselling_products(self, trans_date):
        '''returns best selling product(s) of all times or
        best selling product(s) of a specific year/ month/ date'''
        report = []
        headers = ['Product', 'Total quantity sold']
        report.append(headers)
        products_sold = {}
        num_of_sales = 0
        best_selling_prods = []

        for sales_date in self.sales:
            if trans_date in sales_date:
                for sale_index in range(len(self.sales[sales_date])):
                    product = self.sales[sales_date][sale_index]["product"]
                    quantity = self.sales[sales_date][sale_index]["quantity"]
                    if not (product in products_sold):
                        products_sold[product] = quantity
                    else:
                        products_sold[product] += quantity

        if products_sold:
            for product in products_sold:
                product_quantity = products_sold[product]
                if product_quantity > num_of_sales:
                    num_of_sales = product_quantity
                    best_selling_prods = [product]
                elif product_quantity == num_of_sales:
                    best_selling_prods.append(product)
            for product in best_selling_prods:
                report.append([product, num_of_sales])

        if len(report) <= 1:
            console.print(f'No sale records found for date: {trans_date}')
            return False
        return ['best-selling products', report, trans_date]

superpy = Super_inventory()

# add purch id to sales report i self.sales on every sale. adjust __init__ tmb
# either inventory or expiry dates needs to refer back to purch id. in plaats van apples: 3 prod_id: 3. if invemtory orei get inv report ta decode prod name, amd tells them all op bij elkaar
# on sale the qty after purchid gets updated
# product lookup: --product apples returns inventory qty di apples i onderverdeling
# i tur active purchid's ku tin e product name "apples" {apples: 8 - waarvan purchid1:5 -purchid2:3}
# id lookup --purch or sale id returns prodname, cost, price, qty and if its still in stock