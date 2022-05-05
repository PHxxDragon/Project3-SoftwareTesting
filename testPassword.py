import xlrd
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import os
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
class PASSWORD(unittest.TestCase):
  def setUp(self):
    self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    self.timeout = 10
    # self.driver.get('https://tinhte.vn/login/')
    self.driver.get('https://tinhte.vn/')

    # Đăng nhập

    self.driver.find_element(By.CSS_SELECTOR, 'button').click()

    link_SignIn = self.driver.find_element(By.CSS_SELECTOR, "a[href='https://tinhte.vn/login/']")
    link_SignIn.click()
    
    WebDriverWait(self.driver,self.timeout).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, '#ctrl_pageLogin_login2'))
    )


  @data(*get_data('./profile/UpdatePassword.xls'))
  @unpack
  def test_update_password(self, account, password, currentPassword, newPassword, confirmPassword, expect):
    # login
    txt_email = self.driver.find_element(By.CSS_SELECTOR, '#ctrl_pageLogin_login2')
    txt_email.send_keys(account)

    txt_passwd = self.driver.find_element(By.CSS_SELECTOR, '#ctrl_pageLogin_password2')
    txt_passwd.send_keys(password)

    txt_passwd.send_keys(Keys.RETURN)
    WebDriverWait(self.driver, self.timeout).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, "div.main-page"))
    )

    # test
    self.driver.get('https://tinhte.vn/account/security')
    WebDriverWait(self.driver, self.timeout).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, "form.ContactDetailsForm"))
    )

    curr_field = self.driver.find_element(By.XPATH, f"//input[@name='old_password']")
    curr_field.clear()
    curr_field.send_keys(currentPassword)
    
    pass_field = self.driver.find_element(By.XPATH, f"//input[@name='password']")
    pass_field.clear()
    pass_field.send_keys(newPassword)
    
    conf_field = self.driver.find_element(By.XPATH, f"//input[@name='password_confirm']")
    conf_field.clear()
    conf_field.send_keys(confirmPassword)

    submit_button = self.driver.find_element(By.CSS_SELECTOR, "form.ContactDetailsForm input[type='submit']")
    time.sleep(0.5)
    submit_button.click()

    if (expect == 'OK'):
      WebDriverWait(self.driver, self.timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "form.ContactDetailsForm"))
      )
      # log out
      logout_button = self.driver.find_element(By.CSS_SELECTOR, "a.LogOut")
      time.sleep(0.5)
      self.driver.get(logout_button.get_attribute('href'))
      WebDriverWait(self.driver, self.timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.main-page"))
      )

      # find login page
      self.driver.get('https://tinhte.vn/login/')
      
      WebDriverWait(self.driver,self.timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#ctrl_pageLogin_login2'))
      )

      # log in again with new password
      txt_email = self.driver.find_element(By.CSS_SELECTOR, '#ctrl_pageLogin_login2')
      txt_email.send_keys(account)

      txt_passwd = self.driver.find_element(By.CSS_SELECTOR, '#ctrl_pageLogin_password2')
      txt_passwd.send_keys(newPassword)

      txt_passwd.send_keys(Keys.RETURN)
      self.driver.implicitly_wait(10)

      try:
        WebDriverWait(self.driver, 2).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, "div.main-page"))
        )
      except TimeoutException:
        assert False

    else:
      WebDriverWait(self.driver, self.timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.errorOverlay"))
      )
      errorCode = self.driver.find_element(By.XPATH, "//label[@class='OverlayCloser']")
      print(errorCode.get_attribute('innerHTML'))
      assert expect in str(errorCode.get_attribute('innerHTML'))

  

  def tearDown(self):
    self.driver.quit()

if __name__ == '__main__':
  unittest.main(verbosity=2)

  # 
  # 