from selenium import webdriver
import os
import glob
import os.path
import sys
import shutil
import re
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge
from selenium.webdriver.edge.options import Options


dir_inicial = "C:\\Tablero\\"
adjuntos = "C:\\Tablero\\Adjuntos\\"
ok = "C:\\Tablero\\ProcesadoOK\\"
     

cantdocs=len(glob.glob(adjuntos + "*"))

if cantdocs > 0:
    ruta = os.listdir(adjuntos)
    for i in ruta:
        #modularizar esto
        nombre_archivo = i
        lista = re.findall(r'\d+', nombre_archivo)

        for i in lista:
            if (len(str(i))) == 7:
                ticket = i
                break
            else:
                ticket = 99
        if not lista:
            print("no hay numeros")
        else: 
            if ticket == 99:
                print("no hay numero de 7 digitos")
            else:
                print("el ticket debe ser", ticket)
        print(lista)
        ticket = lista[0]
        print(ticket)
        edge_option = EdgeOptions()
        edge_option.add_argument("hide_console")
        driver = Edge("C:\Google\msedgedriver", service_args= ["hide_console"])
        url = "http://10.1.27.11:8080/tfs/TFSYPF/E2E/_workitems?_a=edit&id="
        urlarmada = url + ticket

        driver.get(urlarmada)
        driver.implicitly_wait(8)
        attachment = "ui-id-7"
        driver.find_element_by_id(attachment).click()

        direarchivo= dir_inicial + nombre_archivo

        driver.implicitly_wait(5)
        driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/form/input[1]").send_keys(direarchivo)
        driver.implicitly_wait(5)
        driver.find_element_by_xpath("/html/body/div[4]/div[3]/div/button[1]").click()
        driver.implicitly_wait(5)

        driver.implicitly_wait(5)
        driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/div[2]/div/div[3]/div[4]/div[2]/div/div[2]/div[1]/ul/li[2]").click()
    
    shutil.move(os.path.join(adjuntos, nombre_archivo), os.path.join(ok, nombre_archivo))
        