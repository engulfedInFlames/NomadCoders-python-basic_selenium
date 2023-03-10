import csv
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



class hashtagminer:
    def __init__(self, USER_ID, keyword):
        chrome_options = Options()
        # chrome_options = Options.add_argument("--headless")
        chrome_options.add_experimental_option("detach", True)
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        self.USER_ID = USER_ID
        self.keyword = keyword
        self.collected_hashtags = []
        self.browser.get("https://www.instagram.com/")
    def login(self):
        username_input = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"[aria-label='Phone number, username, or email']")))
        password_input = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"[aria-label='Password']")))
        login_btn = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME,"_aijb")))
        webdriver.ActionChains(self.browser).send_keys_to_element(username_input, self.USER_ID).send_keys_to_element(password_input, input("What is your password?")).move_to_element(login_btn).click().perform()
        saveinfo_pop = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME,"_aa55")))
        if saveinfo_pop:
            not_now_btn1 = self.browser.find_element(By.CLASS_NAME, "_acao")
            webdriver.ActionChains(self.browser).move_to_element(not_now_btn1).click().perform()
        notification_pop = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME,"x7r02ix")))
        if notification_pop:
            not_now_btn2 = self.browser.find_element(By.CLASS_NAME, "_a9_1")
            webdriver.ActionChains(self.browser).move_to_element(not_now_btn2).click().perform()
    def search_and_scrap(self):
        self.browser.maximize_window()
        search_btn = self.browser.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[2]/div/a")
        webdriver.ActionChains(self.browser).move_to_element(search_btn).click().perform()
        search_input = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"[aria-label='Search input']")))
        search_input.send_keys(f"#{self.keyword}")
        sleep(3)
        search_results_container = self.browser.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div[2]/div")
        search_results = search_results_container.find_elements(By.CSS_SELECTOR, "[role='link']")
        for search_result in search_results:
            data = search_result.text.split()
            if data and data[0].startswith("#"):
                hashtag = data[0][1:]
                number_of_posts = data[1]
                self.collected_hashtags.append((hashtag, number_of_posts))
    def sort(self):
        self.collected_hashtags.sort(key=lambda x:x[1], reverse=True)
    def save_as_csv(self):
        csvfile = open(f"{self.keyword}-report.csv", "w")
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Hashtag","Number of posts"])
        for item in self.collected_hashtags:
            csvwriter.writerow(item)
    def start(self):
        self.login()
        self.search_and_scrap()
        self.sort()
        self.save_as_csv()
        self.browser.quit()
    
hashtagminer("recona97", "python").start()
        

