import sys
from PyQt5 import  uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow,QApplication
import mysql.connector

class conecxion:
    def __init__(self):
        conexion=mysql.connector.connect(user='root',password='',host='localhost',database='seniat2023',port='3306')
        

class contador(QMainWindow):
    def __init__(self):
        self.con=conecxion()
        self.ban=False
        super().__init__()
        uic.loadUi("lapiz.ui",self)
        #una lista de los objeto qt de libro de compra
        self.licom=[self.numFac,self.conFac,self.DocAfec,self.dateEdit_3,self.dateEdit_4,self.Rif,self.Cliente,self.montoIncli,self.exten,self.baseIm,self.ISVimpor,self.basenacio,self.ISVnacio,self.lineEdit_14,self.comboBox_4,self.comboBox_5,self.comboBox_6]
    def keyPressEvent(self,event):
        if event.key()==Qt.Key_Return:
            for i in range(len(self.licom)):
                if self.licom[i].hasFocus():
                    # Si es el último QTextEdit en la lista, mueve el foco al primero
                    if i == len(self.licom) - 1:
                        self.licom[0].setFocus()
                    else:
                     
                    # De lo contrario, mueve el foco al siguiente QTextEdit
                        self.licom[i+1].setFocus()

                    break
    def cosedat(self):
        vec=[]
        for i in range(len(self.licom)):
            vec.append(self.licom[i].text())
        return vec
    def guardar(self):
        # Crear un cursor
        cursor = self.con.cursor()
        datos=self.cosedat()
        query = "INSERT INTO libcom (numfactur, columna2, columna3,,fechafactur,Rif,cliente,,,baseimportacion,,basenacional) VALUES (%s, %s, %s)"
        cursor.execute(query, datos)

        # Confirmar la transacción
        self.con.commit()
        # Cerrar la conexión
        self.con.close()


app=QApplication(sys.argv)
GUI=contador()
GUI.show()
sys.exit(app.exec_())