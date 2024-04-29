import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import imaplib
import email
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Login(unittest.TestCase):
    def setUp(self):
        self.psw = "123456789"
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)

    def tearDown(self):
        self.driver.quit()

    def test_register_happy_path(self):
        self.driver.get("http://127.0.0.1:8000/")
        register_btn = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div/div/div[3]/a[1]")
        register_btn.click()
        user = "111111"
        name_field = self.driver.find_element(By.ID, "nombre")
        surname_field = self.driver.find_element(By.ID, "apellido")
        id_field = self.driver.find_element(By.ID, "cedula")
        email_field = self.driver.find_element(By.ID, "correo")
        pass_field = self.driver.find_element(By.ID, "contrasena")
        con_pass_field = self.driver.find_element(By.ID, "confirmar_contrasena")


        name_field.send_keys(user)
        surname_field.send_keys(user)
        id_field
  

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