from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import time
import os
import psutil
import win32.win32clipboard as win32clipboard
from io import StringIO
from board import copy_board_to_clipboard

class WhatsApp():
    def __init__(self, contact):

        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("start-maximized");
        chrome_options.add_argument("disable-infobars");
        chrome_options.add_argument("--disable-extensions");
        chrome_options.add_argument("--disable-dev-shm-usage");
        chrome_options.add_argument("--no-sandbox");
        self.wd = webdriver.WebDriver(options=chrome_options)
        self.wd.implicitly_wait(300)
        print("Navigating to chrome")
        self.wd.get("https://web.whatsapp.com/")
        print("Waiting for page to load")
        search_bar = self.wd.find_element_by_xpath(
            '//*[@id="side"]//div[contains(text(), "Search or start new chat")]/following::label//div[@contenteditable]')
        search_bar.send_keys(contact)
        self.wd.implicitly_wait(10)
        group = self.wd.find_element_by_xpath('//span[@title="%s"]' %contact)
        group.click()


    def send_text(self, text):
        text_bar = self.wd.find_element_by_xpath("//*[@id='main']//div[@contenteditable]")
        text_bar.send_keys(text + Keys.ENTER)

    def send_board(self):
        copy_board_to_clipboard()
        text_bar = self.wd.find_element_by_xpath("//*[@id='main']//div[@contenteditable]")
        text_bar.send_keys(Keys.CONTROL + 'v')
        self.wd.find_element_by_xpath("//span[@data-icon='send-light']").click()

    def read_new_text(self):
        pass

