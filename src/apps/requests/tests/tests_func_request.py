from selenium import webdriver
from selenium.webdriver.common.by import By
from django.test import TestCase
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.test import TestCase, Client
import re
class Requests(TestCase):
    def setUp(self):
        
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        

    def tearDown(self):
        self.driver.quit()

    def tesst_show_request_table(self):
        self.login("123456789")
        bread_crumbs = self.driver.find_element(By.XPATH, '//*[@id="navBarHeader"]/div/h5')
        table = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable thead tr th:nth-child(1) span")
        table1 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable thead tr th:nth-child(2) span")
        table2 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable thead tr th:nth-child(3) span")
        table3 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable thead tr th:nth-child(4) span")
        table4 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable thead tr th:nth-child(5) span")
        table5 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable thead tr th:nth-child(6) span")
        table6 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable thead tr th:nth-child(7) span")
        action = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable tbody tr td:nth-child(7) button")
        
        self.assertEqual(bread_crumbs.text, "Solicitudes / Solicitudes de Sharepoint")
        self.assertEqual(table.text, "ID")
        self.assertEqual(table1.text, "ESTADO")
        self.assertEqual(table2.text, "FECHA INICIO")
        self.assertEqual(table3.text, "FECHA FINAL")
        self.assertEqual(table4.text, "SOLICITANTE")
        self.assertEqual(table5.text, "GESTOR")
        self.assertEqual(table6.text, "ACCIONES")
        first_child_element = self.driver.execute_script("return arguments[0].firstChild;", action)
        self.assertEqual(first_child_element['textContent'], "\n                        Detalles\n                        ")

    def tesst_show_request_table(self):
        self.login("123456789")
        action = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable tbody tr td:nth-child(7) button")
        action.click()
        fld1 = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div#detailsContent div table tbody tr:nth-child(1) th"))
        ) 
        fld2 = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div#detailsContent div table tbody tr:nth-child(2) th"))
        ) 
        fld3 = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div#detailsContent div table tbody tr:nth-child(3) th"))
        ) 
        fld4 = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div#detailsContent div table tbody tr:nth-child(4) th"))
        ) 
        fld5 = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div#detailsContent div table tbody tr:nth-child(5) th"))
        ) 
        fld6 = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div#detailsContent div table tbody tr:nth-child(6) th"))
        ) 
        fld7 = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div#detailsContent div table tbody tr:nth-child(7) th"))
        ) 
        fld8 = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div#detailsContent div table tbody tr:nth-child(8) th"))
        ) 
        fld9 = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div#detailsContent div table tbody tr:nth-child(9) th"))
        ) 
        fld10 = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div#detailsContent div table tbody tr:nth-child(10) th"))
        )
        fld11 = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div#detailsContent div table tbody tr:nth-child(11) th"))
        ) 
        fld12 = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div#detailsContent div table tbody tr:nth-child(12) th"))
        ) 
        fld13 = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div#detailsContent div table tbody tr:nth-child(13) th"))
        ) 
        fld14 = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div#detailsContent div table tbody tr:nth-child(14) th"))
        ) 
        fld15 = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div#detailsContent div table tbody tr:nth-child(15) th"))
        ) 
        fld16 = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div#detailsContent div table tbody tr:nth-child(16) th"))
        ) 
        fld17 = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div#detailsContent div table tbody tr:nth-child(17) th"))
        ) 
        fld18 = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div#detailsContent div table tbody tr:nth-child(18) th"))
        ) 
    
        self.assertEqual(fld1.text, "ID")
        self.assertEqual(fld2.text, "ESTADO")
        self.assertEqual(fld3.text, "GESTOR")
        self.assertEqual(fld4.text, "FECHA INICIAL")
        self.assertEqual(fld5.text, "FECHA FINAL")
        self.assertEqual(fld6.text, "NOMBRE COMPLETO")
        self.assertEqual(fld7.text, "FACULTAD")
        self.assertEqual(fld8.text, "DOCUMENTO")
        self.assertEqual(fld9.text, "TELÉFONO")
        self.assertEqual(fld10.text, "CORREO ELECTRÓNICO")
        self.assertEqual(fld11.text, "CENCO")
        self.assertEqual(fld12.text, "BANCO")
        self.assertEqual(fld13.text, "TIPO DE CUENTA")
        self.assertEqual(fld14.text, "EPS")
        self.assertEqual(fld15.text, "FONDO DE PENSIONES")
        self.assertEqual(fld16.text, "ARL")
        self.assertEqual(fld17.text, "VALOR DE CONTRATO")
        self.assertEqual(fld18.text, "PAGO ÚNICO")

    def tesst_search_request_happy(self):
        self.login("123456789")
        input_search = self.driver.find_element(By.ID, "requestsTableSearch")
        srch = "11"
        input_search.send_keys(srch)
        table = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable tbody td:nth-child(1)")
        table1 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable tbody td:nth-child(2)")
        table2 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable tbody td:nth-child(3)")
        table3 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable tbody td:nth-child(4)")
        table4 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable tbody td:nth-child(5)")
        table5 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable tbody td:nth-child(6)")
        table6 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable tbody td:nth-child(7)")
        self.assertTrue(table.text.__contains__(srch) or table1.text.__contains__(srch) or table2.text.__contains__(srch) or table3.text.__contains__(srch) or table4.text.__contains__(srch) or table5.text.__contains__(srch) or table6.text.__contains__(srch))

    def tesst_search_request_notFound(self):
        self.login("123456789")
        input_search = self.driver.find_element(By.ID, "requestsTableSearch")
        input_search.send_keys("00")
        result = self.driver.find_element(By.XPATH, '//*[@id="requestsTable"]/tbody/tr/td')
        self.assertTrue(result.text, "No se encontraron resultados")

        
    def tesst_assert_state(self):
        self.login("123456789")
        table1 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable tbody td:nth-child(6)")
        self.assertTrue(table1.text == "PAGADO - CONTABILIDAD" or table1.text == "APROBADO - DECANO" or table1.text == "APROBADO - CENCO" or table1.text == "CERRADO" or table1.text == "RECHAZADO - DECANO")

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

    def extraer_texto(self, texto):
    # Define el patrón de búsqueda utilizando una expresión regular
        patron = r'@([^)]+)'
        # Busca todas las ocurrencias del patrón en el texto
        coincidencias = re.findall(patron, texto)
        # Retorna la lista de coincidencias encontradas
        return coincidencias

