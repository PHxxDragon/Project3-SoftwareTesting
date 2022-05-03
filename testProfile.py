import xlrd
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
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
class PROFILE(unittest.TestCase):
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

    txt_email = self.driver.find_element(By.CSS_SELECTOR, '#ctrl_pageLogin_login2')
    txt_email.send_keys("bugbugphapha@gmail.com")

    txt_passwd = self.driver.find_element(By.CSS_SELECTOR, '#ctrl_pageLogin_password2')
    txt_passwd.send_keys("bugpha")

    txt_passwd.send_keys(Keys.RETURN)

    WebDriverWait(self.driver, self.timeout).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, "div.main-page"))
    )

  @data(*get_data('./profile/UpdateProfileSuccess.xls'))
  @unpack
  def test_update_profile_success(self, gender, address, profession, phone, idcard, homepage, avatar):
    self.driver.get('https://tinhte.vn/account/personal-details')
    WebDriverWait(self.driver, self.timeout).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, "form.personalDetailsForm"))
    )

    if gender != 'NOVALUE':
      radio_button = self.driver.find_element(By.XPATH, f"//input[@name='gender' and @value='{gender}']")
      radio_button.click()

    if address != 'NOVALUE':
      address_input = self.driver.find_element(By.XPATH, "//input[@name='location']")
      address_input.clear()
      time.sleep(0.5)
      address_input.send_keys(address)

    if profession != 'NOVALUE':
      profession_input = self.driver.find_element(By.XPATH, "//input[@name='occupation']")
      profession_input.clear()
      time.sleep(0.5)
      profession_input.send_keys(profession)

    if phone != 'NOVALUE':
      phone_input = self.driver.find_element(By.XPATH, "//input[@id='ctrl_custom_field_citizenPhoneNumber']")
      phone_input.clear()
      time.sleep(1)
      phone_input.send_keys(str(phone))

    if idcard != 'NOVALUE':
      idcard_input = self.driver.find_element(By.XPATH, "//input[@id='ctrl_custom_field_citizenId']")
      idcard_input.clear()
      time.sleep(0.5)
      idcard_input.send_keys(idcard)

    if homepage != 'NOVALUE':
      homepage_input = self.driver.find_element(By.XPATH, "//input[@name='homepage']")
      homepage_input.clear()
      time.sleep(0.5)
      homepage_input.send_keys(homepage)

    if avatar != 'NOVALUE':
      self.driver.find_element(By.XPATH, "//a[@href='account/avatar']/span").click()
      WebDriverWait(self.driver, self.timeout).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='avatar']"))
      )
      self.driver.find_element(By.XPATH, "//input[@name='avatar']").send_keys(os.getcwd() + "/profile/" + avatar)
      time.sleep(2)
      self.driver.find_element(By.XPATH, "//input[@id='ctrl_save']").click()

    time.sleep(1)

    submit_button = self.driver.find_element(By.CSS_SELECTOR, "form.personalDetailsForm input[type='submit']")
    submit_button.click()

    self.driver.get('https://tinhte.vn/account/personal-details')

    WebDriverWait(self.driver, self.timeout).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, "form.personalDetailsForm"))
    )
    time.sleep(1)

    if gender != 'NOVALUE':
      radio_button = self.driver.find_element(By.XPATH, f"//input[@name='gender' and @value='{gender}']")
      # assert radio_button.get_attribute("checked")

    if address != 'NOVALUE':
      address_input = self.driver.find_element(By.XPATH, "//input[@name='location']")
      assert address_input.get_attribute('value') == address

    if profession != 'NOVALUE':
      profession_input = self.driver.find_element(By.XPATH, "//input[@name='occupation']")
      assert profession_input.get_attribute('value') == profession

    if phone != 'NOVALUE':
      phone_input = self.driver.find_element(By.XPATH, "//input[@id='ctrl_custom_field_citizenPhoneNumber']")
      assert str(phone_input.get_attribute('value')) == str(phone)
    
    if idcard != 'NOVALUE':
      idcard_input = self.driver.find_element(By.XPATH, "//input[@id='ctrl_custom_field_citizenId']")
      assert idcard_input.get_attribute('value') == idcard

    if homepage != 'NOVALUE':
      homepage_input = self.driver.find_element(By.XPATH, "//input[@name='homepage']")
      assert homepage_input.get_attribute('value') == homepage
    
  @data(*get_data('./profile/UpdateProfileFail.xls'))
  @unpack
  def test_update_profile_fail(self, phone, homepage):
    self.driver.get('https://tinhte.vn/account/personal-details')
    WebDriverWait(self.driver, self.timeout).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, "form.personalDetailsForm"))
    )

    if phone != 'NOVALUE':
      phone_input = self.driver.find_element(By.XPATH, "//input[@id='ctrl_custom_field_citizenPhoneNumber']")
      prev_phone = phone_input.get_attribute('value')
      phone_input.clear()
      time.sleep(1)
      phone_input.send_keys(str(phone))

    if homepage != 'NOVALUE':
      homepage_input = self.driver.find_element(By.XPATH, "//input[@name='homepage']")
      prev_homepage = homepage_input.get_attribute('value')
      homepage_input.clear()
      time.sleep(0.5)
      homepage_input.send_keys(homepage)

    time.sleep(1)

    submit_button = self.driver.find_element(By.CSS_SELECTOR, "form.personalDetailsForm input[type='submit']")
    submit_button.click()

    self.driver.get('https://tinhte.vn/account/personal-details')

    WebDriverWait(self.driver, self.timeout).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, "form.personalDetailsForm"))
    )
    time.sleep(1)

    if phone != 'NOVALUE':
      phone_input = self.driver.find_element(By.XPATH, "//input[@id='ctrl_custom_field_citizenPhoneNumber']")
      assert str(phone_input.get_attribute('value')) == str(prev_phone)

    if homepage != 'NOVALUE':
      homepage_input = self.driver.find_element(By.XPATH, "//input[@name='homepage']")
      assert homepage_input.get_attribute('value') == prev_homepage

  @data(*get_data('./profile/UpdateAvatarFail.xls'))
  @unpack
  def test_update_avatar_fail(self, avatar, output):
    self.driver.get('https://tinhte.vn/account/personal-details')
    WebDriverWait(self.driver, self.timeout).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, "form.personalDetailsForm"))
    )

    if avatar != 'NOVALUE':
      self.driver.find_element(By.XPATH, "//a[@href='account/avatar']/span").click()
      WebDriverWait(self.driver, self.timeout).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='avatar']"))
      )
      self.driver.find_element(By.XPATH, "//input[@name='avatar']").send_keys(os.getcwd() + "/profile/" + avatar)
      time.sleep(1)

    assert output in self.driver.page_source


  

  def tearDown(self):
    self.driver.quit()

if __name__ == '__main__':
  unittest.main(verbosity=2)

  # 
  # 