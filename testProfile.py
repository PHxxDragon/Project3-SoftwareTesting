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
class PROFILE(unittest.TestCase):
  def setUp(self):
    self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    self.timeout = 60
    # self.driver.get('https://tinhte.vn/login/')
    self.driver.get('https://tinhte.vn/')

    # Đăng nhập

    self.driver.find_element(By.CSS_SELECTOR, 'button').click()

    link_SignIn = self.driver.find_element(By.CSS_SELECTOR, "a[href='https://tinhte.vn/login/']")
    link_SignIn.click()
    
    WebDriverWait(self.driver,self.timeout).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, '#ctrl_pageLogin_login2'))
    )

    txt_email = self.driver.find_element(By.CSS_SELECTOR, '#ctrl_pageLogin_login2')
    txt_email.send_keys("bugbugphapha@gmail.com")

    txt_passwd = self.driver.find_element(By.CSS_SELECTOR, '#ctrl_pageLogin_password2')
    txt_passwd.send_keys("bugpha")

    txt_passwd.send_keys(Keys.RETURN)

    

  # get test data from specified excle spreadsheet by using the get_data funcion
  @data(*get_data('./TextData.xls'))
  @unpack
  def test_text_comment(self, input_value, expected_result):
    self.driver.get('https://vn-z.vn/threads/bai-test-dau-tien-giua-i5-12400f-va-ryzen-5-5600x-i5-khoe-hon-nhung-re-hon-nhieu.44220/')

    WebDriverWait(self.driver,self.timeout).until(

      EC.presence_of_element_located((By.CSS_SELECTOR,".fr-element.fr-view p"))
    )
    txt_cmt=self.driver.find_element(By.CSS_SELECTOR,".fr-element.fr-view p")
    txt_cmt.send_keys(input_value)

    btn_reply = self.driver.find_element(By.CLASS_NAME, 'button--icon--reply')
    btn_reply.click()

    time.sleep(2)
    cmt=self.driver.find_element(By.CSS_SELECTOR,"article[data-author='minhhoang0411']:last-child article .bbWrapper")

    self.assertEqual(expected_result, cmt.text)

  def tearDown(self):
    self.driver.quit()

if __name__ == '__main__':
  unittest.main(verbosity=2)

  # 
  # 