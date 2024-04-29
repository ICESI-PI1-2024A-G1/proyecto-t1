from selenium import webdriver
from selenium.webdriver.common.by import By
import imaplib
import email
import time
from django.test import TestCase
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
class Requests(TestCase):
    def setUp(self):
        
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.login()

    def tearDown(self):
        self.driver.quit()

    def tesst_show_request_table(self):
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
        
    def tesst_search_request(self):
        input_search = self.driver.find_element(By.ID, "requestsTableSearch")
        input_search.send_keys("00")
        table = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable tbody td:nth-child(1)")
        table1 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable tbody td:nth-child(2)")
        table2 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable tbody td:nth-child(3)")
        table3 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable tbody td:nth-child(4)")
        table4 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable tbody td:nth-child(5)")
        table5 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable tbody td:nth-child(6)")
        table6 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable tbody td:nth-child(7)")
        self.assertTrue(table.text.__contains__("00") or table1.text.__contains__("00") or table2.text.__contains__("00") or table3.text.__contains__("00") or table4.text.__contains__("00") or table5.text.__contains__("00") or table6.text.__contains__("00"))

        
    def tesst_assert_state(self):
        table1 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable tbody td:nth-child(2)")
        self.assertTrue(table1.text == "PAGADO - CONTABILIDAD" or table1.text == "APROBADO - DECANO" or table1.text == "APROBADO - CENCO" or table1.text == "CERRADO" or table1.text == "RECHAZADO - DECANO")

    def tesst_show_request_table(self):
        intern = self.driver.find_element(By.XPATH, '//*[@id="layout-menu"]/ul/li[2]/ul/li[2]/a')
        intern.click()
        bread_crumbs = self.driver.find_element(By.XPATH, '//*[@id="navBarHeader"]/div/h5')
        table = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable thead tr th:nth-child(1) span")
        table1 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable thead tr th:nth-child(2) span")
        table2 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable thead tr th:nth-child(3) span")
        table3 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable thead tr th:nth-child(4) span")
        table4 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable thead tr th:nth-child(5) span")
        table5 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable thead tr th:nth-child(6) span")
        table6 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable thead tr th:nth-child(7) span")
        action = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable tbody tr td:nth-child(8) div button i")
        
        self.assertEqual(bread_crumbs.text, "Solicitudes / Solicitudes Internas")
        self.assertEqual(table.text, "ID")
        self.assertEqual(table1.text, "FECHA INICIO")
        self.assertEqual(table2.text, "FECHA FINAL")
        self.assertEqual(table3.text, "DOCUMENTO")
        self.assertEqual(table4.text, "SOLICITANTE")
        self.assertEqual(table5.text, "GESTOR")
        self.assertEqual(table6.text, "ESTADO")
        first_child_element = self.driver.execute_script("return arguments[0].className;", action)
        self.assertEqual(first_child_element, 'bx bx-dots-vertical-rounded')

    def tesst_search_request_inner(self):
            intern = self.driver.find_element(By.XPATH, '//*[@id="layout-menu"]/ul/li[2]/ul/li[2]/a')
            intern.click()
            search = "11"
            input_search = self.driver.find_element(By.ID, "requestsTableSearch")
            input_search.send_keys(search)
            table = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable tbody td:nth-child(1)")
            table1 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable tbody td:nth-child(2)")
            table2 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable tbody td:nth-child(3)")
            table3 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable tbody td:nth-child(4)")
            table4 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable tbody td:nth-child(5)")
            table5 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable tbody td:nth-child(6)")
            table6 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable tbody td:nth-child(7)")
            self.assertTrue(table.text.__contains__(search) or table1.text.__contains__(search) or table2.text.__contains__(search) or table3.text.__contains__(search) or table4.text.__contains__(search) or table5.text.__contains__(search) or table6.text.__contains__(search))

    def tesst_assert_inner_state(self):
        intern = self.driver.find_element(By.XPATH, '//*[@id="layout-menu"]/ul/li[2]/ul/li[2]/a')
        intern.click()
        table1 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable thead th:nth-child(2)")
        self.assertTrue(table1.text == "EN REVISIÓN" or table1.text == "DEVUELTO" or table1.text == "PENDIENTE" or table1.text == "RESUELTO" or table1.text == "RECHAZADO" or table1.text == "POR APROBAR")

    def test_review_request_happy_path(self):
        intern = self.driver.find_element(By.XPATH, '//*[@id="layout-menu"]/ul/li[2]/ul/li[2]/a')
        intern.click()
        
        tb= self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable thead th:nth-child(2)")
        tb.click()
        table1 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable tbody td:nth-child(8) div button")
        table1.click()
        table2 = self.driver.find_element(By.CSS_SELECTOR, "table#requestsTable tbody td:nth-child(8) div div button:nth-child(1)")
        table2.click()
        mdl = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located((By.ID, "detailsContent"))
        ) 

        scroll_height = mdl.size['height']
        self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", mdl)

        reason_fl = self.driver.find_element(By.ID, "reason")
        reason_fl.send_keys("Razon válida")

        checkAll = self.driver.find_element(By.ID, "markAll")
        checkAll.click()

        completeBtn = self.driver.find_element(By.ID, "completeReview")
        completeBtn.click()

        
        input(" ")

    def login(self): 
        self.driver.get("http://127.0.0.1:8000/")
        user_input = self.driver.find_element(By.ID,"usuario")
        pass_input = self.driver.find_element(By.ID,"contrasena")
        login_btn = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div[2]/form/div[2]")
        user_input.send_keys("123456789")
        pass_input.send_keys("123456789")
        login_btn.click()

        time.sleep(5)
        verification_code = self.get_code_from_email()
        
        code_input = self.driver.find_element(By.ID,"verificationCode")
        code_btn = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div/div/div[3]/form/div[2]/button")

        code_input.send_keys(verification_code)
        code_btn.click()

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
    
