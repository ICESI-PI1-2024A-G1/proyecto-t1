from selenium import webdriver
from selenium.webdriver.common.by import By
from django.test import TestCase
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.test import TestCase, Client

class permission_test(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        

    def tearDown(self):
        self.driver.quit()

    def test_change_leader_to_member(self):
        self.login("123456789")
        
        self.driver.find_element(By.XPATH, '//*[@id="layout-menu"]/ul/li[8]/a').click()
        self.search("Natali")
        self.driver.find_element(By.CSS_SELECTOR, 'table#usersTable tbody tr td:nth-child(6) input').click()
        self.driver.find_element(By.ID, "saveButton").click()
        alert = self.get_alert()
        self.assertEqual(alert.text, 'Permisos actualizados correctamente.')

    def test_change_member_with_req(self):
        self.login("123456789")
        self.driver.find_element(By.XPATH, '//*[@id="layout-menu"]/ul/li[8]/a').click()

        self.driver.find_element(By.CSS_SELECTOR, 'table#usersTable tbody tr td:nth-child(7) input').click()
        self.driver.find_element(By.ID, "saveButton").click()
        alert = self.get_alert()
        self.assertIn('No se puede cambiar el permiso de miembro a un usuario que es miembro de un equipo', alert.text)

    def test_change_member_to_leader(self):
        self.login("123456789")
        self.driver.find_element(By.XPATH, '//*[@id="layout-menu"]/ul/li[8]/a').click()
        self.search("Kath")
        self.driver.find_element(By.CSS_SELECTOR, 'table#usersTable tbody tr td:nth-child(5) input').click()
        self.driver.find_element(By.ID, "saveButton").click()
        alert = self.get_alert()
        self.assertEqual(alert.text, 'Permisos actualizados correctamente.')

    def test_change_leader_to_member_with_team(self):
        self.login("123456789")
        self.driver.find_element(By.XPATH, '//*[@id="layout-menu"]/ul/li[8]/a').click()
        self.driver.find_element(By.CSS_SELECTOR, 'table#usersTable tbody tr td:nth-child(7) input').click()
        self.driver.find_element(By.ID, "saveButton").click()
        alert = self.get_alert()
        
        self.assertIn('No se puede cambiar el permiso de miembro a un usuario que es miembro de un equipo.', alert.text)

    def search(self, criteria):
        input_search =  WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "usersTableSearch"))
        )    
        input_search.send_keys(criteria)

    def logout(self):
        logout = self.driver.find_element(By.XPATH, '//*[@id="layout-navbar"]/div[3]')
        logout.click()

    def get_alert(self):
        return WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.ID, "toast-body"))
        ) 

    def login(self, user): 
        client = Client()
        self.driver.get("http://127.0.0.1:8000/")
        user_input = self.driver.find_element(By.ID,"usuario")
        pass_input = self.driver.find_element(By.ID,"contrasena")
        login_btn = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div[2]/form/div[2]")
        user_input.send_keys(user)
        pass_input.send_keys("123456789")
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