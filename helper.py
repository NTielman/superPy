from datetime import date, timedelta

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

# formatting helpers
length = 50
scheidingslijn = '-' * length
header_lines = '#' * length


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
        transaction_id = f'#SUP{current.strftime("%y%m%d")}PURCH0{len(self.purchases[current_date]) + 1}'
        purchase_info = {
            "product": product,
            "quantity": quantity,
            "total_cost": round((cost_per_unit*quantity), 2),
            "id": transaction_id
        }
        self.purchases[current_date].append(purchase_info)

    def sell(self, product, quantity, price_per_unit, exp_date):
        if quantity > self.inventory[product]["quantity"]:
            return "not enough in stock to complete transaction"
        elif quantity > self.expiry_dates[exp_date][product]:
            # ensure items of differing expiration dates are entered seperately
            return "incorrect quantity or expiration date provided"
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
            "total_income": round((price_per_unit*quantity), 2),
            "id": transaction_id
        }
        self.sales[current_date].append(sale_info)
        products_left = self.inventory[product]["quantity"]
        if products_left <= 1:
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

    # creates and returns a list of inventory report
    def get_inventory_report(self):
        report = []
        for product in self.inventory:
            report.append(
                f'| {product}\t | {self.inventory[product]["quantity"]}\t | {self.inventory[product]["cost"]}\t | {self.inventory[product]["expiry_date"]}\t |')
        return report, 'inventory'

    def get_products_report(self):
        '''returns a list of all products in inventory'''
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
            # return all purchases
            for date in self.purchases:
                for purchase_num in range(len(self.purchases[date])):
                    product = self.purchases[date][purchase_num]["product"]
                    quantity = self.purchases[date][purchase_num]["quantity"]
                    total_spent = self.purchases[date][purchase_num]["total_cost"]
                    trans_id = self.purchases[date][purchase_num]["id"]
                    total_cost += total_spent
                    report.append(
                        f'{date} | {product} | {quantity} | {total_spent} | {trans_id}')
        elif purchase_date in self.purchases:
            for purchase_num in range(len(self.purchases[purchase_date])):
                product = self.purchases[purchase_date][purchase_num]["product"]
                quantity = self.purchases[purchase_date][purchase_num]["quantity"]
                total_spent = self.purchases[purchase_date][purchase_num]["total_cost"]
                trans_id = self.purchases[purchase_date][purchase_num]["id"]
                total_cost += total_spent
                report.append(
                    f'{purchase_date} | {product} | {quantity} | {total_spent} | {trans_id}')
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
            # return all sales
            for date in self.sales:
                for sale_num in range(len(self.sales[date])):
                    product = self.sales[date][sale_num]["product"]
                    quantity = self.sales[date][sale_num]["quantity"]
                    total_income = self.sales[date][sale_num]["total_income"]
                    trans_id = self.sales[date][sale_num]["id"]
                    total_revenue += total_income
                    report.append(
                        f'{date} | {product} | {quantity} | {total_income} | {trans_id}')
        elif sell_date in self.sales:
            for sale_num in range(len(self.sales[sell_date])):
                product = self.sales[sell_date][sale_num]["product"]
                quantity = self.sales[sell_date][sale_num]["quantity"]
                total_income = self.sales[sell_date][sale_num]["total_income"]
                trans_id = self.sales[sell_date][sale_num]["id"]
                total_revenue += total_income
                report.append(
                    f'{sell_date} | {product} | {quantity} | {total_income} | {trans_id}')
        else:
            report.append(f'No sale records found for date: {sell_date}')
        report.append(f'Total Revenue: ${round(total_revenue, 2)}')
        return report, 'sales'

    def get_low_stock_report(self, max_stock_amount=2):
        '''returns a list of products that are out of stock 
        or running low on stock'''
        report = []
        for product in self.inventory:
            prod_quantity = self.inventory[product]["quantity"]
            # if products remaining is less than max stock amount
            if prod_quantity <= max_stock_amount:
                report.append(
                    f'| Product: {product}\t | Product Quantity: {prod_quantity}')
        return report, 'low_stock'

    # returns a list of products costs per (1) unit
    # delete this
    def get_costs_report(self):
        report = []
        for product in self.inventory:
            cost = self.inventory[product]["cost"]
            report.append(
                f'Product: {product}\t | Cost: {cost}')
        return report, 'costs'

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


class CurrentDate():

    def advance_time(self, num_of_days):
        # try catch value error if days is not int
        self.day += num_of_days
        self.date = f'{self.year}-{self.month}-{self.day}'
        return f'Current Date is: {self.date}'

    def reverse_time(self, num_of_days):
        # try catch value error if days is not int
        self.day -= num_of_days
        self.date = f'{self.year}-{self.month}-{self.day}'
        return f'Current Date is: {self.date}'

    # set to current date
    def reset_time(self):
        self.year = 2021
        self.month = 1
        self.day = 11


def print_report(report):
    '''formats and prints out a report to console 
    or to a csv file'''
    report_type = report[1]
    print(header_lines)
    if report_type == 'low_stock':
        print('LOW STOCK REPORT')
    elif report_type == 'sales':
        print('SALES REPORT')
    elif report_type == 'purchases':
        print('PURCHASES REPORT')
    elif report_type == 'products':
        print('PRODUCTS REPORT')
    elif report_type == 'expiry':
        print('EXPIRY REPORT')
    elif report_type == 'costs':
        print('COST PER UNIT REPORT')
    elif report_type == 'inventory':
        print('INVENTORY REPORT')
    print(header_lines)

    if report_type == 'inventory':
        print(scheidingslijn)
        print('| Product\t | Amnt | Cost\t | Expiry Date\t |')
        print(scheidingslijn)
    elif report_type == 'purchases':
        print(scheidingslijn)
        print('| Date | Product | Amnt | Total Spent | Transaction ID |')
        print(scheidingslijn)
    elif report_type == 'sales':
        print(scheidingslijn)
        print('| Date | Product | Amnt | Total Earned | Transaction ID |')
        print(scheidingslijn)
    for line in report[0]:
        print(line)
        print(scheidingslijn)


#superpy = Supermarket(my_inventory)
#superpy.buy(product='mango\'s', quantity=10, exp_date="2020-01-01", cost_per_unit=3)
# print_report(superpy.get_products_report())
# print_report(superpy.get_costs_report())
# print_report(superpy.get_low_stock_report(4))
# print_report(superpy.get_expiry_report())
#superpy.buy('bananas', 2, 0.2, "2021-05-01")
#superpy.buy('bananas', 7, 0.2, "2021-05-03")
# current.reverse_time(2)
#superpy.sell('kiwi\'s', 1, 2, "2021-01-17")
# current.advance_time(2)
#superpy.sell(product='mango\'s', quantity=5, exp_date="2020-01-01", price_per_unit=10 )
# print_report(superpy.get_purchase_report())
# print_report(superpy.get_sales_report())
#superpy.discard_items(product='bananas', exp_date="2021-05-01", quantity=2)
# print_report(superpy.get_inventory_report())
