from bs4 import BeautifulSoup
from selenium import webdriver

def getStockPrice(stock_name):
    url = "https://www.google.com/search?q=" + stock_name + "+stock+price"
    print("URL: ", url)

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    browser = webdriver.Chrome(options=options) 
    browser.get(url)

    soup = BeautifulSoup(browser.page_source, 'html.parser')
    soup.prettify()
    data = soup.find('span', class_="IsqQVc NprOob wT3VGc")
    # handle when it doesn't exist
    if data is None:
        return
    else:
        return data.text

   
