from datetime import date, timedelta
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
        # if product already in inventory
        if product in self.inventory:
            # update inventory quantity
            self.inventory[product]["quantity"] += quantity
            # update prod expiry list
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
        transaction_id = f'#SUP{current.strftime("%Y%m%d")}PURCH0{len(self.purchases[current_date]) + 1}'
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
        if not (product in self.inventory):
            return f"product: {product} not in stock"
        if quantity > self.inventory[product]["quantity"]:
            return "not enough in stock to complete transaction"
        # extract product info from purchase id
        # '#SUP20210114PURCH01'
        #  ----yyyymmdd-----ii
        #  0123456789012345678
        year = purchase_id[4:8]
        month = purchase_id[8:10]
        day = purchase_id[10:12]
        purchase_index = int(purchase_id[17:19]) - 1
        purchase_date = f"{year}-{month}-{day}"
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
        transaction_id = f'#SUP{current.strftime("%Y%m%d")}SALE0{len(self.sales[current_date]) + 1}'
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
                f'| {product}\t | {self.inventory[product]["quantity"]}\t | {self.inventory[product]["cost"]}\t | {self.inventory[product]["expiry_date"]}\t |')
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
                        f'{date} | {product} | {quantity} | {unit_cost} | {total_spent} | {expiry_date} | {trans_id}')
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
                    f'{purchase_date} | {product} | {quantity} | {unit_cost} | {total_spent} | {expiry_date} | {trans_id}')
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
                        f'{date} | {product} | {quantity} | {unit_price} | {total_income} | {trans_id}')
        elif sell_date in self.sales:
            for sale_num in range(len(self.sales[sell_date])):
                product = self.sales[sell_date][sale_num]["product"]
                quantity = self.sales[sell_date][sale_num]["quantity"]
                unit_price = self.sales[sell_date][sale_num]["unit_price"]
                total_income = self.sales[sell_date][sale_num]["total_income"]
                trans_id = self.sales[sell_date][sale_num]["id"]
                total_revenue += total_income
                report.append(
                    f'{sell_date} | {product} | {quantity} | {unit_price} | {total_income} | {trans_id}')
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
                for sale_num in range(len(self.sales[date])):
                    quantity = self.sales[date][sale_num]["quantity"]
                    unit_cost = self.sales[date][sale_num]["unit_cost"]
                    product_cost = unit_cost * quantity
                    product_revenue = self.sales[date][sale_num]["total_income"]
                    product_profit = product_revenue - product_cost
                    day_profit += product_profit
                total_profit += day_profit
                report.append(f'{date} | {day_profit}')
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
                    f'{profit_date} | {quantity} x {product} | {product_cost} | {product_revenue} | {product_profit}')
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
                    f'| Product: {product} OUT OF STOCK')
            elif prod_quantity <= max_stock_amount:
                report.append(
                    f'| Product: {product}\t | Product Quantity: {prod_quantity}')
        return report, 'low stock'

    # returns a list of products costs per (1) unit
    # delete this
    def get_costs_report(self):
        report = []
        for product in self.inventory:
            cost = self.inventory[product]["cost"]
            report.append(
                f'Product: {product}\t | Cost: {cost}')
        return report, 'costs'

    def get_bestselling_days(self, year='', month=''):
        '''returns the most profitable days (most sales) of all times
        or most profitable days of a specific month and year'''
        best_dates = []
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
                    best_dates.append(sales_date)
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
                        best_dates.append(sales_date)
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
                        best_dates.append(sales_date)
        print(f'Date(s) with most sales are:')
        print(", ".join(best_dates))
        print(f'number of sales on day(s): {num_of_sales}')
        return best_dates

    def get_bestselling_products(self, year='', month=''):
        '''returns the best selling products of all times
        or best selling products of a specific month and year'''
        best_products = []
        num_of_sales = 0
        if year == '' and month == '':
            # return bestselling products of all time
            products_sold = {}
            for sales_date in self.sales:
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
                    best_products.append(product)
        elif year != '' and month != '':
            # return bestselling products of specific year and month
            products_sold = {}
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
            # find highest product quantity
            for product in products_sold:
                product_quantity = products_sold[product]
                if product_quantity > num_of_sales:
                    num_of_sales = product_quantity
            # find products with this number of sales
            for product in products_sold:
                product_quantity = products_sold[product]
                if product_quantity == num_of_sales:
                    best_products.append(product)
        elif year != '' or month != '':
            # return bestselling products for specific year or month
            products_sold = {}
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
                    best_products.append(product)
        print(f'Product(s) with most sales are:')
        print(", ".join(best_products))
        print(f'quantity sold: {num_of_sales}')
        return best_products

    def get_expiry_report(self, num_of_days=7):
        '''returns a list of expired items or 
        items that expire a specific set of days from now'''
        report = []
        expired_items = 0
        for exp_date in self.expiry_dates:
            # convert expiry date into date object
            expiry_date = date.fromisoformat(exp_date)
            max_date = current + timedelta(days=num_of_days)
            # compare expiry date to current date
            if expiry_date < current:  # if product already expired
                for product in self.expiry_dates[exp_date]:
                    quantity = self.expiry_dates[exp_date][product]
                    report.append(
                        f'Product: {product} | Quantity: {quantity} | EXPIRED on {exp_date}')
                    expired_items += 1
            # if expiry date within specific amount of days
            elif expiry_date <= max_date:
                for product in self.expiry_dates[exp_date]:
                    quantity = self.expiry_dates[exp_date][product]
                    time_till_expiry = abs(expiry_date - current)
                    report.append(
                        f'Product: {product} | Quantity: {quantity} | expires soon in {time_till_expiry.days} days')
        if expired_items > 0:
            self.warn("expired_items")
        return report, 'expiry'


