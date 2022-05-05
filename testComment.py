from imaplib import _Authenticator
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
from selenium.webdriver.common.action_chains import ActionChains
import time
import pickle
import random
import os
from ddt import ddt, data, unpack

class readDatatest:

  def dataTestComment(self, path):
    data_test = open_workbook(path)

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

dataTests = readDatatest().dataTestComment('./dataTestComment/Data_testComment.xls')
isLogin = True
# options = webdriver.ChromeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# executor_url = driver.command_executor._url
# session_id = driver.session_id

# @ddt
class MyTestCase(unittest.TestCase):
  def setUp(self):
    print("\n========== [ Begin Test ] ==========")
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    self.driver.get('https://tinhte.vn/')

    global isLogin
    if not isLogin:
      stepComment(self.driver).login("bugbugphapha@gmail.com", "bugpha")
      pickle.dump(self.driver.get_cookies() , open("cookies.pkl","wb"))
      isLogin = True
    else:
      cookies = pickle.load(open("cookies.pkl", "rb"))
      for cookie in cookies:
        self.driver.add_cookie(cookie)


  def tearDown(self):
    self.driver.quit()
    # self.browser.quit()
    print("========== [ End Test ] ========== \n")

  @parameterized.expand(dataTests)
  # @unpack
  def test_comment(self, no, scenario, comment, picPath, desiredResult, desiredMessage):
    CMT = stepComment(self.driver)
    # CMT.commentSuccess(comment)

    if scenario in ['CMTRP13', 'CMTRP3', 'CMTRP4', 'CMTRP5', 'CMTRP10']:
      CMT.commentSuccess(comment)
    elif scenario in ['CMTRP12', 'CMTRP11']:
      CMT.commentPicture(comment, picPath)
    else:
      CMT.commentSuccess(comment)

    # self.assertIn(desiredMessage, verifyLogin(self.browser).login())

class stepComment:
  def __init__(self, driver):
    self.driver = driver
    self.timeout = 60
    self.author = 'bugpha'

  @classmethod
  def login(self, username, password):
    print("[Step] Login")

    self.driver.find_element(By.CSS_SELECTOR, 'button').click()

    link_SignIn = self.driver.find_element(By.CSS_SELECTOR, "a[href='https://tinhte.vn/login/']")
    link_SignIn.click()
    
    WebDriverWait(self.driver, self.timeout).until(
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
  
  def commentTemplate(self):
    print("[Step] Comment by " + self.author)
    self.driver.get(self.randomUrl())

    WebDriverWait(self.driver, self.timeout).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, "div.thread-view--content-wrapper"))
    )

    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") 

    time.sleep(9)
  
  def commentSuccess(self, input_value):
    self.commentTemplate()

    print("[Step] Comment text")
  
    txt_cmt=self.driver.find_element(By.XPATH, "//textarea[@class='post-reply-input']")
    self.driver.execute_script("arguments[0].scrollIntoView();", txt_cmt)
    txt_cmt.send_keys(input_value)

    # actions = ActionChains(self.driver)
    # actions.move_to_element(txt_cmt).perform()

    btn_reply = self.driver.find_element(By.XPATH, "//button[contains(@class, 'post-reply-submit')]")
    btn_reply.click()

    time.sleep(14)

    cmt = self.driver.find_element(By.CSS_SELECTOR, "div[data-author='" + self.author + "'] span")
    assert bool(cmt) == True

    time.sleep(14)
    
  def commentPicture(self, comment, path):
    self.commentTemplate()

    print("[Step] Comment picture")

    # txt_cmt=self.driver.find_element(By.XPATH, "//textarea[@class='post-reply-input']")
    # self.driver.execute_script("arguments[0].scrollIntoView();", txt_cmt)
    txt_cmt=self.driver.find_element(By.XPATH, "//textarea[@class='post-reply-input']")
    self.driver.execute_script("arguments[0].scrollIntoView();", txt_cmt)
    txt_cmt.send_keys(comment)

    time.sleep(5)

    fileInput = self.driver.find_element(By.XPATH, "//input[@type='file']")
    fileInput.send_keys(os.getcwd() + path)

    btn_reply = self.driver.find_element(By.XPATH, "//button[contains(@class, 'post-reply-submit')]")
    btn_reply.click()

    time.sleep(5)

    cmt = self.driver.find_element(By.CSS_SELECTOR, "div[data-author='" + self.author + "'] span")

    assert bool(cmt) == True

    time.sleep(9)

  def randomUrl(self):
    print("[Step] Random thread")
    threadComponent = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'thread-containers')]/ol/li/div/article/*[1][name()='a']")
    
    # links = [thread.get_attribute('href') for thread in threadComponent]
    selectedThread = random.choice(threadComponent)
    self.driver.execute_script("arguments[0].scrollIntoView();", selectedThread)

    return selectedThread.get_attribute('href')

if __name__ == '__main__':
  unittest.main(verbosity=2)
