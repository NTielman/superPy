import numpy as np
import matplotlib.pyplot as plt
from rich.console import Console
from output_styling import superpy_theme

console = Console(theme=superpy_theme)
plt.style.use('dark_background')

def create_graph(report_type, report_data):
    '''creates a line or bar chart 
    of report data'''
    headers = report_data.pop(0)
    plt.figure(num=f'{report_type}')  #title of graph
    
    if report_type == 'inventory':
        x_axis = []
        y_axis = []
        for row in report_data:
            product = row[0]
            quantity = row[1]
            x_axis.append(product)
            y_axis.append(quantity)
        plt.bar(x_axis, y_axis)
        plt.xticks(rotation=90)
        plt.ylabel('quantity')
    elif report_type == 'profit':
        x_axis = []
        cost_y_axis = []
        revenue_y_axis = []
        profit_y_axis = []

        #remove footer before adding report body to graph
        footer = report_data.pop()

        for row in report_data:
            transaction_date = row[0]
            x_axis.append(transaction_date)
            cost_y_axis.append(row[1])
            revenue_y_axis.append(row[2])
            profit_y_axis.append(row[3])
        # plot
        plt.subplot(121)
        plt.plot(x_axis, cost_y_axis, label='cost', marker='_', markersize=10)
        plt.plot(x_axis, revenue_y_axis, label='revenue', marker='+', markersize=10)
        plt.plot(x_axis, profit_y_axis, label='profit', linestyle='-.')
        plt.ylabel('amount in $')
        plt.xticks(rotation=45)
        # bar
        x = np.arange(len(x_axis)) # the position of the bars on the x-axis
        ax = plt.subplot(122)
        bar_width = 0.2
        #example: if x = 1 cost-bar will be placed at position 0.8 on x-axis
        ax.bar(x - bar_width, cost_y_axis, label='cost', width=bar_width)
        #example: if x = 1 revenue-bar will be placed at position 1
        ax.bar(x, revenue_y_axis, label='revenue', width=bar_width)
        #example: if x = 1 profit-bar will be placed at position 1.2 on x-axis
        ax.bar(x + bar_width, profit_y_axis, label='profit', width=bar_width) 
        ax.set_xticks(x)
        ax.set_xticklabels(x_axis) #set transaction dates as labels
        ax.set_ylabel('amount in $')
        plt.xticks(rotation=45)
        plt.legend()
    plt.tight_layout(pad=0.4)
    console.print(f'Plotting {report_type} report...', style='process_info')
    plt.show()

def plot_report(report):
    if report:
        report_type = report[0]
        report_data = report[1]
        create_graph(report_type, report_data)
    else:
        console.print('Failure: could not create graph of report', style='failure')
        return None