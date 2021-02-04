from jira import JIRA, JIRAError
import os 
import shutil
import urllib3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
import glob
import time


class Jira:
    #constructor para armar el email, pasando el server de correo, pass y correo destino
    def __init__(self,servidor, usuario, password):
        self.servidor = servidor
        self.usuario = usuario
        self.password = password
        
    #metodo conectar
    def conectar(self):
        try:
            jira = JIRA(options = {'server': self.servidor,'verify': False}, basic_auth=(self.usuario, self.password))
            return True, jira
        except JIRAError as e:
            if e.status_code == 401:
                return False, e.status_code
            
class Email:
    #constructor para armar el email, pasando el server de correo, pass y correo destino
    def __init__(self,email_from, email_pass, email_to):
        self.email_from = email_from
        self.email_pass = email_pass
        self.email_to = email_to
    
    #metodo envio
    def envio(self,mensaje):
        msg = MIMEMultipart()
        msg['From'] = self.email_from
        msg['To'] = self.email_to
        msg['Subject'] = "Aviso"
        msg.attach(MIMEText(mensaje, 'plain'))
        try:
            server = smtplib.SMTP('smtp.office365.com', 587)
            server.ehlo()
            server.starttls()
            server.login(self.email_from, self.email_pass)
            text = msg.as_string()
            server.sendmail(self.email_from, self.email_to, text)
            print('email sent')
            server.quit()
            exit
        except:
            print("SMPT server connection error")

#desactivar el warning de certificado no confiable en la conexion al server
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#constantes de direcciones
dir_inicial = "C:\\Jira_Autom\\"
adjuntos = "C:\\Jira_Autom\\Adjuntos\\"
ok = "C:\\Jira_Autom\\ProcesadoOK\\"
error = "C:\\Jira_Autom\\ProcesadoError\\"

#patron de ticket
ticket = "TICKET-"

#obtencion de variables de entorno del usuario
servidor = os.environ['JIRA.SERVIDOR']
usuario = os.environ['JIRA.USUARIO']
password = os.environ['JIRA.PASS']
mail = os.environ['JIRA.CORREO']

#usuario y contrasena de servidor de correo
email_from = "neorisalertajira@outlook.com"
email_pass = "Neoris2020-"

#instancio email
email = Email(email_from, email_pass, mail)
#consulto cuantos documentos hay en la carpeta adjuntos
cantdocs=len(glob.glob(adjuntos + "*"))
#si la cantidad es mayor que 0, me conecto a jira 
if cantdocs > 0:
    #instancio jira
    jira = Jira(servidor, usuario, password)
    conexion, jira = jira.conectar()
    if conexion is True:
        ruta = os.listdir(adjuntos)
        for i in ruta:
            nombre_archivo = i
            pos = nombre_archivo.find(ticket)
            #pos > - 1 = a archivo con numero de ticket
            if pos > -1:
                #Obtengo el numero de ticket y lo guardo en nticket - el formato de ticket es: TICKET-XXXXXX
                nticket = nombre_archivo[pos:pos+13]
                #armo la direccion del archivo a adjuntar
                dirarchivo = adjuntos + nombre_archivo
                try:
                    jira.add_attachment(issue=nticket, attachment=dirarchivo)
                    #muevo el archivo a la carpeta ProcesadosOK
                    shutil.move(os.path.join(adjuntos, nombre_archivo), os.path.join(ok, nombre_archivo))
                    print("Se adjunto el archivo:", nombre_archivo)
                    
                except JIRAError as e:
                    email.envio('No se pudo adjuntar documento, el ticket no existe en Jira, quitar de la carpeta Adjuntos el documento : {}'.format(nombre_archivo))
                    #muevo el archivo a la carpeta Error para que no siga enviando mails en la otra ejecucion

            else: 
                    #trato los adjuntos que no tienen numero de ticket 
                    #se envia archivo a carpeta ProcesadoError
                    print("No se adjunto el archivo:", nombre_archivo)
                    shutil.move(os.path.join(adjuntos, nombre_archivo), os.path.join(error, nombre_archivo))
                    
    else:
        email.envio("No se logro conexion a Jira favor de verificar en sus variables de entorno: Jira.Servidor, Jira.Usuario , Jira.Contrasena")

else:
    exit
