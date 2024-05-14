import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.models import CustomUser
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
class Registration(unittest.TestCase):
    """
    Test case for user registration functionality.

    This test case covers various scenarios related to user registration, 
    including successful registration, repeated username, invalid username,
    invalid email, invalid password, and password mismatch.
    """

    def setUp(self):
        """
        Set up method to initialize the test environment.

        This method sets up the WebDriver environment for testing.
        """
        self.user = "111111"
        self.userName = ""
        self.email = 'cssa_register_user@hotmail.com'
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)

    def tearDown(self):
        """
        Tear down method to clean up after the tests.

        This method deletes any user created during the tests and quits the WebDriver.
        """
        nombre_usuario = self.userName
        if CustomUser.objects.filter(username=nombre_usuario).exists():
            usuario_a_eliminar = CustomUser.objects.get(username=nombre_usuario)
            usuario_a_eliminar.delete()
        self.driver.quit()

    def test_register_happy_path(self):
        """
        Test registering with valid input.

        This test verifies the successful registration of a user with valid input.
        """
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
        self.userName = self.generate_random_id()
        id_field.send_keys(self.userName)
        email_field.send_keys(self.email)
        pass_field.send_keys(psw)
        con_pass_field.send_keys(psw)
        rgstr_btn.click()
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
        success_msg = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.ID, "toast-body"))
        )
        self.assertEqual(success_msg.text, "Usuario registrado correctamente.")

    def test_register_repeated_username(self):
        """
        Test registering with a repeated username.

        This test verifies the behavior when attempting to register with a username that already exists.
        """
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
        """
        Test registering with an invalid username.

        This test checks the behavior when providing an invalid username during registration.
        """
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
        """
        Test registering with a second type of invalid username.

        This test checks the behavior when providing another type of invalid username during registration.
        """

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
        """
        Test registering with an invalid email.

        This test checks the behavior when providing an invalid email address during registration.
        """
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
        self.userName = self.generate_random_id()
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
        """
        Test registering with an invalid password.

        This test verifies the behavior when providing an invalid password during registration.
        """
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
        self.userName = self.generate_random_id()
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
        """
        Test registering with different passwords.

        This test checks the behavior when the passwords provided during registration do not match.
        """
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
        self.userName = self.generate_random_id()
        id_field.send_keys(self.userName)
        email_field.send_keys(self.email)
        pass_field.send_keys(psw)
        con_pass_field.send_keys(psw2)
        rgstr_btn.click()

        error_msg = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.ID, "toast-body"))
        )
        self.assertEqual(error_msg.text, "Las contraseñas no coinciden.")

    def generate_random_id(self):
        """
        Generate a random ID for testing.

        This method generates a random numerical ID for testing purposes.
        """
        numero = random.randint(1000001, 999999999999)
        return str(numero)

if __name__ == "__main__":
    unittest.main()