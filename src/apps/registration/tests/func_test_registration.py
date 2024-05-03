import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import imaplib
import email
import random
import time
from utils.models import CustomUser
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Registration(unittest.TestCase):
    def setUp(self):
        self.user = "111111"
        self.userName = ""
        self.email = 'cssa_register_user@hotmail.com'
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)

    def tearDown(self):
        nombre_usuario = self.userName
        if CustomUser.objects.filter(username=nombre_usuario).exists():
            usuario_a_eliminar = CustomUser.objects.get(username=nombre_usuario)
            usuario_a_eliminar.delete()
        self.driver.quit()

    def test_register_happy_path(self):

        psw = "11111111"
        self.driver.get("http://127.0.0.1:8000/")
        register_btn = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div/div/div[3]/a[1]")
        register_btn.click()
        name_field = self.driver.find_element(By.ID, "nombre")
        surname_field = self.driver.find_element(By.ID, "apellido")
        id_field = self.driver.find_element(By.ID, "cedula")
        email_field = self.driver.find_element(By.ID, "correo")
        pass_field = self.driver.find_element(By.ID, "contrasena")
        con_pass_field = self.driver.find_element(By.ID, "confirmar_contrasena")
        rgstr_btn = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div[2]/form/div[5]/button")
        name_field.send_keys(self.user)
        surname_field.send_keys(self.user)
        self.userName = self.generar_numero_aleatorio()
        id_field.send_keys(self.userName)
        email_field.send_keys(self.email)
        pass_field.send_keys(psw)
        con_pass_field.send_keys(psw)
        rgstr_btn.click()

        time.sleep(5)
        verification_code = self.get_code_from_email()
        
        code_input = self.driver.find_element(By.ID,"verificationCode")
        code_btn = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div/div/div[3]/form/div[2]/button")

        code_input.send_keys(verification_code)
        code_btn.click()
        success_msg = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.ID, "toast-body"))
        )
        self.assertEqual(success_msg.text, "Usuario registrado correctamente.")

    def test_register_repeated_username(self):

        psw = "11111111"
        self.driver.get("http://127.0.0.1:8000/")
        register_btn = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div/div/div[3]/a[1]")
        register_btn.click()
        name_field = self.driver.find_element(By.ID, "nombre")
        surname_field = self.driver.find_element(By.ID, "apellido")
        id_field = self.driver.find_element(By.ID, "cedula")
        email_field = self.driver.find_element(By.ID, "correo")
        pass_field = self.driver.find_element(By.ID, "contrasena")
        con_pass_field = self.driver.find_element(By.ID, "confirmar_contrasena")
        rgstr_btn = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div[2]/form/div[5]/button")

        name_field.send_keys(self.user)
        surname_field.send_keys(self.user)
        id_field.send_keys("123456789")
        email_field.send_keys(self.email)
        pass_field.send_keys(psw)
        con_pass_field.send_keys(psw)
        rgstr_btn.click()

        error_msg = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.ID, "toast-body"))
        )
        self.assertEqual(error_msg.text, "El usuario ya está registrado.")

    def test_register_invalid_username(self):
        psw = "999999"
        self.driver.get("http://127.0.0.1:8000/")
        register_btn = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div/div/div[3]/a[1]")
        register_btn.click()
        name_field = self.driver.find_element(By.ID, "nombre")
        surname_field = self.driver.find_element(By.ID, "apellido")
        id_field = self.driver.find_element(By.ID, "cedula")
        email_field = self.driver.find_element(By.ID, "correo")
        pass_field = self.driver.find_element(By.ID, "contrasena")
        con_pass_field = self.driver.find_element(By.ID, "confirmar_contrasena")
        rgstr_btn = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div[2]/form/div[5]/button")

        name_field.send_keys(self.user)
        surname_field.send_keys(self.user)
        id_field.send_keys("999999")
        email_field.send_keys(self.email)
        pass_field.send_keys(psw)
        con_pass_field.send_keys(psw)
        rgstr_btn.click()

        error_msg = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.ID, "toast-body"))
        )
        self.assertEqual(error_msg.text, "La cédula ingresada no es válida.")

    def test_register_invalid_username2(self):
        psw = "999999"
        self.driver.get("http://127.0.0.1:8000/")
        register_btn = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div/div/div[3]/a[1]")
        register_btn.click()
        name_field = self.driver.find_element(By.ID, "nombre")
        surname_field = self.driver.find_element(By.ID, "apellido")
        id_field = self.driver.find_element(By.ID, "cedula")
        email_field = self.driver.find_element(By.ID, "correo")
        pass_field = self.driver.find_element(By.ID, "contrasena")
        con_pass_field = self.driver.find_element(By.ID, "confirmar_contrasena")
        rgstr_btn = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div[2]/form/div[5]/button")

        name_field.send_keys(self.user)
        surname_field.send_keys(self.user)
        id_field.send_keys("1000000000000")
        email_field.send_keys(self.email)
        pass_field.send_keys(psw)
        con_pass_field.send_keys(psw)
        rgstr_btn.click()

        error_msg = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.ID, "toast-body"))
        )
        self.assertEqual(error_msg.text, "La cédula ingresada no es válida.")

    def test_register_invalid_mail(self):

        psw = "11111111"
        self.driver.get("http://127.0.0.1:8000/")
        register_btn = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div/div/div[3]/a[1]")
        register_btn.click()
        name_field = self.driver.find_element(By.ID, "nombre")
        surname_field = self.driver.find_element(By.ID, "apellido")
        id_field = self.driver.find_element(By.ID, "cedula")
        email_field = self.driver.find_element(By.ID, "correo")
        pass_field = self.driver.find_element(By.ID, "contrasena")
        con_pass_field = self.driver.find_element(By.ID, "confirmar_contrasena")
        rgstr_btn = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div[2]/form/div[5]/button")

        name_field.send_keys(self.user)
        surname_field.send_keys(self.user)
        self.userName = self.generar_numero_aleatorio()
        id_field.send_keys(self.userName)
        email_field.send_keys("correo_falso.com")
        pass_field.send_keys(psw)
        con_pass_field.send_keys(psw)
        rgstr_btn.click()

        error_msg = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.ID, "toast-body"))
        )
        self.assertEqual(error_msg.text, "Por favor, ingrese un correo válido.")

    def test_register_invalid_password(self):

        psw = "1111111"
        self.driver.get("http://127.0.0.1:8000/")
        register_btn = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div/div/div[3]/a[1]")
        register_btn.click()
        name_field = self.driver.find_element(By.ID, "nombre")
        surname_field = self.driver.find_element(By.ID, "apellido")
        id_field = self.driver.find_element(By.ID, "cedula")
        email_field = self.driver.find_element(By.ID, "correo")
        pass_field = self.driver.find_element(By.ID, "contrasena")
        con_pass_field = self.driver.find_element(By.ID, "confirmar_contrasena")
        rgstr_btn = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div[2]/form/div[5]/button")

        name_field.send_keys(self.user)
        surname_field.send_keys(self.user)
        self.userName = self.generar_numero_aleatorio()
        id_field.send_keys(self.userName)
        email_field.send_keys(self.email)
        pass_field.send_keys(psw)
        con_pass_field.send_keys(psw)
        rgstr_btn.click()

        error_msg = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.ID, "toast-body"))
        )
        self.assertEqual(error_msg.text, "La contraseña debe tener al menos 8 caracteres.")

    def test_register_diff_password(self):

        psw = "11111111"
        psw2= "11111112"
        self.driver.get("http://127.0.0.1:8000/")
        register_btn = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div/div/div[3]/a[1]")
        register_btn.click()
        name_field = self.driver.find_element(By.ID, "nombre")
        surname_field = self.driver.find_element(By.ID, "apellido")
        id_field = self.driver.find_element(By.ID, "cedula")
        email_field = self.driver.find_element(By.ID, "correo")
        pass_field = self.driver.find_element(By.ID, "contrasena")
        con_pass_field = self.driver.find_element(By.ID, "confirmar_contrasena")
        rgstr_btn = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div[2]/form/div[5]/button")

        name_field.send_keys(self.user)
        surname_field.send_keys(self.user)
        self.userName = self.generar_numero_aleatorio()
        id_field.send_keys(self.userName)
        email_field.send_keys(self.email)
        pass_field.send_keys(psw)
        con_pass_field.send_keys(psw2)
        rgstr_btn.click()

        error_msg = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.ID, "toast-body"))
        )
        self.assertEqual(error_msg.text, "Las contraseñas no coinciden.")
  

    def get_code_from_email(self):
        mail = imaplib.IMAP4_SSL('outlook.office365.com')
        mail.login(self.email, 'hola1597!')
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
    
    def generar_numero_aleatorio(self):
        numero = random.randint(1000001, 999999999999)
        return str(numero)

if __name__ == "__main__":
    unittest.main()