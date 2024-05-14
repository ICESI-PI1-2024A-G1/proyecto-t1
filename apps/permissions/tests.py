from selenium import webdriver
from selenium.webdriver.common.by import By
from django.test import TestCase
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.test import TestCase, Client

class permission_test(TestCase):
    """
    Test case for permission-related functionalities.

    This test case covers various scenarios related to user permissions, 
    such as changing a user from leader to member, member with requests, 
    member to leader, and leader to member when the user is a member of a team.
    """
    def setUp(self):
        """
        Set up method to initialize the test environment.

        This method sets up the WebDriver environment for testing.
        """
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        

    def tearDown(self):
        """
        Tear down method to clean up after the tests.

        This method quits the WebDriver after each test.
        """
        self.driver.quit()

    def test_change_leader_to_member(self):
        """
        Test changing a leader to a member.

        This test verifies the functionality of changing a user's role from
        leader to member.
        """
        self.login("123456789")
        
        self.driver.find_element(By.XPATH, '//*[@id="layout-menu"]/ul/li[8]/a').click()
        self.search("Natali")
        self.driver.find_element(By.CSS_SELECTOR, 'table#usersTable tbody tr td:nth-child(6) input').click()
        self.driver.find_element(By.ID, "saveButton").click()
        alert = self.get_alert()
        self.assertEqual(alert.text, 'Permisos actualizados correctamente.')

    def test_change_member_with_req(self):
        """
        Test changing a member with requests.

        This test verifies the behavior when attempting to change a member's
        role to leader when the member has active requests.
        """
        self.login("123456789")
        self.driver.find_element(By.XPATH, '//*[@id="layout-menu"]/ul/li[8]/a').click()

        self.driver.find_element(By.CSS_SELECTOR, 'table#usersTable tbody tr td:nth-child(7) input').click()
        self.driver.find_element(By.ID, "saveButton").click()
        alert = self.get_alert()
        self.assertIn('No se puede cambiar el permiso de miembro a un usuario que es miembro de un equipo', alert.text)

    def test_change_member_to_leader(self):
        """
        Test changing a member to a leader.

        This test checks the functionality of promoting a member to a leader.
        """
        self.login("123456789")
        self.driver.find_element(By.XPATH, '//*[@id="layout-menu"]/ul/li[8]/a').click()
        self.search("Kath")
        self.driver.find_element(By.CSS_SELECTOR, 'table#usersTable tbody tr td:nth-child(5) input').click()
        self.driver.find_element(By.ID, "saveButton").click()
        alert = self.get_alert()
        self.assertEqual(alert.text, 'Permisos actualizados correctamente.')

    def test_change_leader_to_member_with_team(self):
        """
        Test changing a leader to a member with team membership.

        This test verifies the behavior when trying to change a leader to a
        member when the user is already a member of a team.
        """
        self.login("123456789")
        self.driver.find_element(By.XPATH, '//*[@id="layout-menu"]/ul/li[8]/a').click()
        self.driver.find_element(By.CSS_SELECTOR, 'table#usersTable tbody tr td:nth-child(7) input').click()
        self.driver.find_element(By.ID, "saveButton").click()
        alert = self.get_alert()
        
        self.assertIn('No se puede cambiar el permiso de miembro a un usuario que es miembro de un equipo.', alert.text)

    def search(self, criteria):
        """
        Helper method to perform a search.

        This method performs a search operation based on the provided criteria.
        """
        input_search =  WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "usersTableSearch"))
        )    
        input_search.send_keys(criteria)

    def logout(self):
        """
        Helper method to perform logout.

        This method simulates the logout functionality.
        """
        logout = self.driver.find_element(By.XPATH, '//*[@id="layout-navbar"]/div[3]')
        logout.click()

    def get_alert(self):
        """
        Helper method to get the alert message.

        This method retrieves the alert message displayed on the page.
        """
        return WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.ID, "toast-body"))
        ) 

    def login(self, user): 
        """
        Helper method to perform login.

        This method simulates the login process for the specified user.
        """
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