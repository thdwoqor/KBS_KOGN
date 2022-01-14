import os
from selenium.webdriver.chrome.options import Options

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from dotenv import load_dotenv
import time

from post.chaptcha import Chaptcha
load_dotenv()

class Write:
    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument('headless') 
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    
    def displayed(self, by, value):
        try:
            self.driver.find_element(by,value)
        except:
            return False
        return True

    def Write_Text(self,by, value, text):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((by,value)))
        post_title=self.driver.find_element(by,value)
        post_title.send_keys(f'{text}')

    def Login(self):
        self.driver.get("https://sso.kbs.co.kr/SSO2/KBSWeb/Logon.php?from_url=https%3A%2F%2Fmypage.kbs.co.kr%2F")
        self.driver.maximize_window()

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'txtUserID')))

        ID=os.environ.get("ID")
        PW=os.environ.get("PASSWORD")

        self.Write_Text(By.ID,'txtUserID',ID)
        self.Write_Text(By.ID,'txtPwd',PW)

        # https://stackoverflow.com/questions/17361742/download-image-with-selenium-python
        if self.displayed(By.ID,'chaptchID'):
            with open('filename.png', 'wb') as file:
                file.write(self.driver.find_element(By.XPATH,'//*[@id="captcha_image"]').screenshot_as_png)

            chaptcha=Chaptcha()
            num = chaptcha.chaptcha_crawling()
            self.Write_Text(By.ID,'chaptchID',num)

            self.driver.find_element(By.XPATH,'//*[@id="mainForm"]/div[1]/div[1]/div[4]/a').click()
        else:
            self.driver.find_element(By.XPATH,'//*[@id="mainForm"]/div/div[1]/div[1]/div[3]/a').click()

        try:
            WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
            self.Login()
        except:
            print("no alert")
    
    def Write_Post(self,id,title,address,contents):
        self.driver.get(f"https://pbbs.kbs.co.kr/general/write.html?bbs_id={id}&post_header=")

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'agree-new-checkbox')))

        self.driver.find_element(By.CLASS_NAME,'agree-new-checkbox').click()

        self.Write_Text(By.XPATH,'//*[@id="post_title"]',title)

        self.Write_Text(By.XPATH,'//*[@id="per_address2"]',address)

        self.Write_Text(By.XPATH,'//*[@id="post_contents"]',contents)

        input()