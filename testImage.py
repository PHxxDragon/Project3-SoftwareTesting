import xlrd
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
   # print(get_data('./TextData.xls'))
@ddt
class COMMENT(unittest.TestCase):
   def setUp(self):
      self.driver = webdriver.Chrome(executable_path=".././driver/chromedriver.exe")
      self.timeout = 60
      self.driver.get('https://vn-z.vn')

      # Đăng nhập 

      link_SignIn = self.driver.find_element(By.CSS_SELECTOR, "a[href='/login/']")
      link_SignIn.click() 

      WebDriverWait(self.driver,self.timeout).until(

         EC.presence_of_element_located((By.NAME,'login'))
      )

      txt_email = self.driver.find_element(By.NAME,'login')
      txt_email.send_keys("minhhoang0411")

      txt_passwd = self.driver.find_element(By.NAME,'password')
      txt_passwd.send_keys("20062000")

      btn_login = self.driver.find_element(By.CLASS_NAME, 'button--icon--login')
      btn_login.click()

  # get test data from specified excle spreadsheet by using the get_data funcion
   @data(*get_data('./ImageData.xls'))
   @unpack
   def test_text_comment(self, input_value, expected_result):
      self.driver.get('https://vn-z.vn/threads/eternals-2021-phim-hay-nhat-hoac-do-te-nhat-trong-lich-su-marvel.44167/')

      WebDriverWait(self.driver,self.timeout).until(

         EC.presence_of_element_located((By.CSS_SELECTOR,".fr-element.fr-view p"))
      )

      btn_insert=self.driver.find_element(By.ID,'insertImage-1')
      btn_insert.click()

      WebDriverWait(self.driver,self.timeout).until(

         EC.presence_of_element_located((By.ID,'imageByURL-1'))
      )

      btn_url=self.driver.find_element(By.ID,'imageByURL-1')
      btn_url.click()

      input_url=self.driver.find_element(By.ID,'fr-image-by-url-layer-text-1')
      input_url.send_keys(input_value)

      btn_chen=self.driver.find_element(By.CSS_SELECTOR,"button[data-cmd='imageInsertByURL']")
      btn_chen.click()
         
      time.sleep(3)

      btn_reply = self.driver.find_element(By.CLASS_NAME, 'button--icon--reply')
      btn_reply.click()

      time.sleep(2)
         
      cmt=self.driver.find_element(By.CSS_SELECTOR,"article[data-author='minhhoang0411']:last-child article .bbWrapper")
      check=True
      try:
         checkImage=cmt.find_element(By.CSS_SELECTOR,"img")
      except:
         check=False
      assert check==True

   def tearDown(self):
      self.driver.quit()

if __name__ == '__main__':
  unittest.main(verbosity=2)