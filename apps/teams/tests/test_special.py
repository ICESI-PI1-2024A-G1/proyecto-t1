from selenium import webdriver
from selenium.webdriver.common.by import By
from django.test import TestCase
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.test import TestCase, Client
import re
import subprocess
import time


class teams_test(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)

    def tearDown(self):
        self.driver.quit()

    def test_change_leader_and_delete_team_succesful(self):
        ruta_script = "generate_for_teams.py"
        comando = f"python {ruta_script}"
        subprocess.call(comando, shell=True)
        self.login("123456789")
        self.select_opt_teams("1")
        self.click_opt_first("2")
        self.driver.find_element(By.ID, "leader").click()
        self.driver.find_element(By.CSS_SELECTOR, "#leader option:nth-child(3)").click()
        self.driver.find_element(
            By.XPATH, '//*[@id="mainContainer"]/form/div[3]/div/div[2]/button'
        ).click()
        alert = self.get_alert()
        self.assertEqual(alert.text, "Equipo editado con éxito")
        WebDriverWait(self.driver, 30).until(
            EC.invisibility_of_element_located((By.ID, "toast-body"))
        )
        self.click_opt_first("3")
        time.sleep(2)
        alerta = self.driver.switch_to.alert
        alerta.accept()
        alert = self.get_alert()
        self.assertEqual(alert.text, "Equipo eliminado con éxito")

    def click_opt_first(self, opt):
        son = ""
        if opt == "1":
            son = "button"
        else:
            son = "a"
        self.driver.find_element(
            By.CSS_SELECTOR, "table#teamsTable tbody td:nth-child(7) div button"
        ).click()
        table2 = self.driver.find_element(
            By.CSS_SELECTOR,
            "table#teamsTable tbody td:nth-child(7) div div "
            + son
            + ":nth-child("
            + opt
            + ")",
        )
        table2.click()

    def select_opt_teams(self, num):
        teambtn = self.driver.find_element(
            By.XPATH, '//*[@id="layout-menu"]/ul/li[3]/a'
        )
        teambtn.click()
        addbtn = self.driver.find_element(
            By.XPATH, '//*[@id="layout-menu"]/ul/li[3]/ul/li[' + num + "]/a"
        )
        addbtn.click()

    def select_option(self, selector):
        self.driver.find_element(By.CSS_SELECTOR, selector).click()
        self.driver.find_element(
            By.CSS_SELECTOR, selector + " option:nth-child(2)"
        ).click()

    def fill_req(self):
        self.login("99685182")
        self.click_form("5")

        self.driver.find_element(By.ID, "work").send_keys("Comandante general")

        self.driver.find_element(By.ID, "idValue").send_keys("1000000")

        selects = ["#dependence", "#cenco"]

        for selector in selects:
            self.select_option(selector)

        self.driver.find_element(By.ID, "description").send_keys(
            "My name is Yoshikage Kira. I'm 33 years old. My house is in the northeast section of Morioh, where all the villas are, and I am not married. I work as an employee for the Kame Yu department stores, and I get home every day by 8 PM at the latest. I don't smoke, but I occasionally drink. I'm in bed by 11 PM, and make sure I get eight hours of sleep, no matter what. After having a glass of warm milk and doing about twenty minutes of stretches before going to bed, I usually have no problems sleeping until morning. Just like a baby, I wake up without any fatigue or stress in the morning. I was told there were no issues at my last check-up. I'm trying to explain that I'm a person who wishes to live a very quiet life. I take care not to trouble myself with any enemies, like winning and losing, that would cause me to lose sleep at night. That is how I deal with society, and I know that is what brings me happiness. Although, if I were to fight I wouldn't lose to anyone."
        )
        self.sign("robotop")

        self.driver.find_element(By.NAME, "bank").click()
        self.driver.find_element(
            By.XPATH,
            '//*[@id="mainContainer"]/form/div[2]/div[11]/div[1]/select/option[2]',
        ).click()

        self.driver.find_element(By.NAME, "accountType").click()
        self.driver.find_element(
            By.XPATH,
            '//*[@id="mainContainer"]/form/div[2]/div[11]/div[2]/select/option[2]',
        ).click()

        self.driver.find_element(By.ID, "idBank").send_keys("456475")

        self.driver.find_element(
            By.XPATH, '//*[@id="mainContainer"]/form/div[3]/div/button'
        ).click()

    def click_form(self, number):
        self.driver.find_element(By.XPATH, '//*[@id="layout-menu"]/ul/li[3]/a').click()
        self.driver.find_element(
            By.XPATH, '//*[@id="layout-menu"]/ul/li[3]/ul/li[' + number + "]"
        ).click()

    def sign(self, sign):
        self.driver.find_element(By.ID, "signButton").click()
        self.select_option("#swal2-select")

        self.driver.find_element(
            By.XPATH, "/html/body/div[4]/div/div[6]/button[1]"
        ).click()

        self.driver.find_element(By.ID, "swal2-input").send_keys(sign)
        self.driver.find_element(
            By.XPATH, "/html/body/div[4]/div/div[6]/button[1]"
        ).click()

    def check_all_fields(self):
        reason_fl = self.driver.find_element(By.ID, "reason").send_keys("Razon válida")

        checkAll = self.driver.find_element(By.ID, "markAll")
        checkAll.click()

    def accept_all_fields(self):
        reason_fl = self.driver.find_element(By.ID, "reason").send_keys("Razon válida")

        checkAll = self.driver.find_element(By.ID, "markAll")
        checkAll.click()

        self.accept_alert((By.ID, "completeReview"))

    def accept_alert(self, selector):

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(selector)
        ).click()

        confirmBtn = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div[5]/div/div[4]/div[2]/button")
            )
        )
        confirmBtn.click()

        WebDriverWait(self.driver, 30).until(
            EC.invisibility_of_element_located((By.ID, "detailsContent"))
        )

    def scroll_element(self, element):
        scroll_height = element.size["height"]
        self.driver.execute_script(
            "arguments[0].scrollTop = arguments[0].scrollHeight", element
        )

    def extract_gestor(self):
        tableUser = self.driver.find_element(
            By.CSS_SELECTOR, "table#requestsTable tbody td:nth-child(6)"
        )
        return self.extraer_texto(tableUser.text)

    def logout(self):
        logout = self.driver.find_element(By.XPATH, '//*[@id="layout-navbar"]/div[3]')
        logout.click()

    def get_status(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "table#requestsTable tbody td:nth-child(7)")
            )
        )

    def get_alert(self):
        return WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.ID, "toast-body"))
        )

    def click_change_state(self):
        table1 = self.driver.find_element(
            By.CSS_SELECTOR, "table#requestsTable tbody td:nth-child(8) div button"
        )
        table1.click()
        table2 = self.driver.find_element(
            By.CSS_SELECTOR,
            "table#requestsTable tbody td:nth-child(8) div div button:nth-child(2)",
        )
        table2.click()

    def search(self, criteria):
        input_search = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "requestsTableSearch"))
        )
        input_search.send_keys(criteria)

    def input_change_reason(self, reason):
        reasonTxt = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "reasonTextarea"))
        )
        reasonTxt.send_keys(reason)
        changeBtn = self.driver.find_element(By.ID, "changeStatusBtn")
        changeBtn.click()

        confirmBtn = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div[5]/div/div[6]/button[1]")
            )
        )
        confirmBtn.click()

    def click_inner_requests(self):
        intern = self.driver.find_element(
            By.XPATH, '//*[@id="layout-menu"]/ul/li[2]/ul/li[2]/a'
        )
        intern.click()

    def click_review_first(self):
        table1 = self.driver.find_element(
            By.CSS_SELECTOR, "table#requestsTable tbody td:nth-child(8) div button"
        )
        table1.click()
        table2 = self.driver.find_element(
            By.CSS_SELECTOR,
            "table#requestsTable tbody td:nth-child(8) div div button:nth-child(1)",
        )
        table2.click()

    def click_first(self, num):
        table1 = self.driver.find_element(
            By.CSS_SELECTOR, "table#requestsTable tbody td:nth-child(8) div button"
        )
        table1.click()
        table2 = self.driver.find_element(
            By.CSS_SELECTOR,
            "table#requestsTable tbody td:nth-child(8) div div button:nth-child("
            + num
            + ")",
        )
        table2.click()

    def login(self, user):
        client = Client()
        self.driver.get("http://127.0.0.1:8000/")
        user_input = self.driver.find_element(By.ID, "usuario")
        pass_input = self.driver.find_element(By.ID, "contrasena")
        login_btn = self.driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div/div/div/div[2]/form/div[2]"
        )
        user_input.send_keys(user)
        pass_input.send_keys("123456789")
        login_btn.click()
        file = open("codes.txt")
        verification_code = file.read()

        code_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "verificationCode"))
        )

        code_btn = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[1]/div/div/div/div/div[3]/form/div[2]/button",
                )
            )
        )
        code_input.send_keys(verification_code)
        code_btn.click()

    def extraer_texto(self, texto):
        # Define el patrón de búsqueda utilizando una expresión regular
        patron = r"@([^)]+)"
        # Busca todas las ocurrencias del patrón en el texto
        coincidencias = re.findall(patron, texto)
        # Retorna la lista de coincidencias encontradas
        return coincidencias
