from datetime import date, timedelta, datetime
from create_directory import create_directory
import csv
import os

'''upon buying, selling, discarding or changing inventory, mester update root-inventory file tmb mesora. otherwise the changes won't hold, prob is that on __init__ i can't use
the buy() func cause it will add the already existing inventory to the inventory. whivch is not the bedoeling. purchases.csv, sales.csv get updated with every buy/ sell trans
inventory reflects current inventory inventory report ta reflect inventory di specific date.of den init if product tin purchase - id kaba, buy function shouldn 't buy/ add it to inventory again.'''

class Supermarket():
    purchases = {}
    sales = {}
    expiry_dates = {}
    inventory = {}

    def __init__(self):
        '''please ensure to place your initial inventory
        in the root_files directory 
        please ensure to name the initial inventory "root_inventory.csv" '''
        #find root folder path
        dir_path = create_directory('root_files')
        file_name = 'root_inventory.csv'
        file_path = os.path.join(dir_path, file_name)

        # if "root_inventory.csv" exists in current directory
        if os.path.isfile(file_path):
            with open(file_path, newline='') as csvfile:
                reader = csv.reader(csvfile)
                # skip header
                next(reader)

                for row in reader:
                    product = row[0]
                    quantity = float(row[1])
                    cost_per_unit = float(row[2])
                    exp_date = row[3]
                    purchase_date = row[4]
                    self.buy(product, quantity, cost_per_unit,
                             exp_date, purchase_date)

    def discard(self, product, exp_date, quantity=1):
        '''removes item(s) from inventory (bijv, if item is: defect, expired)
        and adds to loss records'''
        if quantity >= self.inventory[product]:
            del self.inventory[product]
        else:
            self.inventory[product] -= quantity
        # remove items from expiry dates
        if quantity >= self.expiry_dates[exp_date][product]:
            del self.expiry_dates[exp_date][product]
        else:
            self.expiry_dates[exp_date][product] -= quantity

    def buy(self, product, quantity, cost_per_unit, exp_date, purchase_date):
        '''adds a product to inventory and
        adds product info to purchase records'''
        if product in self.inventory:
            self.inventory[product] += quantity
        else:
            # add product to inventory
            self.inventory[product] = quantity
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
        return f'items added to inventory. Transaction ID: {transaction_id}'

    def sell(self, product, quantity, price_per_unit, purchase_id, sell_date):
        '''removes a product from inventory and
        adds product info to sales records'''
        if not (product in self.inventory):
            return f"product: {product} not in stock"
        if quantity > self.inventory[product]:
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
        self.inventory[product] -= quantity
        # remove products and prod quantities from expiry date
        if quantity >= self.expiry_dates[exp_date][product]:
            del self.expiry_dates[exp_date][product]
        else:
            self.expiry_dates[exp_date][product] -= quantity
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
        products_left = self.inventory[product]
        if products_left == 0:
            del self.inventory[product]
        elif products_left <= 5:
            self.warn("low_stock")

    def warn(self, message):
        #set timeout function 2/ 3 seconds so iot prints warning after report?
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
        csv_report = [['Product Name', 'Amount In Stock']]
        terminal_report = [f'{"Product Name":<20}| Amount In Stock']
        for product in self.inventory:
            quantity = self.inventory[product]
            terminal_report.append(
                f'{product:<20}| {quantity}')
            csv_report.append([product, quantity])
        return [terminal_report, 'inventory', csv_report]

    def get_products_report(self):
        '''returns a list of all products the supermarket offers'''
        terminal_report = []
        csv_report = []
        for product in self.inventory:
            terminal_report.append(f'{product}')
            csv_report.append([product])
        return [terminal_report, 'products', csv_report]

