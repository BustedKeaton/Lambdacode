from os import walk
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

class CheckSauv:
    """Vérifie que les sauvegardes des sites web se sont bien déroulées"""

    def __init__(self):
        """Initialise le chaîne contenant la synthèse de sauvegardes"""
        
        self.CheckMess = "" #La synthèse

    def runCheck(self):
        """Lance la vérification"""

        tree = walk("C:\sauvegarde_sql_crest_ensae")
        
        self.resList = []
        
        for root,dirs,files in tree:
            self.resList.append(files) #resList[5] : sauvegardes Crest

        todayString = str(date.today()) #date du jour
        #todayString = "2010-01-04" #Je triche pour tester
                
        self.CheckMess += "SAUVEGARDES DU %s\n" %todayString

        #Solution bourrine, à optimiser
        #CREST
        test = 0
        for files in self.resList[5]:
            if todayString in files:
                s = "Sauvegarde Crest | FICHIER : %s \n" %files
                self.CheckMess += s
                test = 1
        if test == 0:
            self.CheckMess += "Aucune sauvegarde pour ce jour. \n"

        #ENSAE
        test = 0
        for files in self.resList[7]:
            if todayString in files:
                s = "Sauvegarde Ensae | FICHIER : %s \n" %files
                self.CheckMess += s
                test = 1
        if test == 0:
            self.CheckMess += "Aucune sauvegarde pour ce jour. \n"

        #ENSAEENGLISH
        test = 0
        for files in self.resList[8]:
            if todayString in files:
                s = "Sauvegarde EnsaeEnglish | FICHIER : %s \n" %files
                self.CheckMess += s
                test = 1
        if test == 0:
            self.CheckMess += "Aucune sauvegarde pour ce jour. \n"

        #LECEPE
        test = 0
        for files in self.resList[9]:
            if todayString in files:
                s = "Sauvegarde Lecepe | FICHIER : %s \n" %files
                self.CheckMess += s
                test = 1
        if test == 0:
            self.CheckMess += "Aucune sauvegarde pour ce jour. \n"

    def sendEmail(self):
        """Envoit le mail de synthèse"""

        serverName = "hermes.ensae.fr"
        port = 25
        sender = "service.informatique@ensae.fr"
        recipient = "romain.tailhurat@ensae.fr"
        
        #Création du message
        
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = "FORWEB : Verification des sauvegardes des sites web" #Attention encodage
        msg.attach(MIMEText(self.CheckMess))

        serverConn = smtplib.SMTP(serverName,port)
        serverConn.ehlo()
        serverConn.sendmail(sender,recipient,str(msg))
        
        
if __name__ == "__main__":
    check = CheckSauv()
    check.runCheck()
    check.sendEmail()
        
