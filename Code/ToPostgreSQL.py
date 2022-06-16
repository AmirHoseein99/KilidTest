import sys
sys.path.append(".")
import psycopg2
import numpy as np
import pandas as pd
from Crawler import CrawlerClass
from sqlalchemy import create_engine
from matplotlib import pyplot as plt
import matplotlib.dates as mpl_dates
from mplfinance.original_flavor import candlestick_ohlc


# global vars, change it according your Postgres and db setup
USERNAME = 'postgres'
PASSWORD = 12345678
DATABASE_NAME = 'KilidTest_db'
TABLE_NAME = 'data'

# we get the data from table by this query, you can chang it accoring to your need for data
QUERY =  f'''select date, open, high, low, close  from {TABLE_NAME} ORDER BY date DESC;'''

"""
    Class for creating the connection to database 
    we use this connection to create a table and fill it with tha dataframe we get from the 
    Crawler
    then we get the data by querry and use it to plot 
    we have a plot close prices with matplotlib 
    and we have a candlestick plot for each day

"""


class PostgresClass():
    connection_string = f'postgresql://{USERNAME}:{PASSWORD}@localhost/{DATABASE_NAME}'

    def create_Connection(self):
        db = create_engine(self.connection_string)
        conn = db.connect()
        return conn

    def create_Table(self, conn ,data):
        data.to_sql(TABLE_NAME, con=conn, if_exists='replace',
            index=False)
        conn = psycopg2.connect(self.connection_string)
        conn.autocommit = True
        cursor = conn.cursor()
        return cursor

    def query_To_Table(self, cursor, query):
        daily__data = []
        cursor.execute(query)
        for item in cursor.fetchall():
            daily__data.append(item)
        daily__data = pd.DataFrame(daily__data, 
            columns =['date','open', 'high', 'low', 'close'])

        daily__data.set_index('date', inplace=True)  
        daily__data.index = pd.to_datetime(daily__data.index) 
        return daily__data

    def get_Data(self):
        usd_Crawler = CrawlerClass()
        daily_usd_prices = usd_Crawler.Prices_To_Dfprices((usd_Crawler.get_Usd_Prices()))
        print(daily_usd_prices.head())
        return daily_usd_prices

    def plot_Closed(self, data):
        print(data.head())
        plt.plot(data.index, data["close"])
        plt.show()

    def candlestick_Plot(self, data):
            data.reset_index(inplace=True)
            print(data.head())
            ohlc = data.loc[:, ['date', 'open', 'high', 'low', 'close']]
            ohlc['date'] = pd.to_datetime(ohlc['date'])
            ohlc['date'] = ohlc['date'].apply(mpl_dates.date2num)
            ohlc = ohlc.astype(float)
            fig, ax = plt.subplots()
            candlestick_ohlc(ax, ohlc.values, width=0.6,
                 colorup='green', colordown='red', alpha=0.8)
            date_format = mpl_dates.DateFormatter("%Y/%m/%d")
            ax.xaxis.set_major_formatter(date_format)
            fig.autofmt_xdate()
            fig.tight_layout()
            plt.show()


postgres = PostgresClass()
daily_usd_price_data = postgres.get_Data()
connection = postgres.create_Connection()
cursor = postgres.create_Table(connection, daily_usd_price_data)
data_from_Table = postgres.query_To_Table(cursor, QUERY)
postgres.plot_Closed(data_from_Table)
postgres.candlestick_Plot(data_from_Table)






