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
    }
}
scheidingslijn = '-' * 54
header_lines = '#' * 54
current_month = 1
current_day = 11
current_year = 2021

# returns list of all products in inventory
def get_prod_list(inventory):
    product_list = []
    for product in inventory:
        product_list.append(f'{product}')
    return product_list

# formats and prints out a report to console or to a csv file
def print_report(report):
    report_type = report[1]
    print(header_lines)
    if report_type == 'low_stock':
        print('LOW STOCK REPORT')
    elif report_type == 'sales':
        print('SALES REPORT')
    elif report_type == 'expiry':
        print('EXPIRY REPORT')
    elif report_type == 'inventory':
        print('INVENTORY REPORT')
    print(header_lines)

    if report_type == 'inventory':
        print(scheidingslijn)
        print('| Product Name | Count | Buy Price | Expiration Date |')
        print(scheidingslijn)
    for line in report[0]:
        print(line)
        print(scheidingslijn)

# creates and returns a list of inventory report
def inventory_report(inventory):
    report = []
    for product in inventory:
        report.append(
            f'| {product}\t | {inventory[product]["quantity"]}\t | {inventory[product]["purchase_price"]}\t | {inventory[product]["expiry_date"]}\t |')
    return report, 'inventory'

# returns a list of products running low on stock (pass in minimun stock amount)
def low_stock_report(inventory):
    low_stock_items = []
    for product in inventory:
        prod_quantity = inventory[product]["quantity"]
        # if 2 or less of product remaining
        if prod_quantity <= 2:
            low_stock_items.append(
                f'| Product Name: {product} | Product Quantity: {prod_quantity}')
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
        if expiry_year < current_year:
            expiry_list.append(f'{product} EXPIRED last year in {expiry_year}')
        elif expiry_year == current_year:
            if expiry_month < current_month:
                expiry_list.append(f'{product} EXPIRED this year in {expiry_month}')
            elif expiry_month == current_month:
                if expiry_day < current_day:
                    expiry_list.append(f'{product} EXPIRED this month on {expiry_day}')
                else:
                    expiry_list.append(f'{product} expires soon in {expiry_day - current_day} days')
    return expiry_list, 'expiry'


# returns a list of products and their purchase price (cost) per (1) unit
def get_prod_costs(inventory):
    product_costs = []
    for product in inventory:
        product_costs.append(
            f'Product Name: {product} | Cost: {inventory[product]["cost"]}')
    return product_costs


# print_report(inventory_report(my_inventory))
# print(get_prod_list(my_inventory))
# print(get_prod_costs(my_inventory))
# print_report(low_stock_report(my_inventory))
print_report(near_expiry_report(my_inventory))