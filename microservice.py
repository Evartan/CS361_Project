# This is the microservice provided to me by teammate Masud Hussain

import requests
import pandas_datareader as pdr
from pandas_datareader._utils import RemoteDataError
import yfinance as yf
import datetime as dt
import time
import json

### Global Variables ###
ticker_name = ''
ticker_date = ''


# run_Search():
# Method that runs indefinitely that reads status.txt file and if the file contains 'run'
# then it will open stocks.txt and read the ticker name and date.
# The method will then call getStock to use the ticker name/date to retrieve price info.

def run_search():
    while True:
        time.sleep(1)
        with open('run.txt') as r:
            text = r.readline()
        if text == 'run':

            with open('send.txt') as g:
                input_json = g.readline()
            input_dict = json.loads(input_json)
            # print('---Retrieving stock info from send.txt---')

            # Open stocks.txt and read each line: 1st line = ticker_name, 2nd line = date
            global ticker_name
            global ticker_date

            ticker_name = input_dict['ticker']
            ticker_date = input_dict['date']

            # Output confirmation message
            # print('Run_Search Function - Running')
            # print('Ticker: ' + ticker_name)
            # print('Date: ' + ticker_date)

            # Run getStock method to retrieve price info
            getStock(ticker_name, ticker_date)

            # clear out the run.txt file
            with open('run.txt', 'w+') as s:
                s.write('')


# outputToFile():
    # Method that outputs data returned from getStock method to a text file named output.txt

def outputToFile(output_data):
    with open('data.txt', 'w+') as f:
        f.write(str(output_data))

# getStock():
    # Method to retrieve stock data with the stock_name and date


def getStock(stock_name, date):

    # Test Code for pdr
    # start = dt.datetime(2022, 2, 24)
    # data = pdr.get_data_yahoo('AAPL', start)
    try:
        # Data object containing price information using (ticker_name, start_date, end_date)
        data = pdr.get_data_yahoo(stock_name, date, date)

        json_data = data.to_json()

        dict = json.loads(json_data)
        new_dict = {'Ticker': ticker_name, 'Date': ticker_date}

        for key, value in dict.items():

            amount = round(list(value.values())[0], 2)

            wrap_int = f'{amount:.2f}'

            new_dict[key] = wrap_int

        # insert ticker and date key value pairs

        new_key = "Adj_close"
        old_key = "Adj Close"

        new_dict[new_key] = new_dict.pop(old_key)

        result_json = json.dumps(new_dict)

        # Call method to output data to text file
        outputToFile(result_json)

    except (RemoteDataError, KeyError) as error:
        print(error)
        outputToFile('not found')


#### TEST CODE ###
# stock_info = yf.Ticker('MSFT').info
# # stock_info.keys() for other properties you can explore
# market_price = stock_info['regularMarketPrice']
# previous_close_price = stock_info['regularMarketPreviousClose']
# print('market price ', market_price)
# print('previous close price ', previous_close_price)

### Method Call ###
if __name__ == "__main__":
    run_search()
