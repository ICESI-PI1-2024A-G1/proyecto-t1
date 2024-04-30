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

        time.sleep(7)
        verification_code = self.get_code_from_email()
        
        code_input = self.driver.find_element(By.ID,"verificationCode")
        code_btn = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div/div/div[3]/form/div[2]/button")

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

        time.sleep(7)
        verification_code = self.get_code_from_email()

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



        time.sleep(7)
        verification_code = self.get_code_from_email()

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

        
    def get_code_from_email(self):
        mail = imaplib.IMAP4_SSL('outlook.office365.com')
        mail.login('ccsa_test_user@hotmail.com', 'hola1597')
        mail.select('inbox')

        _, data = mail.search(None, 'FROM', 'ccsa101010@gmail.com')
        mail_ids = data[0].split()

        latest_mail_id = mail_ids[-1]

        _, datas = mail.fetch(latest_mail_id, "(RFC822)")
        message = email.message_from_bytes(datas[0][1])

        verification_code = None

        if message.is_multipart():
            for part in message.walk():
                content_disposition = str(part.get("Content-Disposition"))
                if "attachment" not in content_disposition:
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = message.get_payload(decode=True).decode()

            code = body.split("Su código de verificación es: ")
            verification_code = code[1][:6]
        mail.close()
        return verification_code

if __name__ == "__main__":
    unittest.main()