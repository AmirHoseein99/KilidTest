import datetime 
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

"""    
    Base Class for getting the data from the web
    Using selenium to interact with the web page, and crawling the data from it
    sleep before reading the data in order to make sure the page has been fully loaded
    we use another method to transform the data exctracted from web to pandas dataframe
    and we can use this dataframe to create our Table for DataBase
"""
class CrawlerClass :
    base_url = 'https://www.tgju.org/profile/price_dollar_rl/history'
    def get_Usd_Prices(self):
        crawled_data = []
        try:
            browser = webdriver.Chrome()
            browser.get(self.base_url)
            while(len(crawled_data) < 300):
                time.sleep(3)
                doc = browser.find_element(by=By.ID, value="table-list")
                for result in doc.text.split("\n"):
                    crawled_data.append(result.split(" "))
                time.sleep(3)
                doc = browser.find_element(by=By.CLASS_NAME, value="next")
                doc.click()
            time.sleep(1)
            browser.quit()
        except Exception as e: print(e)
        return crawled_data


    def Prices_To_Dfprices(self, price_list):
        daily_prices_df = pd.DataFrame(price_list, 
        columns =['open', 'low', 'high', 'close', "change", "change%", "Date", "shamsiDate"])
        for col in ['open', 'low', 'high', 'close'] :
            daily_prices_df[f"{col}"]= daily_prices_df[f"{col}"].apply(lambda x : int(x.replace(',', '')))
        daily_prices_df.columns = daily_prices_df.columns.str.lower()
        daily_prices_df['date'] = pd.to_datetime(daily_prices_df['date'], format="%Y/%m/%d").dt.date
        return daily_prices_df.iloc[1: , :]



