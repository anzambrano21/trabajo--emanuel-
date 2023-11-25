import sys
from PyQt5 import  uic
from PyQt5.QtCore import Qt,QDate
from PyQt5.QtWidgets import QMainWindow,QApplication,QTableWidget,QTableWidgetItem
import mysql.connector
from PyQt5 import QtWidgets

class conecxion:
    def __init__(self):
        self.conexion=mysql.connector.connect(user='root',password='',host='localhost',database='seniat2023',port='3306')
    

class contador(QMainWindow):
    def __init__(self):
        self.con=conecxion()
        super().__init__()
        uic.loadUi("lapiz.ui",self)
        self.tableWidget_2.selectionModel().selectionChanged.connect(self.fila_seleccionada)     
        self.cartablaliCom()
        self.ban=None
        #una lista de los objeto qt de libro de compra
        self.licom=[self.numFac,self.conFac,self.DocAfec,self.dateEdit_3,self.dateEdit_4,self.Rif,self.Cliente,self.montoIncli,self.exten,self.baseIm,self.ISVimpor,self.basenacio,self.ISVnacio,self.comboBox_4,self.comboBox_5,self.comboBox_6]
    def keyPressEvent(self,event):
        if event.key()==Qt.Key_Return:
            for i in range(len(self.licom)):
                if self.licom[i].hasFocus():
                    # Si es el último QTextEdit en la lista, mueve el foco al primero
                    if i == len(self.licom) - 1:
                        self.guardar()
                    else:
                    # De lo contrario, mueve el foco al siguiente QTextEdit
                        self.licom[i+1].setFocus()
                    break
             
    def cosedatlicom(self):
        vec=[]
        for i in range(len(self.licom)):
            if(isinstance(self.licom[i],QtWidgets.QLineEdit)):
                vec.append(self.licom[i].text())
            elif isinstance(self.licom[i],QtWidgets.QDateEdit):
                dat=self.licom[i].date()
                vec.append(dat.toPyDate())
                print(vec[i])
            elif isinstance(self.licom[i],QtWidgets.QComboBox):
                vec.append(self.licom[i].currentText())
        return vec
    def guardar(self):
        # Crear un cursor
        cursor = self.con.conexion.cursor()
        datos=self.cosedatlicom()
        if(self.ban is None):
            query = "INSERT INTO libcom (numfactur, controlFac, docafectado,fechafactur,fechafactura,Rif,cliente,montoimputotal,exentas,baseimportacion,impuimportacion,basenacional,ISVnacional,facPolar,documento,impunacional) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s)"
            cursor.execute(query, datos)
            # Confirmar la transacción
            self.con.conexion.commit()
        else:
            self.ban=(int(float(self.ban)))
            query = "UPDATE  libcom SET numfactur=%s, controlFac=%s, docafectado=%s,fechafactur=%s,fechafactura=%s,Rif=%s,cliente=%s,montoimputotal=%s,exentas=%s,baseimportacion=%s,impuimportacion=%s,basenacional=%s,ISVnacional=%s,facPolar=%s,documento=%s,impunacional=%s  WHERE "+str(self.ban)+"=id"
            cursor.execute(query, datos)
            # Confirmar la transacción
            self.con.conexion.commit()
        self.cartablaliCom()
        self.liplicom()
    def cartablaliCom(self):
        self.tabla=self.findChild(QTableWidget, 'tableWidget_2') 
        cursor =self.con.conexion.cursor()
        cursor.execute("SELECT id,numfactur,docafectado,fechafactur,fechafactura,rif,proveedor,montoimputotal,exentas,baseimportacion,impuimportacion,basenacional,impunacional,usuario,pornacional,porimportacion,poreten,comproreten,fecharetencion,facPolar,fechafactura FROM libcom")
        
        results = cursor.fetchall()
        
        self.tabla.setRowCount(len(results))
        self.tabla.setColumnCount(len(results[0]))
        for i, row in enumerate(results):
            for j, item in enumerate(row):
                self.tabla.setItem(i, j, QTableWidgetItem(str(item)))
    def fila_seleccionada(self):
        rows = self.tableWidget_2.currentRow()
        item = self.tableWidget_2.item(rows, 0).text()
        self.ban=item
        cursor =self.con.conexion.cursor()
        cursor.execute("SELECT numfactur,controlFac,docafectado,DATE(fechafactur),DATE(fechafactura),Rif,cliente,montoimputotal,exentas,baseimportacion,impuimportacion,basenacional,ISVnacional,facPolar,documento,impunacional FROM libcom WHERE "+str(item)+"=id")
        results = cursor.fetchall()
        
        for i in range(len(self.licom)):
            
            if(isinstance(self.licom[i],QtWidgets.QLineEdit)):
                self.licom[i].setText(str(results[0][i]))
            elif isinstance(self.licom[i],QtWidgets.QDateEdit):
                date = QDate(results[0][i])
                self.licom[i].setDate(date)
            elif isinstance(self.licom[i],QtWidgets.QComboBox):
                 if isinstance(results[0][i], float):
                    res=int(results[0][i])
                    self.licom[i].setCurrentText(str(res))
                    break
                 
                 self.licom[i].setCurrentText(str(results[0][i]))
    def liplicom(self):
        for i in range(len(self.licom)):
            if(isinstance(self.licom[i],QtWidgets.QLineEdit)):
                self.licom[i].setText("")
        self.ban=None

app=QApplication(sys.argv)
GUI=contador()
GUI.show()
sys.exit(app.exec_())