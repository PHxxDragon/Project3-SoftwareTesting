import unittest

from parameterized import parameterized
from xlrd import open_workbook

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from ddt import ddt, data, unpack

class readDatatest:

  def dataTestComment(self):
    data_test = open_workbook('./dataTest/Data_testComment.xls')

    values = []
    for s in data_test.sheets():
      for row in range(1, s.nrows):
        col_names = s.row(0)
        col_value = []
        for name, col in zip(col_names, range(s.ncols)):
          value = (s.cell(row, col).value)
          try:
            value = str(int(value))
          except:
            pass
          col_value.append(value)
        values.append(col_value)
    return values

dataTests = readDatatest().dataTestComment()

# @ddt
class MyTestCase(unittest.TestCase):
  def setUp(self):
    print("========== [ Begin Test ] ==========")
    self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    self.driver.get('https://tinhte.vn/')
    stepComment(self.driver).login("bugbugphapha@gmail.com", "bugpha")

  def tearDown(self):
    self.driver.quit()
    # self.browser.quit()
    print("========== [ End Test ] ========== \n")

  @parameterized.expand(dataTests)
  # @unpack
  def test_comment(self, no, url, comment, desiredResult, desiredMessage):
    stepComment(self.driver).comment("https://tinhte.vn/thread/nhung-soi-cap-usb4-240w-dau-tien-da-xuat-hien-con-cho-thiet-bi-va-bo-sac-nua-thoi.3513195/", comment)
    # self.assertIn(desiredMessage, verifyLogin(self.browser).login())  

class stepComment:
  def __init__(self, driver):
    self.driver = driver

  def login(self, username, password):
    print("[Step] Login")

    self.timeout = 60
    self.driver.find_element(By.CSS_SELECTOR, 'button').click()

    link_SignIn = self.driver.find_element(By.CSS_SELECTOR, "a[href='https://tinhte.vn/login/']")
    link_SignIn.click()
    
    WebDriverWait(self.driver,self.timeout).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, '#ctrl_pageLogin_login2'))
    )

    txt_email = self.driver.find_element(By.CSS_SELECTOR, '#ctrl_pageLogin_login2')
    txt_email.send_keys(username)

    txt_passwd = self.driver.find_element(By.CSS_SELECTOR, '#ctrl_pageLogin_password2')
    txt_passwd.send_keys(password)

    txt_passwd.send_keys(Keys.RETURN)

    WebDriverWait(self.driver, self.timeout).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, "div.main-page"))
    )
  
  def comment(self, url, input_value, expected_result=""):
    print("[Step] Comment")
    self.driver.get(url)

    WebDriverWait(self.driver,self.timeout).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, "textarea"))
    )

    txt_cmt=self.driver.find_element(By.CSS_SELECTOR, "textarea")
    txt_cmt.send_keys(input_value)

    btn_reply = self.driver.find_element(By.CLASS_NAME, 'post-reply-submit')
    btn_reply.click()

    time.sleep(20)
    # cmt=self.driver.find_element(By.CSS_SELECTOR,"article[data-author='minhhoang0411']:last-child article .bbWrapper")

    # self.assertEqual(expected_result, cmt.text)

if __name__ == '__main__':
  unittest.main(verbosity=2)
