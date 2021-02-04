import tkinter as tk
from tkinter.ttk import *
from tkinter import filedialog
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.options import Options
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge
import os
import glob
import os.path
import sys
# import time
# import winreg
# from keyboard._mouse_event import HORIZONTAL
# import pyautogui as robot
# from win32console import BACKGROUND_BLUE
# from tkinter import messagebox as MessageBox


class E2e():
    def __init__(self):
        self.dato = "hola"


class Aplicacion():
    def __init__(self):
        self.ventana1=tk.Tk()
        self.ventana1.title('TFS')      
        self.ventana1.geometry('270x250')
        #self.ventana1.iconbitmap('C:\\Users\\JorgeDanielGarcia\\Desktop\\Descarga.ico\\')
        self.label1=tk.Label(self.ventana1,text="Ticket:")
        self.label1.grid(column=0, row=0,)
        self.dato1=tk.IntVar()
        self.entry1=tk.Entry(self.ventana1, width=30, textvariable=self.dato1)
        self.entry1.grid(column=1, row=0)
        self.entry1.insert(0, "123456")
        self.label2=tk.Label(self.ventana1,text="Carpeta:")
        self.label2.grid(column=0, row=1)
        self.dato2=tk.StringVar()
        self.entry2=tk.Entry(self.ventana1, width=30, textvariable=self.dato2)
        self.entry2.grid(column=1, row=1)

        radioGroup = LabelFrame(self.ventana1, text = "Seleccionar modo de ejecucion")
        radioGroup.grid(column=0, row=4 , columnspan = 5 , pady = 2)
        self.seleccion=tk.IntVar()
        self.radio1=tk.Radiobutton(radioGroup,text="Background",  variable=self.seleccion, value=1)
        self.radio1.grid(column=0, row=2)
        self.radio2=tk.Radiobutton(radioGroup,text="Online", variable=self.seleccion, value=2)
        self.radio2.grid(column=1, row=2)
        self.boton1=tk.Button(self.ventana1, text="Upload", command=self.upload)
        self.boton1.grid(column=1, row=10)
        # self.boton1.config(bg='white')
        self.boton2=tk.Button(self.ventana1, text=" /\ ",command=self.directory)
        self.boton2.grid(column=5, row=1)
        # self.boton2.config(bg='white')
        # self.ventana1.config(bg='light grey')
        self.ventana1.mainloop()
        
    def directory(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.folder_selected = filedialog.askdirectory()
        buscar = "/" 
        reemplazar = "\\"
        carpeta = self.folder_selected.replace(buscar,reemplazar)
        carpeta2 = carpeta + reemplazar
        self.entry2.insert(0, carpeta2)
        print(carpeta2)
        
    def validacion1(self):
        ticket= self.dato1.get() # ticket
        dire = self.dato2.get()  # dire
        print (ticket)
        print (dire)
        # cantdocs=len(glob.glob(dire + "*"))
        # validacion cant de documentos, si no hay documentos en la carpeta, error
        try:
            os.listdir(dire)
            error = 0
            cantdocs=len(glob.glob(dire + "*"))
        except Exception as e:
            print(e)
            error = 1
        if error == 0:
            if cantdocs == 0:
                self.label4=tk.Label(self.ventana1,text= "No hay docs en la carpeta")
                self.label4.grid(column=1, row=15)
                error = 1
        return error

    def accesotfs(self, ruta, dire):
        # self.robot = robot
        ticket1 = str(self.dato1.get())
        #self.chrome_options = Options()
        #if self.seleccion.get()==1:
            #self.chrome_options.add_argument("--headless")
        # self.driver = webdriver.Chrome(executable_path=r"C:\Google\chromedriver")
        # self.driver = webdriver.Edge(executable_path=r"C:\Google\msedgedriver")
        self.edge_option = EdgeOptions()
        self.edge_option.add_argument("hide_console")
        # options.add_argument = ["hide_console"]
        # self.driver = webdriver.Edge(options)
        # self.driver = webdriver.Edge("C:\Google\msedgedriver", options=self.edge_option)
        self.driver = Edge("C:\Google\msedgedriver", service_args= ["hide_console"])
        url = "http://10.1.27.11:8080/tfs/TFSYPF/E2E/_workitems?_a=edit&id="
        urlarmada = url + ticket1
        # Conectarse
        self.driver.get(urlarmada)
        self.driver.implicitly_wait(8)
        # self.robot.typewrite("SE33439")
        # time.sleep(1)
        # self.robot.press('tab')
        # time.sleep(1)
        # robot.typewrite("Homeroibm2020-")
        # time.sleep(1)
        # self.robot.press('tab')
        # time.sleep(1)
        # self.robot.press('enter')
        # time.sleep(4)
        # dirigirse hacia el modulo attachment
        self.attachment = "ui-id-7"
        self.driver.find_element_by_id(self.attachment).click()
        # boton agregar adjuntos
        # time.sleep(1)
        self.driver.implicitly_wait(5)
        for i in ruta:
            nombre_archivo = i
            direarchivo= dire + nombre_archivo
            self.driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/div[2]/div/div[3]/div[4]/div[2]/div/div[2]/div[2]/table/tbody/tr[5]/td/table/tbody/tr/td[2]/table/tbody/tr/td/div/div[3]/table/tbody/tr/td/div/ul/li[2]").click()
            # time.sleep(1)
            # boton seleccionar archivo
            self.driver.implicitly_wait(5)
            self.driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/form/input[1]").send_keys(direarchivo)
            # time.sleep(1)
            # boton aceptar
            self.driver.implicitly_wait(5)
            self.driver.find_element_by_xpath("/html/body/div[4]/div[3]/div/button[1]").click()
            # time.sleep(1)
            # boton guardar
            self.driver.implicitly_wait(5)
        
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/div[2]/div/div[3]/div[4]/div[2]/div/div[2]/div[1]/ul/li[2]").click()
        
        
            
    def upload(self):
        if self.seleccion.get()==1 or self.seleccion.get()==2:
            resul = self.validacion1()
            if resul == 0:
                print ("todo ok")
                # self.label3=tk.Label(self.ventana1,text= cantdocs)
                # self.label3.grid(column=0, row=6)
                # self.label4=tk.Label(self.ventana1,text= "docs en Direccion indicada")
                # self.label4.grid(column=1, row=6)
                # self.label5=tk.Label(self.ventana1,text= cantdocs)
                # self.label5.grid(column=0, row=7)
                # self.label6=tk.Label(self.ventana1,text= "docs subidos a TFS")
                # self.label6.grid(column=1, row=7)
                # self.popup()
            
            dire = self.dato2.get()  # dire
            # validacion si algun archivo pesa mas de 4mb -  #4.194.304 si es mayor a este numero, entonces pesa mas de 4mb el archivo
            ruta = os.listdir(dire)
            print(ruta)
            for i in ruta:
                nombre_archivo = i
                direarchivo= dire + nombre_archivo
                sizefile = os.stat(direarchivo).st_size
                print(direarchivo, "--- este archivo pesa", sizefile , "bytes")
            # validacion existencia de usuario y contrasena 
            #keyQ = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment', 0, winreg.KEY_QUERY_VALUE)
            #try:
            #    usuario = winreg.QueryValueEx(keyQ, "UsuarioE2E")
            #    contrasena = winreg.QueryValueEx(keyQ, "PassE2E")
            #    error = 0
            #except Exception as e:
            #    print(e)
            #   error = 1
            
            #if error == 1:
            #    print("No existe usuario o contrasena")
                
            #if error == 0:
            #    print("todo bien")
            #    print(usuario[0])
            #    print(contrasena[0])
            
            #armado de ruta para acceder a TFS
            
            #if ruta:
            conectar = self.accesotfs(ruta, dire)


#ce2e = E2e()
if __name__ == "__main__":
    aplicacion1=Aplicacion()   #se le puede pasar un objeto como parametro