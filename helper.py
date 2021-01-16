from datetime import date, timedelta, datetime
import csv
import os

current = date.today()
my_inventory = {
    "apples": {
        "quantity": 2,
        "expiry_date": "2020-01-01",
        "cost": 0.5,
    },
    "bananas": {
        "quantity": 7,
        "expiry_date": "2021-07-01",
        "cost": 0.2,
    },
    "oranges": {
        "quantity": 5,
        "expiry_date": "2022-02-06",
        "cost": 0.6,
    },
    "kiwi's": {
        "quantity": 3,
        "expiry_date": "2021-01-17",
        "cost": 2,
    },
    "watermelons": {
        "quantity": 3,
        "expiry_date": "2021-01-20",
        "cost": 5,
    }
}


class Supermarket():
    purchases = {}
    sales = {}
    expiry_dates = {}

    def __init__(self, inventory={}):
        # if no inventory is passed in, initialise to empty dict
        self.inventory = inventory
        # if inventory not empty
        if inventory:
            for product in inventory:
                # extract needed info into variables
                #self.buy(product=product, quantity=quantity)
                expiry_date = inventory[product]["expiry_date"]
                quantity = inventory[product]["quantity"]
                # if date not yet in expiry dates
                if not (expiry_date in self.expiry_dates):
                    # create a dict
                    self.expiry_dates[expiry_date] = {}
                # add products and prod quantities to expiry date
                self.expiry_dates[expiry_date][product] = quantity

    def discard_items(self, product, exp_date, quantity=1):
        '''removes a specific item from inventory'''
        if quantity >= self.inventory[product]["quantity"]:
            del self.inventory[product]
        else:
            self.inventory[product]["quantity"] -= quantity
        # remove items from expiry dates
        if quantity >= self.expiry_dates[exp_date][product]:
            del self.expiry_dates[exp_date][product]
        else:
            self.expiry_dates[exp_date][product] -= quantity

    def buy(self, product, quantity, cost_per_unit, exp_date):
        '''adds a product to inventory and
        adds product info to purchase records'''
        if product in self.inventory:
            self.inventory[product]["quantity"] += quantity
        else:
            prod_info = {
                "quantity": quantity,
                "expiry_date": exp_date,
                "cost": cost_per_unit,
            }
            # add product to inventory
            self.inventory[product] = prod_info
        # if date not yet in expiry dates
        if not (exp_date in self.expiry_dates):
            # create a dict
            self.expiry_dates[exp_date] = {}
        # if product not yet in dict
        if not (product in self.expiry_dates[exp_date]):
            # add products and prod quantities to expiry date
            self.expiry_dates[exp_date][product] = quantity
        else:
            self.expiry_dates[exp_date][product] += quantity
        # if purchase date not yet in purchases
        current_date = current.isoformat()
        if not (current_date in self.purchases):
            # create a transaction (purchases) list
            self.purchases[current_date] = []
        # add purchase info to purchase date
        transaction_id = f'#SUP{current.strftime("%y%m%d")}PURCH0{len(self.purchases[current_date]) + 1}'
        purchase_info = {
            "product": product,
            "quantity": quantity,
            "unit_cost": cost_per_unit,
            "total_cost": round((cost_per_unit*quantity), 2),
            "expiry_date": exp_date,
            "id": transaction_id
        }
        self.purchases[current_date].append(purchase_info)
        return f'items added to inventory. Transaction ID: {transaction_id}'

    def sell(self, product, quantity, price_per_unit, purchase_id):
        '''removes a product from inventory and
        adds product info to sales records'''
        if not (product in self.inventory):
            return f"product: {product} not in stock"
        if quantity > self.inventory[product]["quantity"]:
            return "not enough in stock to complete transaction"
        # extract product info from purchase id
        id_date = datetime.strptime(purchase_id[4:10], "%y%m%d")
        purchase_index = int(purchase_id[15:17]) - 1
        purchase_date = id_date.strftime("%Y-%m-%d")
        if not purchase_date in self.purchases:
            return "purchase ID not found"
        exp_date = self.purchases[purchase_date][purchase_index]["expiry_date"]
        unit_cost = self.purchases[purchase_date][purchase_index]["unit_cost"]
        if quantity > self.expiry_dates[exp_date][product]:
            # ensure items of differing expiration dates are entered seperately
            return "incorrect quantity or purchase ID provided"
        # reduce product inventory quantities
        self.inventory[product]["quantity"] -= quantity
        # remove products and prod quantities from expiry date
        if quantity >= self.expiry_dates[exp_date][product]:
            del self.expiry_dates[exp_date][product]
        else:
            self.expiry_dates[exp_date][product] -= quantity
        # if transaction date not yet in sales
        current_date = current.isoformat()
        if not (current_date in self.sales):
            # create a transaction (sales) list
            self.sales[current_date] = []
        # add sale info to transaction date
        transaction_id = f'#SUP{current.strftime("%y%m%d")}SALE0{len(self.sales[current_date]) + 1}'
        sale_info = {
            "product": product,
            "quantity": quantity,
            "unit_cost": unit_cost,
            "unit_price": price_per_unit,
            "total_income": round((price_per_unit*quantity), 2),
            "id": transaction_id
        }
        self.sales[current_date].append(sale_info)
        products_left = self.inventory[product]["quantity"]
        if products_left == 0:
            del self.inventory[product]
        elif products_left <= 5:
            self.warn("low_stock")

    def warn(self, message):
        if message == "low_stock":
            print("Warning: some items are low on stock")
            answer = input(
                "Would you like to print a low-stock report? (y/n)\n")
            if answer == 'y':
                print_report(self.get_low_stock_report())
        elif message == "expires_soon":
            print("Warning: some items are close to expiring")
            answer = input("Would you like to print an expiry report? (y/n)\n")
            if answer == 'y':
                print_report(self.get_expiry_report())
        elif message == "expired_items":
            print("Warning: some items have expired")
            print("Consider discarding the items from inventory")

    def get_inventory_report(self):
        '''returns a list of products and product quantities
        that the supermarket currently holds'''
        report = []
        for product in self.inventory:
            report.append(
                f'{product:<20}| {self.inventory[product]["quantity"]}')
        return report, 'inventory'

    def get_products_report(self):
        '''returns a list of all products the supermarket offers'''
        report = []
        for product in self.inventory:
            report.append(f'{product}')
        return report, 'products'

    def get_purchase_report(self, purchase_date='all'):
        '''returns all purchase transactions 
        or all purchases made on a specific date'''
        report = []
        total_cost = 0
        if purchase_date == 'all':
            for date in self.purchases:
                for purchase_num in range(len(self.purchases[date])):
                    product = self.purchases[date][purchase_num]["product"]
                    quantity = self.purchases[date][purchase_num]["quantity"]
                    unit_cost = self.purchases[date][purchase_num]["unit_cost"]
                    total_spent = self.purchases[date][purchase_num]["total_cost"]
                    expiry_date = self.purchases[date][purchase_num]["expiry_date"]
                    trans_id = self.purchases[date][purchase_num]["id"]
                    total_cost += total_spent
                    report.append(
                        f'{date:<11}| {product:<10}| {quantity:<8}| {unit_cost:<10}| {total_spent:<8}| {expiry_date:<11}| {trans_id}')
        elif purchase_date in self.purchases:
            for purchase_num in range(len(self.purchases[purchase_date])):
                product = self.purchases[purchase_date][purchase_num]["product"]
                quantity = self.purchases[purchase_date][purchase_num]["quantity"]
                unit_cost = self.purchases[purchase_date][purchase_num]["unit_cost"]
                total_spent = self.purchases[purchase_date][purchase_num]["total_cost"]
                expiry_date = self.purchases[purchase_date][purchase_num]["expiry_date"]
                trans_id = self.purchases[purchase_date][purchase_num]["id"]
                total_cost += total_spent
                report.append(
                    f'{purchase_date:<11}| {product:<10}| {quantity:<8}| {unit_cost:<10}| {total_spent:<10}| {expiry_date:<10}| {trans_id}')
        else:
            report.append(
                f'No purchase records found for date: {purchase_date}')
        report.append(f'Total Cost: ${round(total_cost, 2)}')
        return report, 'purchases'

    def get_sales_report(self, sell_date='all'):
        '''returns all sales transactions 
        or all sales made on a specific date'''
        report = []
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
                    report.append(
                        f'{date:<11}| {product:<15}| {quantity:<10}| {unit_price:<13}| {total_income:<10}| {trans_id}')
        elif sell_date in self.sales:
            for sale_num in range(len(self.sales[sell_date])):
                product = self.sales[sell_date][sale_num]["product"]
                quantity = self.sales[sell_date][sale_num]["quantity"]
                unit_price = self.sales[sell_date][sale_num]["unit_price"]
                total_income = self.sales[sell_date][sale_num]["total_income"]
                trans_id = self.sales[sell_date][sale_num]["id"]
                total_revenue += total_income
                report.append(
                    f'{sell_date:<11}| {product:<15}| {quantity:<10}| {unit_price:<13}| {total_income:<10}| {trans_id}')
        else:
            report.append(f'No sale records found for date: {sell_date}')
        report.append(f'Total Revenue: ${round(total_revenue, 2)}')
        return report, 'sales'

    def get_profit_report(self, profit_date="all"):
        '''returns total profit made over time 
        or profit made on a specific date'''
        report = []
        total_profit = 0
        if profit_date == 'all':
            for date in self.sales:
                day_profit = 0
                day_revenue = 0
                day_cost = 0
                for sale_num in range(len(self.sales[date])):
                    quantity = self.sales[date][sale_num]["quantity"]
                    unit_cost = self.sales[date][sale_num]["unit_cost"]
                    product_cost = unit_cost * quantity
                    product_revenue = self.sales[date][sale_num]["total_income"]
                    product_profit = product_revenue - product_cost
                    day_cost += product_cost
                    day_revenue += product_revenue
                    day_profit += product_profit
                total_profit += day_profit
                report.append(
                    f'{date:<11}| {"":<20}| {day_cost:<15}| {day_revenue:<15}| {day_profit}')
        elif profit_date in self.sales:
            for sale_num in range(len(self.sales[profit_date])):
                product = self.sales[profit_date][sale_num]["product"]
                quantity = self.sales[profit_date][sale_num]["quantity"]
                unit_cost = self.sales[profit_date][sale_num]["unit_cost"]
                product_cost = unit_cost * quantity
                product_revenue = self.sales[profit_date][sale_num]["total_income"]
                product_profit = product_revenue - product_cost
                total_profit += product_profit
                report.append(
                    f'{profit_date:<11}| {str(quantity) + " x " + product:<20}| {product_cost:<15}| {product_revenue:<15}| {product_profit}')
        else:
            report.append(f'No sale records found for date: {profit_date}')
        report.append(f'Total Profit: ${round(total_profit, 2)}')
        return report, 'profit'

    def get_low_stock_report(self, max_stock_amount=2):
        '''returns a list of products that are out of stock 
        or running low on stock'''
        report = []
        for product in self.inventory:
            prod_quantity = self.inventory[product]["quantity"]
            # if products remaining is less than max stock amount
            if prod_quantity == 0:
                report.append(
                    f'Product: {product} OUT OF STOCK')
            elif prod_quantity <= max_stock_amount:
                report.append(
                    f'Product: {product:<20}| Quantity: {prod_quantity}')
        return report, 'low stock'

    def get_expiry_report(self, num_of_days=7):
        '''returns a list of expired items or 
        items that expire a specific set of days from now'''
        report = []
        expired_items = 0
        for exp_date in self.expiry_dates:
            # convert expiry date into date object
            expiry_date = date.fromisoformat(exp_date)
            max_date = current + timedelta(days=num_of_days)
            # if product already expired
            if expiry_date < current:
                for product in self.expiry_dates[exp_date]:
                    quantity = self.expiry_dates[exp_date][product]
                    report.append(
                        f'Product: {product:<15}| Quantity: {quantity:<10}| EXPIRED on {exp_date}')
                    expired_items += 1
            # if expiry date within specific amount of days
            elif expiry_date <= max_date:
                for product in self.expiry_dates[exp_date]:
                    quantity = self.expiry_dates[exp_date][product]
                    time_till_expiry = abs(expiry_date - current)
                    report.append(
                        f'Product: {product:<15}| Quantity: {quantity:<10}| expires soon in {time_till_expiry.days} days')
        if expired_items > 0:
            self.warn("expired_items")
        return report, 'expiry'

    def get_bestselling_days(self, year='', month=''):
        '''returns days with most sales transactions of all times
        or days with most sales transactions of a specific month and year '''
        report = []
        num_of_sales = 0
        if year == '' and month == '':
            # return bestselling days of all time
            # find the highest num of daily sales
            for sales_date in self.sales:
                day_sales = len(self.sales[sales_date])
                if day_sales > num_of_sales:
                    num_of_sales = day_sales
            # find dates with this number of sales
            for sales_date in self.sales:
                if len(self.sales[sales_date]) == num_of_sales:
                    report.append(sales_date)
        elif year != '' and month != '':
            # return bestselling days of specific year and month
            for sales_date in self.sales:
                if f'{year}-{month}' in sales_date:
                    day_sales = len(self.sales[sales_date])
                    if day_sales > num_of_sales:
                        num_of_sales = day_sales
            for sales_date in self.sales:
                if f'{year}-{month}' in sales_date:
                    if len(self.sales[sales_date]) == num_of_sales:
                        report.append(sales_date)
        elif year != '' or month != '':
            # return bestselling days for specific year or month
            for sales_date in self.sales:
                sales_year = sales_date[:4]
                sales_month = sales_date[5:7]
                if sales_year == year or sales_month == month:
                    day_sales = len(self.sales[sales_date])
                    if day_sales > num_of_sales:
                        num_of_sales = day_sales
            for sales_date in self.sales:
                sales_year = sales_date[:4]
                sales_month = sales_date[5:7]
                if sales_year == year or sales_month == month:
                    if len(self.sales[sales_date]) == num_of_sales:
                        report.append(sales_date)
        report.append(f'Total transactions made per day: {num_of_sales}')
        return report, 'best-selling days'

    def get_bestselling_products(self, year='', month=''):
        '''returns the best selling products of all times
        or best selling products of a specific month and year'''
        report = []
        num_of_sales = 0
        products_sold = {}
        if year == '' and month == '':
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
        elif year != '' and month != '':
            # return bestselling products of specific year and month
            for sales_date in self.sales:
                if f'{year}-{month}' in sales_date:
                    # find all products sold and quantities sold
                    for sale_index in range(len(self.sales[sales_date])):
                        product = self.sales[sales_date][sale_index]["product"]
                        quantity = self.sales[sales_date][sale_index]["quantity"]
                        if not (product in products_sold):
                            products_sold[product] = quantity
                        else:
                            products_sold[product] += quantity
        elif year != '' or month != '':
            # return bestselling products for specific year or month
            for sales_date in self.sales:
                sales_year = sales_date[:4]
                sales_month = sales_date[5:7]
                if sales_year == year or sales_month == month:
                    # find all products sold and quantities sold
                    for sale_index in range(len(self.sales[sales_date])):
                        product = self.sales[sales_date][sale_index]["product"]
                        quantity = self.sales[sales_date][sale_index]["quantity"]
                        if not (product in products_sold):
                            products_sold[product] = quantity
                        else:
                            products_sold[product] += quantity
        # find highest product quantity
        for product in products_sold:
            product_quantity = products_sold[product]
            if product_quantity > num_of_sales:
                num_of_sales = product_quantity
        # find products with this number of sales
        for product in products_sold:
            product_quantity = products_sold[product]
            if product_quantity == num_of_sales:
                report.append(product)
        report.append(f'Total amount of product(s) sold: {num_of_sales}')
        return report, 'best-selling products'