def print_report(report):
    '''formats and prints out a report to console 
    or to a csv file '''
    # formatting helpers
    length = 90
    scheidingslijn = '-' * length
    header_lines = '#' * length
    report_type = report[1]
    print(header_lines)
    print(f'{report_type.upper()} REPORT')
    print(header_lines)

    if report_type == 'inventory':
        print(scheidingslijn)
        print('| Product\t | Amnt | Cost\t | Expiry Date\t |')
        print(scheidingslijn)
    elif report_type == 'purchases':
        print(scheidingslijn)
        print('| Date | Product | Amnt | Cost Per Unit | Total Spent | Expiry Date | Transaction ID |')
        print(scheidingslijn)
    elif report_type == 'sales':
        print(scheidingslijn)
        print('| Date | Product | Amnt | Price per Unit | Total Earned | Transaction ID |')
        print(scheidingslijn)
    elif report_type == 'profit':
        print(scheidingslijn)
        print('| Date | Amnt x Product | Total Cost | Total Revenue |Total Profit |')
        print(scheidingslijn)
    for line in report[0]:
        print(line)
        print(scheidingslijn)


superpy = Supermarket(my_inventory)
superpy.buy(product='mango\'s', quantity=10,
            exp_date="2020-01-01", cost_per_unit=3)
# print_report(superpy.get_costs_report())
# print_report(superpy.get_low_stock_report(4))
superpy.buy('bananas', 2, 0.2, "2021-05-01")
superpy.buy('kiwi\'s', 6, 1, "2022-06-01")
#superpy.sell('kiwi\'s', 1, 2, "2021-01-17")
# current += timedelta(days=2) #def advance_time(num_days)
superpy.buy('bananas', 7, 0.2, "2021-05-03")

superpy.sell(product='mango\'s', quantity=10,
             purchase_id="#SUP20210115PURCH01", price_per_unit=10)
current -= timedelta(days=365)  # current.reverse_time(2)
superpy.sell(product='bananas', quantity=5,
             purchase_id="#SUP20210115PURCH04", price_per_unit=2)
superpy.sell(product='kiwi\'s', quantity=3,
             purchase_id="#SUP20210115PURCH03", price_per_unit=5)
# print_report(superpy.get_purchase_report())
print_report(superpy.get_sales_report())
#superpy.discard_items(product='bananas', exp_date="2021-05-01", quantity=2)
# print_report(superpy.get_inventory_report())
# print_report(superpy.get_profit_report())
# print_report(superpy.get_expiry_report())
# print_report(superpy.get_products_report())
# superpy.get_bestselling_days(month="01")
superpy.get_bestselling_products(month="01", year="2020")
