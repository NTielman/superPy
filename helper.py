my_inventory = {
    "apples": {
        "quantity": 2,
        "expiry_date": "2020-01-01",
        "cost": 0.5,
        "price": 1
    },
    "bananas": {
        "quantity": 7,
        "expiry_date": "2021-07-01",
        "cost": 0.2,
        "price": 0.8
    },
    "oranges": {
        "quantity": 5,
        "expiry_date": "2022-02-06",
        "cost": 0.6,
        "price": 2
    },
    "kiwi's": {
        "quantity": 1,
        "expiry_date": "2021-01-17",
        "cost": 2,
        "price": 3
    },
    "watermelons": {
        "quantity": 3,
        "expiry_date": "2021-01-20",
        "cost": 5,
        "price": 15
    }
}

# formatting helpers
length = 50
scheidingslijn = '-' * length
header_lines = '#' * length


class Supermarket():
    purchases = {}
    sales = []
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

    def buy(self, product, quantity, cost, exp_date):
        # if product already in inventory
        if product in self.inventory:
            # update inventory quantity
            self.inventory[product]["quantity"] += quantity
            # update prod expiry list
        else:
            prod_info = {
                "quantity": quantity,
                "expiry_date": exp_date,
                "cost": cost,
                "price": 15
                # set price on sale or on purchase of product?
            }
            # add product to inventory
            self.inventory[product] = prod_info
        # if date not yet in expiry dates
        if not (exp_date in self.expiry_dates):
            # create a dict
            self.expiry_dates[exp_date] = {}
        # add products and prod quantities to expiry date
        self.expiry_dates[exp_date][product] = quantity
        # if purchase date not yet in purchases
        if not (current.date in self.purchases):
            # create a transaction (purchases) list
            self.purchases[current.date] = []
        # add purchase info to purchase date
        purchase_info = {
            "product": product,
            "quantity": quantity,
            "total_cost": round((cost*quantity), 2),
            "id": len(self.purchases[current.date]) + 1
        }
        self.purchases[current.date].append(purchase_info)

    def sell(self, product, quantity):
        if quantity > self.inventory[product]["quantity"]:
            print("not enough in stock to complete transaction")
        else:
            self.inventory[product]["quantity"] -= quantity
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

    # creates and returns a list of inventory report
    def get_inventory_report(self):
        report = []
        for product in self.inventory:
            report.append(
                f'| {product}\t | {self.inventory[product]["quantity"]}\t | {self.inventory[product]["cost"]}\t | {self.inventory[product]["expiry_date"]}\t |')
        return report, 'inventory'

    # returns list of all products in inventory
    def get_products_report(self):
        report = []
        for product in self.inventory:
            report.append(f'{product}')
        return report, 'products'

    def get_purchase_report(self, purchase_date='all'):
        report = []
        if purchase_date == 'all':
            # return all purchases
            for date in self.purchases:
                for purchase_num in range(len(self.purchases[date])):
                    product = self.purchases[date][purchase_num]["product"]
                    quantity = self.purchases[date][purchase_num]["quantity"]
                    total_cost = self.purchases[date][purchase_num]["total_cost"]
                    trans_id = self.purchases[date][purchase_num]["id"]
                    report.append(f'{date} | {product} | {quantity} | {total_cost} | {trans_id}')
        elif purchase_date in self.purchases:
            for purchase_num in range(len(self.purchases[purchase_date])):
                product = self.purchases[purchase_date][purchase_num]["product"]
                quantity = self.purchases[purchase_date][purchase_num]["quantity"]
                total_cost = self.purchases[purchase_date][purchase_num]["total_cost"]
                trans_id = self.purchases[purchase_date][purchase_num]["id"]
                report.append(f'{purchase_date} | {product} | {quantity} | {total_cost} | {trans_id}')
        else:
            report.append(f'No purchase records found for date: {purchase_date}')
        return report, 'purchases'

    # returns a list of products running low on stock
    def get_low_stock_report(self, max_stock_amount=2):
        report = []
        for product in self.inventory:
            prod_quantity = self.inventory[product]["quantity"]
            # if products remaining is less than max stock amount
            if prod_quantity <= max_stock_amount:
                report.append(
                    f'| Product: {product}\t | Product Quantity: {prod_quantity}')
        return report, 'low_stock'

    # returns a list of products costs per (1) unit
    def get_costs_report(self):
        report = []
        for product in self.inventory:
            cost = self.inventory[product]["cost"]
            report.append(
                f'Product: {product}\t | Cost: {cost}')
        return report, 'costs'

    # returns a list of expired or near expiring products
    def get_expiry_report(self):
        report = []
        for exp_date in self.expiry_dates:

            # convert date into integers
            expiry_date = exp_date.split('-')
            expiry_year = int(expiry_date[0])
            expiry_month = int(expiry_date[1])
            expiry_day = int(expiry_date[2])
            # compare expiry year to current year
            if expiry_year < current.year:
                for product in self.expiry_dates[exp_date]:
                    quantity = self.expiry_dates[exp_date][product]
                    report.append(
                        f'Product: {product} | Quantity: {quantity} | EXPIRED on {exp_date}')
            # if expiry year same as current year
            elif expiry_year == current.year:
                # compare expiry month to current month
                if expiry_month < current.month:
                    for product in self.expiry_dates[exp_date]:
                        quantity = self.expiry_dates[exp_date][product]
                        report.append(
                            f'Product: {product} | Quantity: {quantity} | EXPIRED on {exp_date}')
                # if product expires in current month
                elif expiry_month == current.month:
                    for product in self.expiry_dates[exp_date]:
                        quantity = self.expiry_dates[exp_date][product]
                        # compare expiry day to current day
                        if expiry_day < current.day:
                            report.append(
                                f'Product: {product} | Quantity: {quantity} | EXPIRED on {exp_date}')
                        else:
                            report.append(
                                f'Product: {product} | Quantity: {quantity} | expires soon in {expiry_day - current.day} days')
        return report, 'expiry'


class CurrentDate():
    def __init__(self, year=2021, month=1, day=11):
        self.year = year
        self.month = month
        self.day = day
        self.date = f'{year}-{month}-{day}'

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

# formats and prints out a report to console or to a csv file


def print_report(report):
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
        print('| Date | Product | Amnt | Total Cost | Transaction ID |')
        print(scheidingslijn)
    for line in report[0]:
        print(line)
        print(scheidingslijn)


current = CurrentDate()
superpy = Supermarket(my_inventory)

superpy.buy(product='mango\'s', quantity=10, exp_date="2020-01-01", cost=3 )
# print_report(superpy.get_products_report())
# print_report(superpy.get_costs_report())
# print_report(superpy.get_low_stock_report(4))
# print_report(superpy.get_expiry_report())
superpy.buy('bananas', 2, 0.2, "2021-05-01")
current.advance_time(2)
superpy.buy('bananas', 7, 0.2, "2021-05-03")
current.reverse_time(2)
#superpy.sell('bananas', 8)
print_report(superpy.get_purchase_report(current.date))
# print_report(superpy.get_inventory_report())
