
import xlrd
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from ddt import ddt, data, unpack


def get_data(file_name):
  rows = []
  book = xlrd.open_workbook(file_name)
  # get the frist sheet
  sheet = book.sheet_by_index(0)
  for row_idx in range(1, sheet.nrows):
    rows.append(list(sheet.row_values(row_idx, 1, sheet.ncols)))
  return rows

@ddt
class ChromeSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome('../driver/chromedriver')
        self.driver.get('https://tinhte.vn/')
        self.timeout = 60
        # search_icon = self.driver.find_element_by_css_selector(".jsx-3389971726.search-icon.dark-theme-icon")
        self.driver.find_element(By.CSS_SELECTOR, '.jsx-3389971726.search-icon.dark-theme-icon').click()
        # search_icon.click()
        WebDriverWait(self.driver,self.timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.jsx-3389971726.search-textbox'))
        )
    @data(*get_data('./search.xls'))
    @unpack
    def test_search_simple(self, input_value, expected_result):
        search_text = self.driver.find_element(By.CSS_SELECTOR, '.jsx-3389971726.search-textbox')
        search_text.send_keys(input_value)
        search_text.send_keys(Keys.RETURN)
        time.sleep(2)
        search_ = self.driver.current_url
        value = "relevance" in search_
        self.assertEqual(value, expected_result)

    # def test_search_in_python_org(self):
    #     self.assertIn("Python", driver.title)
    #     elem = driver.find_element_by_name("q")
    #     elem.send_keys("getting started with python")
    #     elem.send_keys(Keys.RETURN)
    #     assert "https://www.python.org/search/?q=getting+started+with+python&submit=" == driver.current_url

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)