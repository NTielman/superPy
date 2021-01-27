import argparse
from inventory import superpy
from current_date import current
from plot_report import plot_report
from save_report import save_report
from print_report import print_report

# Do not change these lines.
__winc_id__ = 'a2bc36ea784242e4989deb157d527ba0'
__human_name__ = 'superpy'

current_day = current.current_date.isoformat()

def handle_args(args):
    '''handles parsed args and 
    calls matching command functions'''
    command = args.command

    if command == 'buy':
        superpy.buy(product=args.product, quantity=args.quantity, exp_date=args.exp_date, cost_per_unit=args.cost, purchase_date=args.purch_date)
    elif command == 'sell':
        superpy.sell(product=args.product, quantity=args.quantity, price_per_unit=args.price, purchase_id=args.purch_id, sell_date=args.sell_date)
    elif command == 'discard':
        superpy.discard(purch_id=args.purch_id, quantity=args.quantity)
    elif command == 'plot':
        report_type = args.report
        if report_type == 'inventory':
            plot_report(superpy.get_inventory_report())
        elif report_type == 'profit':
            plot_report(superpy.get_profit_report(args.date))
    elif command == 'print':
        report_type = args.report
        if report_type == 'inventory':
            print_report(superpy.get_inventory_report())
        elif report_type == 'products':
            print_report(superpy.get_products_report())
        elif report_type == 'purchases':
            print_report(superpy.get_purchase_report(args.date))
        elif report_type == 'sales':
            print_report(superpy.get_sales_report(args.date))
        elif report_type == 'profit':
            print_report(superpy.get_profit_report(args.date))
        elif report_type == 'low-stock':
            print_report(superpy.get_low_stock_report(args.stock_amnt))
        elif report_type == 'expiry':
            print_report(superpy.get_expiry_report(current_day, args.exp_days))
        elif report_type == 'best-sell-days':
            print_report(superpy.get_bestselling_days(args.date))
        elif report_type == 'best-sell-products':
            print_report(superpy.get_bestselling_products(args.date))
    elif command == 'save':
        report_type = args.report
        if report_type == 'inventory':
            save_report(superpy.get_inventory_report(), default_date=current_day)
        elif report_type == 'products':
            save_report(superpy.get_products_report(), default_date=current_day)
        elif report_type == 'purchases':
            save_report(superpy.get_purchase_report(args.date), default_date=current_day)
        elif report_type == 'sales':
            save_report(superpy.get_sales_report(args.date), default_date=current_day)
        elif report_type == 'profit':
            save_report(superpy.get_profit_report(args.date), default_date=current_day)
        elif report_type == 'low-stock':
            save_report(superpy.get_low_stock_report(args.stock_amnt), default_date=current_day)
        elif report_type == 'expiry':
            save_report(superpy.get_expiry_report(current_day, args.exp_days), default_date=current_day)
        elif report_type == 'best-sell-days':
            save_report(superpy.get_bestselling_days(args.date), default_date=current_day)
        elif report_type == 'best-sell-products':
            save_report(superpy.get_bestselling_products(args.date), default_date=current_day)
    elif command == 'date':
        if args.reset:
            current.reset_time()
        elif args.advance:
            current.advance_time(num_of_days=args.advance)
        elif args.reverse:
            current.reverse_time(num_of_days=args.reverse)

def main():
    parser = argparse.ArgumentParser(prog='superpy', description="Track and report inventory")
    subparsers = parser.add_subparsers(dest='command')
    #make sure user provides a command
    subparsers.required = True 

    #buy command and buy arguments
    buy_parser = subparsers.add_parser('buy', help='buy and add product(s) to inventory')
    buy_parser.add_argument('--product', type=str, help='product name', required=True)
    buy_parser.add_argument('--quantity', type=float, help='product quantity', default=1)
    buy_parser.add_argument('--cost', type=float, help='cost per product', required=True)
    buy_parser.add_argument('--exp-date', type=str, dest='exp_date', help='product expiration date', required=True)
    buy_parser.add_argument('--purch-date', type=str, dest='purch_date', help='product purchase date', default=current_day)

    #sell command and sell arguments
    sale_parser = subparsers.add_parser('sell', help='sell and remove product(s) from inventory')
    sale_parser.add_argument('--product', type=str, help='product name', required=True)
    sale_parser.add_argument('--quantity', type=float, help='product quantity', default=1)
    sale_parser.add_argument('--price', type=float, help='price per product', required=True)
    sale_parser.add_argument('--purch-ID', type=str, dest='purch_id', help='product purchase ID', required=True)
    sale_parser.add_argument('--sell-date', type=str, dest='sell_date', help='product sale date', default=current_day)

    #discard command and discard arguments
    discard_parser = subparsers.add_parser('discard', help='discard and remove product(s) from inventory')
    discard_parser.add_argument('--quantity', type=float, help='product quantity', default=1)
    discard_parser.add_argument('--purch-ID', type=str, dest='purch_id', help='product purchase ID', required=True)

    #plot command and plot arguments
    plot_parser = subparsers.add_parser('plot', help='plot report data')
    plot_parser.add_argument('--report', type=str, help='report type', required=True, choices=['inventory', 'profit'])
    plot_parser.add_argument('--date', type=str, help='profit date', default='-')

    #print command and print arguments
    print_parser = subparsers.add_parser('print', help='print report data to terminal')
    print_parser.add_argument('--report', type=str, help='report type', required=True, choices=['inventory', 'products', 'purchases', 'sales', 'profit', 'low-stock', 'expiry', 'best-sell-days', 'best-sell-products'])
    print_parser.add_argument('--date', type=str, help='report date', default='-')
    print_parser.add_argument('--stock-amnt', type=int, dest='stock_amnt', help='max amount of stock', default=25)
    print_parser.add_argument('--exp-days', type=int, dest='exp_days', help='number of days till expiration date', default=7)

    #save command and save arguments
    csv_parser = subparsers.add_parser('save', help='saves report data to a csv file')
    csv_parser.add_argument('--report', type=str, help='report type', required=True, choices=['inventory', 'products', 'purchases', 'sales', 'profit', 'low-stock', 'expiry', 'best-sell-days', 'best-sell-products'])
    csv_parser.add_argument('--date', type=str, help='report date', default='-')
    csv_parser.add_argument('--stock-amnt', type=int, dest='stock_amnt', help='maxi amount of stock', default=25)
    csv_parser.add_argument('--exp-days', type=int, dest='exp_days', help='number of days till expiration date', default=7)

    #date command and date arguments
    date_parser = subparsers.add_parser('date', help='modify current inventory date')
    date_parser.add_argument('--advance', type=int, help='number of days')
    date_parser.add_argument('--reverse', type=int, help='number of days')
    date_parser.add_argument('--reset', action="store_true", help='reset date to current date')

    args = parser.parse_args()
    return handle_args(args)

if __name__ == '__main__':
    main()