def console_report():
    '''formats report for printing to console'''
    return None
#both called by print report function
def csv_report():
    '''formats report for writing to csv file'''
    return None

def print_report(report):
    '''formats and prints out a report to console 
    or to a csv file '''
    line_length = 90
    header_lines = '#' * line_length
    division_line = '_' * line_length
    report_type = report[1]

    # print report title and header
    print('\n')
    print(header_lines)
    print(f'{report_type.upper() + " REPORT":^90}')
    print(header_lines)

    # print subheader info for specific types of report
    if report_type == 'inventory':
        print(f'{"Product Name":<20}| Amount In Stock')
        print(division_line)
    elif report_type == 'purchases':
        print(f'{"Date":<11}| {"Product":<10}| {"Amnt":<8}| {"Unit Cost":<10}| {"Total":<8}| {"Exp Date":<11}| Transaction ID')
        print(division_line)
    elif report_type == 'sales':
        print(f'{"Date":<11}| {"Product":<15}| {"Amnt":<10}| {"Unit Price":<13}| {"Total":<10}| Transaction ID')
        print(division_line)
    elif report_type == 'profit':
        print(f'{"Date":<11}| {"Amnt x Product":<20}| {"Total Cost":<15}| {"Total Revenue":<15}| Total Profit')
        print(division_line)

    # print report body
    for line in report[0]:
        print(line)
        print(division_line)