#date (2021-01-13) if len date == 10 print report for specific day
#date (2021-01) if len date == 7 print report for every day in specific month
##date (2021) if len date == 4 print report for every (month) in specific year


    def get_purchase_report(self, purchase_date='all'):
        '''returns all purchase transactions 
        or all purchases made on a specific date'''
        terminal_report = [
            f'{"Date":<11}| {"Product":<10}| {"Amnt":<8}| {"Unit Cost":<10}| {"Total":<8}| {"Exp Date":<11}| Transaction ID']
        csv_report = [['Date', 'Product', 'Amnt', 'Unit Cost',
                       'Total', 'Exp Date', 'Transaction ID']]
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
                    terminal_report.append(
                        f'{date:<11}| {product:<10}| {quantity:<8}| {unit_cost:<10}| {total_spent:<8}| {expiry_date:<11}| {trans_id}')
                    csv_report.append(
                        [date, product, quantity, unit_cost, total_spent, expiry_date, trans_id])
        elif purchase_date in self.purchases:
            for purchase_num in range(len(self.purchases[purchase_date])):
                product = self.purchases[purchase_date][purchase_num]["product"]
                quantity = self.purchases[purchase_date][purchase_num]["quantity"]
                unit_cost = self.purchases[purchase_date][purchase_num]["unit_cost"]
                total_spent = self.purchases[purchase_date][purchase_num]["total_cost"]
                expiry_date = self.purchases[purchase_date][purchase_num]["expiry_date"]
                trans_id = self.purchases[purchase_date][purchase_num]["id"]
                total_cost += total_spent
                terminal_report.append(
                    f'{purchase_date:<11}| {product:<10}| {quantity:<8}| {unit_cost:<10}| {total_spent:<10}| {expiry_date:<10}| {trans_id}')
                csv_report.append(
                    [purchase_date, product, quantity, unit_cost, total_spent, expiry_date, trans_id])
        else:
            terminal_report.append(
                f'No purchase records found for date: {purchase_date}')
            csv_report.append(
                [f'No purchase records found for date: {purchase_date}'])
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
        elif sell_date in self.sales:
            for sale_num in range(len(self.sales[sell_date])):
                product = self.sales[sell_date][sale_num]["product"]
                quantity = self.sales[sell_date][sale_num]["quantity"]
                unit_price = self.sales[sell_date][sale_num]["unit_price"]
                total_income = self.sales[sell_date][sale_num]["total_income"]
                trans_id = self.sales[sell_date][sale_num]["id"]
                total_revenue += total_income
                terminal_report.append(
                    f'{sell_date:<11}| {product:<15}| {quantity:<10}| {unit_price:<13}| {total_income:<10}| {trans_id}')
                csv_report.append(
                    [sell_date, product, quantity, unit_price, total_income, trans_id])
        else:
            terminal_report.append(
                f'No sale records found for date: {sell_date}')
            csv_report.append([f'No sale records found for date: {sell_date}'])
        terminal_report.append(f'Total Revenue: ${round(total_revenue, 2)}')
        csv_report.append([f'Total Revenue: ${round(total_revenue, 2)}'])
        return [terminal_report, 'sales', csv_report, sell_date]

    def get_profit_report(self, profit_date='all'):
        '''returns total profit made over time 
        or profit made on a specific date'''
        terminal_report = []
        csv_report = []
        total_profit = 0
        if profit_date == 'all':
            terminal_report.append(
                f'{"Date":<11}| {"Total Cost":<15}| {"Total Revenue":<15}| Total Profit')
            csv_report.append(
                ['Date', 'Total Cost', 'Total Revenue', 'Total Profit'])
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
                terminal_report.append(
                    f'{date:<11}| {day_cost:<15}| {day_revenue:<15}| {day_profit}')
                csv_report.append([date, day_cost, day_revenue, day_profit])
        elif profit_date in self.sales:
            terminal_report.append(
                f'{"Date":<11}| {"Amnt x Product":<20}| {"Total Cost":<15}| {"Total Revenue":<15}| Total Profit')
            csv_report.append(
                ['Date', 'Amnt x Product', 'Total Cost', 'Total Revenue', 'Total Profit'])
            for sale_num in range(len(self.sales[profit_date])):
                product = self.sales[profit_date][sale_num]["product"]
                quantity = self.sales[profit_date][sale_num]["quantity"]
                unit_cost = self.sales[profit_date][sale_num]["unit_cost"]
                product_cost = unit_cost * quantity
                product_revenue = self.sales[profit_date][sale_num]["total_income"]
                product_profit = product_revenue - product_cost
                total_profit += product_profit
                terminal_report.append(
                    f'{profit_date:<11}| {str(quantity) + " x " + product:<20}| {product_cost:<15}| {product_revenue:<15}| {product_profit}')
                csv_report.append(
                    [profit_date, f'{quantity} x {product}', product_cost, product_revenue, product_profit])
        else:
            terminal_report.append(
                f'No sale records found for date: {profit_date}')
            csv_report.append(
                [f'No sale records found for date: {profit_date}'])
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
        if expired_items > 0:
            self.warn("expired_items")
        return [terminal_report, 'expiry', csv_report]

    def get_bestselling_days(self, year=False, month=False):
        '''returns days with most sales transactions (most products sold) of all times
        or days with most sales transactions of a specific month and year '''
        #change month/ year to date='all'. if date == (yyyy-mm) best day of month report, if date == (yyyy) best day of year report
        #if date (yyyy-mm-dd) print cannot get bestselling day for specific date only for month or year or all time
        terminal_report = []
        csv_report = []
        num_of_sales = 0
        if (not year) and (not month):
            # return bestselling days of all time
            # find the highest num of daily sales
            for sales_date in self.sales:
                day_sales = len(self.sales[sales_date])
                if day_sales > num_of_sales:
                    num_of_sales = day_sales
            # find dates with this number of sales
            for sales_date in self.sales:
                if len(self.sales[sales_date]) == num_of_sales:
                    terminal_report.append(sales_date)
                    csv_report.append([sales_date])
        elif year and month:
            # return bestselling days of specific year and month
            for sales_date in self.sales:
                if f'{year}-{month}' in sales_date:
                    day_sales = len(self.sales[sales_date])
                    if day_sales > num_of_sales:
                        num_of_sales = day_sales
            for sales_date in self.sales:
                if f'{year}-{month}' in sales_date:
                    if len(self.sales[sales_date]) == num_of_sales:
                        terminal_report.append(sales_date)
                        csv_report.append([sales_date])
        elif year or month:
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
                        terminal_report.append(sales_date)
                        csv_report.append([sales_date])
        terminal_report.append(
            f'Total transactions made per day: {num_of_sales}')
        csv_report.append([f'Total transactions made per day: {num_of_sales}'])
        if month:
            month_num = int(month)
            month = date(1900, month_num, 1).strftime('%B')
        #change returned val di year month. {false}{false}
        return [terminal_report, 'best-selling days', csv_report, f'{year}{month}']

    def get_bestselling_products(self, year=False, month=False):
        '''returns the best selling products of all times
        or best selling products of a specific month and year '''
         #change month/ year to date='all'. if date (yyyy-mm-dd) best prod(s) of day
         # if date == (yyyy-mm) best products of month, if date == (yyyy) best prod of year
        terminal_report = []
        csv_report = []
        num_of_sales = 0
        products_sold = {}
        if (not year) and (not month):
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
        elif year and month:
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
        elif year or month:
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
                terminal_report.append(product)
                csv_report.append([product])
        terminal_report.append(
            f'Total amount of product(s) sold: {num_of_sales}')
        csv_report.append([f'Total amount of product(s) sold: {num_of_sales}'])
        if month:
            month_num = int(month)
            month = date(1900, month_num, 1).strftime('%B')
            #change returned val di year month. {false}{false}
        return [terminal_report, 'best-selling products', csv_report, f'{year}{month}']

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