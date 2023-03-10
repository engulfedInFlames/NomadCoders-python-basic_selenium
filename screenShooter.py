# pip install selenium
# pip install webdriver-manager: 필요한 webdriver를 설치해준다.

# driver와 browser는 다르다. driver는 binary 파일이다.
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

#### Challenge ####
#### Page를 넘기며 shoot하기####


class googleKeywordScreenshotShooter:
    def __init__(self, keyword, screenshots_dir):
        chrome_options = Options()
        chrome_options.add_argument("--headless") # 브라우저를 열지 않고 실행
        chrome_options.add_experimental_option("detach", True) # option to be kept open
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        self.keyword = keyword
        self.screenshots_dir = screenshots_dir
    def start(self):
        self.browser.get("https://google.com")
        search_bar = self.browser.find_element(By.CLASS_NAME, "gLFyf")
        search_bar.send_keys(self.keyword)
        search_bar.send_keys(Keys.ENTER)
        search_results = self.browser.find_elements(By.CLASS_NAME, "kvH3mc")
        # try:
        #     shitty_element=WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CLASS_NAME,""))) # 괄호 두 개
        #     self.browser.execute_script(
        #         """
        #         const shitty = arguments[0];
        #         shitty.parentElement.removeChild(shitty)
        #         """
        #     , shitty_element)
        # except Exception:
        #     pass

        for index, search_result in enumerate(search_results):
            search_result.screenshot(f"{self.screenshots_dir}/{self.keyword}0x{str(index).zfill(2)}.png")
    def finish(self):
        self.browser.quit()

keyword_python_scrapper = googleKeywordScreenshotShooter("python", "screenshots")
keyword_python_scrapper.start()
keyword_python_scrapper.finish()
