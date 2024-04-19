import requests;
import pygal;
import webbrowser;
import datetime;
import platform;
import unittest

def intradaily(symbol):
    return 'https://alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=' + symbol + '&interval=60min&apikey=K7HLGROEFZW2C06M'

def daily(symbol):
    return 'https://alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol + '&outputsize=full&apikey=K7HLGROEFZW2C06M'

def weekly(symbol):
    return 'https://alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=' + symbol + '&outputsize=full&apikey=K7HLGROEFZW2C06M'

def monthly(symbol):
    return 'https://alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=' + symbol + '&outputsize=full&apikey=K7HLGROEFZW2C06M'

def main():       
    while True:
        #Title Screen
        print("---------------------")
        print("Stock Data Visualizer")
        print("---------------------\n")
        #Ask the user to enter the stock symbol
        #Make sure the user actually enters an input
        while True:
            Stock_Symbol = input("Enter The Stock Symbol You Are Looking For (ex: GOOGL): ")
            if Stock_Symbol.strip():  # Check if the input is not empty after removing leading and trailing whitespaces
                break
            else:
                print("Please enter a valid stock symbol.")
        #Chart Type Screen
        print("\n-----------")
        print("Chart Types")
        print("-----------")
        print("1. Bar")
        print("2. Line\n")
        #Ask the User to enter the chart type
        #Make sure the user enters a 1 or 2
        Chart_Type = 0
        while True:
            try:
                Chart_Type = int(input("Enter The Chart Type (1 or 2): "))
                if Chart_Type in [1, 2]:
                    break
                else:
                    print("Please enter either 1 or 2.")
            except ValueError:
                print("Please enter a valid number (1 or 2).")
        #Time Series Screen
        print("\n--------------------------------------------------------")
        print("Select the Time Series of the Chart you want to Generate")
        print("--------------------------------------------------------")
        print("1. Intraday")
        print("2. Daily")
        print("3. Weekly")
        print("4. Monthly\n")
        #Ask the user to enter time series
        #Check to make sure user enters a 1, 2, 3, or 4
        while True:
            try:
                Series_Type = int(input("Enter Time Series Option(1, 2, 3, or 4): "))
                if Series_Type in [1, 2, 3, 4]:
                    break
                else:
                    print("Please enter either 1, 2, 3, or 4.")
            except ValueError:
                print("Please enter a valid number (1, 2, 3, or 4).")
        #Ask the user to enter start date
        #Check to make sure the date is entered in the proper format
        #Ask the user to enter end date
        #Check to make sure user enters a valid format end date
        start_y, start_m, start_d, end_y, end_m, end_d = "", "", "", "", "", ""
        while True:
            start_date = input("Enter the start date (YYYY-MM-DD): ")
            end_date = input("Enter the end date (YYYY-MM-DD): ")
            try:
                start_y, start_m, start_d = start_date.split('-')
                end_y, end_m, end_d = end_date.split('-')

                if (start_y, start_m, start_d) > (end_y, end_m, end_d):
                    print("Start date cannot be later than end date. Please try again.")
                else:
                    break
            except ValueError:
                print("Invalid date format. Please enter date in YYYY-MM-DD format.")
            
        data = {}
        series_format = ""
        
        if Series_Type == 1:
            url = intradaily(Stock_Symbol)
            r = requests.get(url)
            data = r.json()
            series_format = "Time Series (60min)"
        if Series_Type == 2:
            url = daily(Stock_Symbol)
            r = requests.get(url)
            data = r.json()
            series_format = "Time Series (Daily)"
        if Series_Type == 3:
            url = weekly(Stock_Symbol)
            r = requests.get(url)
            data = r.json()
            series_format = "Weekly Time Series"
        if Series_Type == 4:
            url = monthly(Stock_Symbol)
            r = requests.get(url)
            data = r.json()
            series_format = "Monthly Time Series"
        
        #defining lists to store data once the dates are filtered and sorted
        dataInRange = []
        dataSorted = []

        #moves all data entries that fall within the date range provided by user
        for x in data[series_format]:
            year, month, day = x.split('-')    
            if int(start_y) <= int(year) and int(end_y) >= int(year) and int(start_m) <= int(month) and int(end_m) >= int(month) and int(start_d) <= int(day) and int(end_d) >= int(day):
                open = data[series_format][x]['1. open']
                high = data[series_format][x]['2. high']
                low = data[series_format][x]['3. low']
                close = data[series_format][x]['4. close']
                dataInRange.append([x, open, high, low, close])

        #by default stock data is in reverse (most recent date first, earliest date last), this function goes through and puts all the stock data in chronological order
        dataLength = len(dataInRange)
        for x in range(dataLength):
            dataSorted.append(dataInRange[dataLength - x - 1])

        #defining lists for the graph values to be stored in
        dates = []
        open = []
        high = []
        low = []
        close = []

        #assigning values to the lists
        for x in dataSorted:
            dates.append(x[0])
            open.append(float(x[1]))
            high.append(float(x[2]))
            low.append(float(x[3]))
            close.append(float(x[4]))

        #making the graph
        if Chart_Type == 1:
            bar_chart = pygal.Bar()
            bar_chart.title = 'Stock Data for ' + Stock_Symbol + ': ' + start_date + ' to ' + end_date #graph title
            bar_chart.x_labels = map(str, dates) #x axis
            bar_chart.add('Open', open) #open line
            bar_chart.add('High', high) #high line
            bar_chart.add('Low', low) #low line
            bar_chart.add('Close', close) #close line
            bar_chart.render_to_file('chart.svg')
            print("bar chart made")
        if Chart_Type == 2:
            line_chart = pygal.Line()
            line_chart.title = 'Stock Data for ' + Stock_Symbol + ': ' + start_date + ' to ' + end_date #graph title
            line_chart.x_labels = map(str, dates) #x axis
            line_chart.add('Open', open) #open line
            line_chart.add('High', high) #high line
            line_chart.add('Low', low) #low line
            line_chart.add('Close', close) #close line
            line_chart.render_to_file('chart.svg')
            print("line chart made")

        if platform.system() == "Windows": #if user is using Windows it will choose this
            browser = webbrowser.get('windows-default') #default windows browser
            browser.open('chart.svg') #opening file in browser
        elif platform.system() == "macOS": #if user is using macOS it will choose this
            browser = webbrowser.get('macosx') #default macOS browser
            browser.open('chart.svg')
        else: #couldnt find one for a default linux, but i assume most linux users use firefox lol
            browser = webbrowser.get('firefox') #firefox lol
            browser.open('chart.svg')


        Continue_Stock = input("Would you like to view more stock data? Press 'y' to continue or Press 'n' to exit: ")
        if Continue_Stock.lower() == 'y':
            pass
        elif Continue_Stock.lower() == 'n':
            print("Exiting the program.")
            break
        else:
            print("Invalid input. Please enter 'y' to continue or 'n' to exit.")

main()