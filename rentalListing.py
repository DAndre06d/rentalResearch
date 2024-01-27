import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/120.0.0.0 Safari/537.36")

class RentalListing:
    def __init__(self, site: str):
        self.website = site
        self.data = self.get_data()
        self.post_data_forms(self.data)

    def get_data(self):
        response = requests.get(self.website)
        data = response.text
        soup = BeautifulSoup(data, "html.parser")
        listings = soup.find_all("div", class_="StyledPropertyCardDataWrapper")
        rentals_data = []
        for item in listings:
            link = item.find("a", class_="StyledPropertyCardDataArea-anchor").get("href")
            address = item.find("a", class_="StyledPropertyCardDataArea-anchor").getText().strip()
            price = item.find("span", class_="PropertyCardWrapper__StyledPriceLine").getText().split("/")[0]
            rentals_data.append(f"{link} + {address} + {price}")
        return rentals_data

    def post_data_forms(self, data: list):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument(f"user-agent={user_agent}")
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("accept-language=en-US,en;q=0.9")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://docs.google.com/forms/d/e/1FAIpQLSeenga5N-QY84IrgJ5Zo_aapGEt9MN5jesUSdb1furg1LIluw"
                   "/viewform")
        for list in data:
            link = list.split("+")[0]
            address = list.split("+")[1]
            price = list.split("+")[2]
            time.sleep(2)
            address_form = driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[1]/div/div/div[2]"
                                                         "/div/div[1]/div/div[1]/input")
            price_form = driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[2]/div"
                                                       "/div/div[2]/div/div[1]/div/div[1]/input")
            link_form = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div'
                                                      '[2]/div/div[1]/div/div[1]/input')
            address_form.send_keys(address)
            price_form.send_keys(price)
            link_form.send_keys(link)
            submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
            submit_button.click()
            time.sleep(2)
            submit_again = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
            submit_again.click()

