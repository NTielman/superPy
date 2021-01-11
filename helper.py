my_inventory = {
    "apples": {
        "quantity": 2,
        "expiry_date": "2020-01-01",
        "cost": 0.5
    },
    "bananas": {
        "quantity": 7,
        "expiry_date": "2021-07-01",
        "cost": 0.2
    },
    "oranges": {
        "quantity": 5,
        "expiry_date": "2022-02-06",
        "cost": 0.6
    },
    "kiwi's": {
        "quantity": 1,
        "expiry_date": "2021-01-17",
        "cost": 2
    },
    "watermelons": {
        "quantity": 3,
        "expiry_date": "2021-01-20",
        "cost": 5
    }
}
length = 50
scheidingslijn = '-' * length
header_lines = '#' * length

class Supermarket():
    def __init__(self, inventory):
        self.inventory = inventory
    
    def buy(self, product, quantity):
        self.inventory[product]["quantity"] += quantity

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
            answer = input("Would you like to print a low-stock report? (y/n)\n")
            if answer == 'y':
                print_report(low_stock_report(self.inventory))
        elif message == "expires_soon":
            print("Warning: some items are close to expiring")
            answer = input("Would you like to print an expiry report? (y/n)\n")
            if answer == 'y':
                print_report(near_expiry_report(self.inventory))

class CurrentDate():
    def __init__(self, year=2021, month=1, day=11):
        self.year = year
        self.month = month
        self.day = day
    def advance_time(self, amount=1, time_unit='day'):
        if time_unit == 'day':
            self.day += amount
        elif time_unit == 'month':
            self.month += amount
        elif time_unit == 'year':
            self.year += amount
    def reset_time(self):
        self.year = 2021
        self.month = 1
        self.day = 11

# returns list of all products in inventory
def get_prod_list(inventory):
    product_list = []
    for product in inventory:
        product_list.append(f'{product}')
    return product_list, 'products'

# formats and prints out a report to console or to a csv file
def print_report(report):
    report_type = report[1]
    print(header_lines)
    if report_type == 'low_stock':
        print('LOW STOCK REPORT')
    elif report_type == 'sales':
        print('SALES REPORT')
    elif report_type == 'products':
        print('PRODUCTS REPORT')
    elif report_type == 'expiry':
        print('EXPIRY REPORT')
    elif report_type == 'prod_costs':
        print('COST PER UNIT REPORT')
    elif report_type == 'inventory':
        print('INVENTORY REPORT')
    print(header_lines)

    if report_type == 'inventory':
        print(scheidingslijn)
        print('| Product\t | Amnt | Cost\t | Expiry Date\t |')
        print(scheidingslijn)
    for line in report[0]:
        print(line)
        print(scheidingslijn)

# creates and returns a list of inventory report
def inventory_report(inventory):
    report = []
    for product in inventory:
        report.append(
            f'| {product}\t | {inventory[product]["quantity"]}\t | {inventory[product]["cost"]}\t | {inventory[product]["expiry_date"]}\t |')
    return report, 'inventory'

# returns a list of products running low on stock (pass in minimun stock amount)
def low_stock_report(inventory):
    low_stock_items = []
    for product in inventory:
        prod_quantity = inventory[product]["quantity"]
        # if 2 or less of product remaining
        if prod_quantity <= 2:
            low_stock_items.append(
                f'| Product: {product}\t | Product Quantity: {prod_quantity}')
    return low_stock_items, 'low_stock'

#returns a list of products near expiring (pass in num months from now) 
def near_expiry_report(inventory):
    expiry_list = []
    for product in inventory:
        expiry_date = inventory[product]["expiry_date"]
        expiry_date = expiry_date.split('-')
        expiry_year = int(expiry_date[0])
        expiry_month = int(expiry_date[1])
        expiry_day = int(expiry_date[2])
        if expiry_year < today.year:
            expiry_list.append(f'{product} EXPIRED last year in {expiry_year}')
        elif expiry_year == today.year:
            if expiry_month < today.month:
                expiry_list.append(f'{product} EXPIRED this year in {expiry_month}')
            elif expiry_month == today.month:
                if expiry_day < today.day:
                    expiry_list.append(f'{product} EXPIRED this month on {expiry_day}')
                else:
                    expiry_list.append(f'{product} expires soon in {expiry_day - today.day} days')
    return expiry_list, 'expiry'


# returns a list of products and their purchase price (cost) per (1) unit
def get_prod_costs(inventory):
    product_costs = []
    for product in inventory:
        product_costs.append(
            f'Product: {product}\t | Cost: {inventory[product]["cost"]}')
    return product_costs, 'prod_costs'

#print_report(inventory_report(my_inventory))
#print_report(get_prod_list(my_inventory))
#print_report(get_prod_costs(my_inventory))
#print_report(low_stock_report(my_inventory))
today = CurrentDate()
superpy = Supermarket(my_inventory)
#print_report(near_expiry_report(my_inventory))
#today.advance_time(amount=2, time_unit='month')
#print(today.month)
superpy.buy('bananas', 2)
superpy.sell('bananas', 8)
#print(superpy.inventory['bananas'])