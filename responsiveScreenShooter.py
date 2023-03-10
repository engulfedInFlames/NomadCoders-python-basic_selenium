from urllib.parse import urlparse
from time import sleep
from math import ceil
import os, re
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class responsiveScreenShooter:
    def __init__(self, urls):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("start-maximized")
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        self.urls = urls
        self.sizes = [480, 960, 1024, 1366, 1920]
    def shoot(self, url, dir):
           self.browser.get(url)
           BROWSER_MAX_HEIGHT = self.browser.execute_script("return window.outerHeight") #Not $ browser.get_window_size()['height']
           for size in self.sizes:
            self.browser.execute_script("window.scrollTo(0,0)")
            self.browser.set_window_size(size, BROWSER_MAX_HEIGHT)
            scroll_height = self.browser.execute_script("return document.body.scrollHeight")
            sleep(5)
            sections = ceil(scroll_height / BROWSER_MAX_HEIGHT)
            for section in range(sections):
                self.browser.execute_script(f"window.scrollTo(0, {section * BROWSER_MAX_HEIGHT})")
                self.browser.save_screenshot(f"screenshots/{dir}/{size}x{section}.png")
                sleep(0.5)
    def start(self):
        for url in self.urls:
            parsed = urlparse(url).netloc.replace("www", "")
            dir = re.sub(r"\.\w","",parsed)
            check_path = os.path.isdir(f"./screenshots/{dir}")
            if not check_path:
                os.mkdir(f"./screenshots/{dir}")
            else:
                pass
            self.shoot(url, dir)
        self.browser.quit()
    
        
    
        

nomadcoder_screen_shooter = responsiveScreenShooter(["https://www.nomadcoders.co/", "https://brownbears.tistory.com/506"])
nomadcoder_screen_shooter.start()