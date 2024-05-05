import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import imaplib
import email
import time
from django.test import TestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Login(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.psw = "123456789"
        self.driver.implicitly_wait(5)

    def tearDown(self):
        self.driver.quit()


    def test_login_happy_path(self):
        self.driver.get("http://127.0.0.1:8000/")
        user_input = self.driver.find_element(By.ID,"usuario")
        pass_input = self.driver.find_element(By.ID,"contrasena")
        login_btn = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div[2]/form/div[2]")




        user_input.send_keys("123456789")
        pass_input.send_keys(self.psw)
        login_btn.click()


        file = open("codes.txt")
        verification_code = file.read()

        code_input =  WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "verificationCode"))
        )    

        code_btn =  WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/div[3]/form/div[2]/button"))
        )    

        code_input.send_keys(verification_code)
        code_btn.click()

        welcome_text =  self.driver.find_element(By.XPATH, '//*[@id="navbar-collapse"]/div')
        self.assertEqual(welcome_text.text, "¡Bienvenid@,\nAccounting Admin!")

    def test_login_wrong_credentials(self):
        self.driver.get("http://127.0.0.1:8000/")
        user_input = self.driver.find_element(By.ID,"usuario")
        pass_input = self.driver.find_element(By.ID,"contrasena")
        login_btn = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div[2]/form/div[2]")

        user_input.send_keys("123456789")
        pass_input.send_keys("aaaa")
        login_btn.click()
        
        error_msg = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.ID, "toast-body"))
        )
        self.assertEqual(error_msg.text, "Por favor, revisa las credenciales.")

    def test_login_wrong_code(self):
        self.driver.get("http://127.0.0.1:8000/")
        user_input = self.driver.find_element(By.ID,"usuario")
        pass_input = self.driver.find_element(By.ID,"contrasena")
        login_btn = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div[2]/form/div[2]")

        user_input.send_keys("123456789")
        pass_input.send_keys(self.psw)
        login_btn.click()

        code_input = self.driver.find_element(By.ID,"verificationCode")
        code_btn = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div/div/div[3]/form/div[2]/button")

        code_input.send_keys("S")
        code_btn.click()

        error_msg = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.ID, "toast-body"))
        )
        self.assertEqual(error_msg.text, "Código de verificación incorrecto.")

    def test_recover_password_happy_path(self):
        self.driver.get("http://127.0.0.1:8000/")
        frg_pass_btn = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div/div/div[3]/a[2]")

        frg_pass_btn.click()

        send_btn = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div/div/div[3]/form/div[2]/button")
        id_field = self.driver.find_element(By.ID, "userId")

        id_field.send_keys("123456789")
        send_btn.click()

        file = open("codes.txt")
        verification_code = file.read()

        code_input =  WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "verificationCode"))
        )    

        code_btn =  WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/div[3]/form/div[2]/button"))
        )    

        verf_code_field = self.driver.find_element(By.ID, "verificationCode")
        enter_code_btn = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div[3]/form/div[2]/button")
        
        verf_code_field.send_keys(verification_code)
        enter_code_btn.click()

        pass_field = self.driver.find_element(By.ID, "password")
        repass_field = self.driver.find_element(By.ID, "confirmPassword")
        enter_pass_btn = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div[2]/form/div[2]/button")

        pass_field.send_keys(self.psw)
        repass_field.send_keys(self.psw)
        enter_pass_btn.click()
        self.test_login_happy_path()

    def test_recover_password_wrong_code(self):
        self.driver.get("http://127.0.0.1:8000/")
        frg_pass_btn = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div/div/div[3]/a[2]")

        frg_pass_btn.click()

        send_btn = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div/div/div[3]/form/div[2]/button")
        id_field = self.driver.find_element(By.ID, "userId")

        id_field.send_keys("123456789")
        send_btn.click()

        code_input = self.driver.find_element(By.ID,"verificationCode")
        code_btn = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div/div/div[3]/form/div[2]/button")

        code_input.send_keys("S")
        code_btn.click()

        error_msg = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.ID, "toast-body"))
        )
        self.assertEqual(error_msg.text, "Código de verificación incorrecto.")

    def test_recover_password_diff_pass(self):
        self.driver.get("http://127.0.0.1:8000/")
        frg_pass_btn = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div/div/div[3]/a[2]")

        frg_pass_btn.click()

        send_btn = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div/div/div[3]/form/div[2]/button")
        id_field = self.driver.find_element(By.ID, "userId")

        id_field.send_keys("123456789")
        send_btn.click()

        file = open("codes.txt")
        verification_code = file.read()

        code_input =  WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "verificationCode"))
        )    

        code_btn =  WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div/div[3]/form/div[2]/button"))
        )    

        verf_code_field = self.driver.find_element(By.ID, "verificationCode")
        enter_code_btn = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div[3]/form/div[2]/button")
        
        verf_code_field.send_keys(verification_code)
        enter_code_btn.click()

        pass_field = self.driver.find_element(By.ID, "password")
        repass_field = self.driver.find_element(By.ID, "confirmPassword")
        enter_pass_btn = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div[2]/form/div[2]/button")

        pass_field.send_keys(self.psw)
        repass_field.send_keys("a")
        enter_pass_btn.click()
        error_msg = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.ID, "toast-body"))
        )
        self.assertEqual(error_msg.text, "Las contraseñas no coinciden.")

if __name__ == "__main__":
    unittest.main()