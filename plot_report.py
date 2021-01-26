import matplotlib.pyplot as plt
import numpy as np
from rich.console import Console

console = Console()

plt.style.use('dark_background')

def plot_report(report):
    '''visualizes report data 
    in a line, bar or pie chart '''
    plotable_reports = ['inventory', 'profit']
    report_type = report[1]
    if not (report_type in plotable_reports):
        return f'Error: {report_type} report is not plotable'
    elif (report_type == 'profit') and (report[3] != 'all'):
        return 'Please leave date field empty'

    report_data = report[2]
    headers = report_data.pop(0)
    x_axis = []
    y_axis = []
    alt_y_axis = []
    alt_alt_y_axis = []

    plt.figure(num=f'{report_type}')
    if report_type == 'inventory':
        for row in report_data:
            product = row[0]
            quantity = row[1]
            y_axis.append(quantity)
            x_axis.append(product)
        # bar chart
        plt.subplot(121)
        plt.bar(x_axis, y_axis)
        plt.xticks(rotation=90)
        plt.ylabel('quantity')
        # pie chart
        plt.subplot(122)
        plt.pie(y_axis, labels=x_axis, autopct='%1.1f%%')
        plt.legend(bbox_to_anchor=(1, 1), loc='lower left', title='product')
    else:
        footer = report_data.pop()
        for row in report_data:
            trans_date = row[0]
            costs = row[1]
            revenue = row[2]
            profit = row[3]
            y_axis.append(costs)
            alt_y_axis.append(revenue)
            alt_alt_y_axis.append(profit)
            x_axis.append(trans_date)
        # plot
        plt.subplot(121)
        plt.plot(x_axis, y_axis, label='cost', marker='_', markersize=10)
        plt.plot(x_axis, alt_y_axis, label='revenue', marker='+', markersize=10)
        plt.plot(x_axis, alt_alt_y_axis, label='profit', linestyle='-.')
        plt.ylabel('amount in $')
        plt.xticks(rotation=45)
        # bar
        x = np.arange(len(x_axis))
        ax = plt.subplot(122)
        bar_width = 0.2  # the width of the bars
        ax.bar(x - bar_width, y_axis, label='cost', width=bar_width)
        ax.bar(x, alt_y_axis, label='revenue', width=bar_width)
        ax.bar(x + bar_width, alt_alt_y_axis, label='profit', width=bar_width)
        ax.set_xticks(x)
        ax.set_xticklabels(x_axis)
        ax.set_ylabel('amount in $')
        plt.xticks(rotation=45)
        plt.legend()
    plt.tight_layout(pad=0.4)
    console.print(f'[bold]Plotting [medium_purple3]{report_type} [/medium_purple3]report...[/bold]')
    plt.show()