superpy = Supermarket(my_inventory)
superpy.buy(product='mango\'s', quantity=10,
            exp_date="2020-01-01", cost_per_unit=3)
# print_report(superpy.get_low_stock_report(4))
superpy.buy('bananas', 2, 0.2, "2021-05-01")
superpy.buy('kiwi\'s', 6, 1, "2022-06-01")
# current += timedelta(days=2) #def advance_time(num_days)
superpy.buy('bananas', 7, 0.2, "2021-05-03")

superpy.sell(product='mango\'s', quantity=10,
             purchase_id="#SUP210116PURCH01", price_per_unit=10)
# current -= timedelta(days=365)  # current.reverse_time(2)
superpy.sell(product='bananas', quantity=5,
             purchase_id="#SUP210116PURCH04", price_per_unit=2)
superpy.sell(product='kiwi\'s', quantity=3,
             purchase_id="#SUP210116PURCH03", price_per_unit=5)
print_report(superpy.get_purchase_report())
# print_report(superpy.get_sales_report())
#superpy.discard_items(product='bananas', exp_date="2021-05-01", quantity=2)
# print_report(superpy.get_inventory_report())
# print_report(superpy.get_profit_report(profit_date="2021-01-16"))
# print_report(superpy.get_expiry_report())
# print_report(superpy.get_products_report())
# print_report(superpy.get_bestselling_days(month="01"))
# print_report(superpy.get_bestselling_products())
