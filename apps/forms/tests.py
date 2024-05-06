from selenium import webdriver
from selenium.webdriver.common.by import By
from django.test import TestCase
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.test import TestCase, Client
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import os
import re
class Requests(TestCase):
    def setUp(self):
        
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        

    def tearDown(self):
        self.driver.quit()

    def test_fill_form_happy_req(self):
        self.login("99685182")
        self.click_form("5")

        self.driver.find_element(By.ID, "work").send_keys("Comandante general")

        self.driver.find_element(By.ID, "idValue").send_keys("1000000")   

        selects = ["#dependence", "#cenco"]

        for selector in selects:
            self.select_option(selector)

        self.driver.find_element(By.ID, "description").send_keys("My name is Yoshikage Kira. I'm 33 years old. My house is in the northeast section of Morioh, where all the villas are, and I am not married. I work as an employee for the Kame Yu department stores, and I get home every day by 8 PM at the latest. I don't smoke, but I occasionally drink. I'm in bed by 11 PM, and make sure I get eight hours of sleep, no matter what. After having a glass of warm milk and doing about twenty minutes of stretches before going to bed, I usually have no problems sleeping until morning. Just like a baby, I wake up without any fatigue or stress in the morning. I was told there were no issues at my last check-up. I'm trying to explain that I'm a person who wishes to live a very quiet life. I take care not to trouble myself with any enemies, like winning and losing, that would cause me to lose sleep at night. That is how I deal with society, and I know that is what brings me happiness. Although, if I were to fight I wouldn't lose to anyone.")
        self.sign("robotop")

        self.driver.find_element(By.NAME, 'bank').click()
        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]/div[11]/div[1]/select/option[2]').click()

        self.driver.find_element(By.NAME, 'accountType').click()
        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]/div[11]/div[2]/select/option[2]').click()
        
        self.driver.find_element(By.ID, "idBank").send_keys("456475")

        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[3]/div/button').click()

        aler = self.get_alert()
        self.assertEqual(aler.text, "Formulario enviado correctamente. Puede revisarlo en la sección de Solicitudes.")

    def tesst_fill_form_happy_cc(self):
        self.login("99685182")
        self.click_form("4")

        self.driver.find_element(By.ID, "value").send_keys("1000000")

        self.driver.find_element(By.ID, "conceptReason").send_keys("Compras compulsivas")

        self.driver.find_element(By.ID, "retentionYes").click()
        self.driver.find_element(By.ID, "taxPayerYes").click()
        self.driver.find_element(By.ID, "residentNo").click()

        self.select_option("#requestCity")

        self.driver.find_element(By.ID, "phoneNumber").send_keys("3015582755")
        self.driver.find_element(By.ID, "address").send_keys("CLL Cristian, 75-24")

        self.sign("robotop")

        self.driver.find_element(By.NAME, 'bank').click()
        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]/div[15]/div[1]/select/option[2]').click()

        self.driver.find_element(By.NAME, 'accountType').click()
        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]/div[15]/div[2]/select/option[2]').click()
        
        self.driver.find_element(By.ID, "idBank").send_keys("456475")
        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[3]/div/button').click()

        self.driver.find_element(By.ID, "idCex").send_keys("78651")
        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[3]/div/button').click()

        aler = self.get_alert()

        self.assertEqual(aler.text, "Formulario enviado correctamente. Puede revisarlo en la sección de Solicitudes.")

    def tesst_fill_form_happy_legan(self):
        self.login("99685182")
        self.click_form("3")
        
        scrollable = self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]')
        selects = ["#dependence", "#costCenter"]
        for selector in selects:
            self.select_option(selector)

        self.driver.find_element(By.ID, "purchaseReason").send_keys("Compras compulsivas")

        self.fill_rowsadv()

        self.driver.find_element(By.NAME, "advanceTotal").send_keys("10000")
        self.sign("robotop")

        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]/div[13]/div[1]/select').click()
        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]/div[13]/div[1]/select/option[2]').click()

        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]/div[13]/div[2]/select').click()
        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]/div[13]/div[2]/select/option[2]').click()
        
        self.driver.find_element(By.ID, "idBank").send_keys("456475")
        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[3]/div/button').click()

        aler = self.get_alert()
        self.assertEqual(aler.text, "Formulario enviado correctamente. Puede revisarlo en la sección de Solicitudes.")

    def tesst_fill_form_happy_legv(self):
        self.login("99685182")
        self.click_form("2")
        
        scrollable = self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]')
        selects = ["#dependence", "#costCenter", "#destinationCity"]
        for selector in selects:
            self.select_option(selector)

        self.inputDates("01022024", "07022024")
        
        self.driver.find_element(By.ID, "travelReason").send_keys("Cumpleaños")

        self.fill_rows()

        self.fill_advance()

        self.sign("robotop")

        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]/div[16]/div[1]/select').click()
        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]/div[16]/div[1]/select/option[2]').click()

        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]/div[16]/div[2]/select').click()
        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]/div[16]/div[2]/select/option[2]').click()
        
        self.driver.find_element(By.ID, "idBank").send_keys("456475")
        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[3]/div/button').click()

        aler = self.get_alert()
        self.assertEqual(aler.text, "Formulario enviado correctamente. Puede revisarlo en la sección de Solicitudes.")

    def fill_advance(self):
        self.driver.find_element(By.ID, "advanceTotal1").send_keys("100000")
        self.driver.find_element(By.ID, "advanceTotal2").send_keys("100")
        self.driver.find_element(By.ID, "advanceTotal3").send_keys("80")
        

    def fill_rows(self):
        i = 0
        while True:
            try:
                self.driver.find_element(By.ID, "provider_"+str(i)).send_keys("Chocolisto S.A")
                
                self.driver.find_element(By.ID, "nit_"+str(i)).send_keys("4156185")

                self.driver.find_element(By.ID, "concept_"+str(i)).send_keys("Avianca")
                self.driver.find_element(By.ID, "pesos_"+str(i)).send_keys("130000")
                self.driver.find_element(By.ID, "dollars_"+str(i)).send_keys("200")
                self.driver.find_element(By.ID, "euros_"+str(i)).send_keys("140")

                i += 1
            except NoSuchElementException:

                break

    def fill_rowsadv(self):
        i = 0
        while True:
            try:
                self.driver.find_element(By.NAME, "category_"+str(i)).send_keys("Saldo")
                
                self.driver.find_element(By.NAME, "provider_"+str(i)).send_keys("Morty y asociados")

                self.driver.find_element(By.NAME, "pesos_"+str(i)).send_keys("50000")
                self.driver.find_element(By.NAME, "concept_"+str(i)).send_keys("Interdimesional")

                i += 1
            except NoSuchElementException:

                break
    def tesst_fill_form_happy_1(self):
        self.login("99685182")
        self.click_form("1")
        
        scrollable = self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]')
        selects = ["#dependence", "#costCenter", "#destinationCity"]
        for selector in selects:
            self.select_option(selector)

        self.inputDates("01022024", "07022024")
        
        self.driver.find_element(By.ID, "travelReason").send_keys("Cumpleaños")

        self.driver.find_element(By.ID, "dollars").click()

        self.fill_prices(2,12,2)

        tot = self.driver.find_element(By.ID, "total")
        self.assertEqual(tot.get_attribute("value"), "6")

        self.sign("robotop")

        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]/div[17]/div[1]/select').click()
        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]/div[17]/div[1]/select/option[2]').click()

        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]/div[17]/div[2]/select').click()
        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]/div[17]/div[2]/select/option[2]').click()
        
        self.driver.find_element(By.ID, "idBank").send_keys("456475")
        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[3]/div/button').click()

        aler = self.get_alert()
        self.assertEqual(aler.text, "Formulario enviado correctamente. Puede revisarlo en la sección de Solicitudes.")

    def tesst_fill_form_happy_sign2(self):
        self.login("99685182")
        self.click_form("1")
        
        scrollable = self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]')
        selects = ["#dependence", "#costCenter", "#destinationCity"]
        for selector in selects:
            self.select_option(selector)

        self.inputDates("01022024", "07022024")
        
        self.driver.find_element(By.ID, "travelReason").send_keys("Cumpleaños")

        self.driver.find_element(By.ID, "dollars").click()

        self.fill_prices(2,12,2)

        tot = self.driver.find_element(By.ID, "total")
        self.assertEqual(tot.get_attribute("value"), "6")

        self.sign2()
        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]/div[17]/div[1]/select').click()
        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]/div[17]/div[1]/select/option[2]').click()

        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]/div[17]/div[2]/select').click()
        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]/div[17]/div[2]/select/option[2]').click()
        
        self.driver.find_element(By.ID, "idBank").send_keys("456475")
        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[3]/div/button').click()

        aler = self.get_alert()
        self.assertEqual(aler.text, "Formulario enviado correctamente. Puede revisarlo en la sección de Solicitudes.")

    def tesst_fill_form_happy_sign3(self):
        self.login("99685182")
        self.click_form("1")
        
        scrollable = self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]')
        selects = ["#dependence", "#costCenter", "#destinationCity"]
        for selector in selects:
            self.select_option(selector)

        self.inputDates("01022024", "07022024")
        
        self.driver.find_element(By.ID, "travelReason").send_keys("Cumpleaños")

        self.driver.find_element(By.ID, "dollars").click()

        self.fill_prices(2,12,2)

        tot = self.driver.find_element(By.ID, "total")
        self.assertEqual(tot.get_attribute("value"), "6")

        self.sign3()
        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]/div[17]/div[1]/select').click()
        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]/div[17]/div[1]/select/option[2]').click()

        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]/div[17]/div[2]/select').click()
        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]/div[17]/div[2]/select/option[2]').click()
        
        self.driver.find_element(By.ID, "idBank").send_keys("456475")
        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[3]/div/button').click()

        aler = self.get_alert()
        self.assertEqual(aler.text, "Formulario enviado correctamente. Puede revisarlo en la sección de Solicitudes.")

    def tesst_fill_form_bad_dates(self):
        self.login("99685182")
        self.click_form("1")
        
        scrollable = self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]')
        selects = ["#dependence", "#costCenter", "#destinationCity"]
        for selector in selects:
            self.select_option(selector)
            
        self.inputDates("07022024","01022024")
        
        self.driver.find_element(By.ID, "travelReason").send_keys("Cumpleaños")

        self.driver.find_element(By.ID, "dollars").click()

        self.fill_prices(2,12,2)

        tot = self.driver.find_element(By.ID, "total")
        self.assertEqual(tot.get_attribute("value"), "6")

        self.sign("robotop")

        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]/div[17]/div[1]/select').click()
        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]/div[17]/div[1]/select/option[2]').click()

        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]/div[17]/div[2]/select').click()
        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]/div[17]/div[2]/select/option[2]').click()
        
        self.driver.find_element(By.ID, "idBank").send_keys("456475")
        self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[3]/div/button').click()

        aler = self.get_alert()
        self.assertEqual(aler.text, "La fecha de regreso no puede ser anterior a la fecha de salida.")

    def inputDates(self, init, end):
        self.driver.find_element(By.ID, "returnDate").send_keys(end)
        self.driver.find_element(By.ID, "departureDate").send_keys(init)

    def sign(self, sign):
        self.driver.find_element(By.ID, "signButton").click()
        self.select_option("#swal2-select")

        self.driver.find_element(By.XPATH, '/html/body/div[4]/div/div[6]/button[1]').click()

        self.driver.find_element(By.ID, "swal2-input").send_keys(sign)
        self.driver.find_element(By.XPATH, '/html/body/div[4]/div/div[6]/button[1]').click()

    def sign2(self):
        self.driver.find_element(By.ID, "signButton").click()
        self.select_optionz("#swal2-select", "3")

        self.driver.find_element(By.XPATH, '/html/body/div[4]/div/div[6]/button[1]').click()


        canvas = self.driver.find_element(By.XPATH, '//*[@id="swal2-html-container"]/canvas')
        action_chains = ActionChains(self.driver)
        action_chains.move_to_element_with_offset(canvas, 0, 0) 
        action_chains.click_and_hold()  
        action_chains.move_by_offset(10, 10) 
        action_chains.move_by_offset(20, 10) 
        action_chains.release() 
        action_chains.perform() 
        self.driver.find_element(By.XPATH, '/html/body/div[4]/div/div[6]/button[1]').click()


    def sign3(self):
        self.driver.find_element(By.ID, "signButton").click()
        self.select_optionz("#swal2-select", "4")

        self.driver.find_element(By.XPATH, '/html/body/div[4]/div/div[6]/button[1]').click()
 
        img = self.driver.find_element(By.XPATH, '/html/body/div[4]/div/input[2]')
        ruta_script = os.path.dirname(os.path.abspath(__file__))
        ruta_archivo = os.path.join(ruta_script, 'test', 'firma.jpg')

        img.send_keys(ruta_archivo)
        self.driver.find_element(By.XPATH, '/html/body/div[4]/div/div[6]/button[1]').click()

    def get_alert(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "toast-body"))
        ) 

    def select_option(self, selector):
        self.driver.find_element(By.CSS_SELECTOR, selector).click()
        self.driver.find_element(By.CSS_SELECTOR, selector+' option:nth-child(2)').click()

    def select_optionz(self, selector, opt):
        self.driver.find_element(By.CSS_SELECTOR, selector).click()
        self.driver.find_element(By.CSS_SELECTOR, selector+' option:nth-child('+opt+')').click()


    def fill_prices(self, init, end, step):
        for i in range(init, end+1, step):
            self.driver.find_element(By.XPATH, '//*[@id="mainContainer"]/form/div[2]/div[11]/div['+str(i)+']/input').send_keys("1")

    def scroll_element(self, element):
        scroll_height = 10000000000000
        self.driver.execute_script("arguments[0].scrollTop = {}", element, scroll_height)

    def click_form(self, number):
        self.driver.find_element(By.XPATH, '//*[@id="layout-menu"]/ul/li[3]/a').click()
        self.driver.find_element(By.XPATH, '//*[@id="layout-menu"]/ul/li[3]/ul/li['+number+']').click()

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

