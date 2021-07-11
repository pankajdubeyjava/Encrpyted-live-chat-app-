import sys
import socket
import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, qApp
from PyQt5.sip import enableautoconversion
from cryptography.fernet import Fernet
from PyQt5.uic import loadUi
import json
s=socket.socket()
h="127.0.0.1"
s.connect((h,8888))

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.gotocreate)

    def loginfunction(self):
        msg="login"
        s.send(msg.encode())
        data={"email":self.email.text(),"password":self.password.text()}
        data= json.dumps(data)
        s.sendall(data.encode())
        incoming_msg=s.recv(1024)
        incoming_msg=incoming_msg.decode()
        if incoming_msg=="Yes":
            self.newwindow()
        else:
            QMessageBox.information(None, "Warning ! ", " Wrong password") 

    def gotocreate(self):
        createacc= CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def newwindow(self):
        createacc= chatwindow()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)

class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc,self).__init__()
        loadUi("createacc.ui",self)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)

    def createaccfunction(self):
        msg="creataccount"
        s.send(msg.encode())
        data={"email":self.email.text(),"password":self.password.text()}
        if self.password.text()==self.confirmpass.text():
            data= json.dumps(data)
            s.sendall(data.encode())
            self.newwindow()  
        else:
             QMessageBox.information(None, "Warning ! ", " passowrd not match")
    def newwindow(self):
        createacc= Login()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)

class chatwindow(QDialog):
    def __init__(self):
        super(chatwindow,self).__init__()
        loadUi("chatwindow.ui",self)
        self.sendbutton.clicked.connect(self.sendfunction)
        
    def sendfunction(self):
        key = Fernet.generate_key()
        f = Fernet(key)
        self.msgbox.addItem("You :  >>"+self.wrmsg.text())
        t=f.encrypt(bytes(self.wrmsg.text(), 'utf-8')) 
        s.send(t)
        s.send(key)
        self.wrmsg.setText("")
        qApp.processEvents()
        incoming_msg=s.recv(1024)
        key=s.recv(1024)
        f = Fernet(key)
        incoming_msg=f.decrypt(incoming_msg) 
        self.msgbox.addItem("server :->"+ incoming_msg.decode())
        qApp.processEvents()
       	
                  
app=QApplication(sys.argv)
mainwindow=Login()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(1050)
widget.setFixedHeight(900)
widget.show()
app.exec_()
s.close()