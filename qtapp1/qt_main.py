from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QThread
import requests
import json
import time


colors = ['#1f3a93', '#26a65b']

class ThreadClass(QThread):
    about_response = QtCore.pyqtSignal(object)

    def __init__(self, url: str):
        super().__init__()

        self.url = url

    def run(self):
        while True:
            try:
                rs = requests.post(self.url)
                self.about_response.emit(rs)

            except Exception as e:
                print('Error:', e)

            finally:
                time.sleep(1)


class MyWindow(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.url_base = 'http://127.0.0.1:5000/'
        self.main_id = 0
        self.res_usr = dict()
        #self.chat_obj = QtWidgets.QListWidget


        url = self.url_base + 'blog/chat'

        self.thread_class = ThreadClass(url)
        self.thread_class.about_response.connect(self.on_response)
        self.thread_class.start()

        self.title = QtWidgets.QLabel('Авторизация')
        self.title.setAlignment(QtCore.Qt.AlignHCenter)

        self.username = QtWidgets.QLineEdit()
        self.username.setPlaceholderText('Введите логин:')
        self.password = QtWidgets.QLineEdit()
        self.password.setPlaceholderText('Введите пароль:'),
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.btnLogin = QtWidgets.QPushButton("&OK")

        self.lnkReg = QtWidgets.QPushButton('&Регистрация')

        self.chat_obj = QtWidgets.QListWidget()

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.title)
        self.vbox.addWidget(self.username)
        self.vbox.addWidget(self.password)
        self.vbox.addWidget(self.btnLogin)
        self.vbox.addWidget(self.lnkReg)
        #self.vbox.addWidget(self.chat_obj)

        self.setLayout(self.vbox)
        self.btnLogin.clicked.connect(self.authorisation)
        self.lnkReg.clicked.connect(self.switchToRegistration)

    def on_response(self, rs):
        #print('on_response:', rs.text)
        #return rs
        res_u = rs.text
        res_pst = json.loads(res_u)
        #res_pst = rs.json()
        #print(res_pst)

        #self.chat_obj = QtWidgets.QListWidget(self)
        self.chat_obj.clear()
        for key, value in res_pst.items():

            item = QtWidgets.QListWidgetItem(self.chat_obj)
            item.setText(value[0] + ': ' + value[1])
            if value[2] == self.main_id:
                item.setTextAlignment(QtCore.Qt.AlignRight)
                item.setForeground(QtGui.QColor(colors[0]))
            else:
                item.setTextAlignment(QtCore.Qt.AlignLeft)
                item.setForeground(QtGui.QColor(colors[1]))

            #self.chat_obj.addItem(value[0] + ': ' + value[1])



    def getChat(self):
        window.resize(300, 400)
        self.clearLayout(self.vbox)

        self.label = QtWidgets.QLabel('Чат')
        self.label.setAlignment(QtCore.Qt.AlignHCenter)
        self.vbox.addWidget(self.label)

        url = self.url_base + 'blog/chat'
        r = requests.post(url)
        #print(r.status_code, r.reason)
        #print(r.request.headers)

        res_u = r.text
        res_pst = json.loads(res_u)
        #print(res_pst)
        #res_pst = r.json()

        #self.chat_obj = QtWidgets.QListWidget(self)
        for key, value in res_pst.items():
            item = QtWidgets.QListWidgetItem(self.chat_obj)
            item.setText(value[0] + ': ' + value[1])
            if value[2] == self.main_id:
                item.setTextAlignment(QtCore.Qt.AlignRight)
                item.setForeground(QtGui.QColor(colors[0]))
            else:
                item.setTextAlignment(QtCore.Qt.AlignLeft)
                item.setForeground(QtGui.QColor(colors[1]))
        #self.chat_obj.addItem(value[0] + ': ' + value[1])

        self.vbox.addWidget(self.chat_obj)

        self.message = QtWidgets.QLineEdit()
        self.message.setPlaceholderText('Введите сообщение')
        self.vbox.addWidget(self.message)

        self.btnSend = QtWidgets.QPushButton("&Отправить")
        self.vbox.addWidget(self.btnSend)
        self.btnSend.clicked.connect(self.sendmessage)


    def switchToRegistration(self):
        """
        Переключение на регистрацию
        """
        window.resize(300, 200)
        self.clearLayout(self.vbox)

        self.title = QtWidgets.QLabel('Регистрация')
        self.title.setAlignment(QtCore.Qt.AlignHCenter)

        self.username = QtWidgets.QLineEdit()
        self.username.setPlaceholderText('Введите логин:')
        self.password = QtWidgets.QLineEdit()
        self.password.setPlaceholderText('Введите пароль:'),
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.btnReg = QtWidgets.QPushButton("&OK")

        self.lnkAutor = QtWidgets.QPushButton('&Авторизация')

        self.vbox.addWidget(self.title)
        self.vbox.addWidget(self.username)
        self.vbox.addWidget(self.password)
        self.vbox.addWidget(self.btnReg)
        self.vbox.addWidget(self.lnkAutor)

        self.setLayout(self.vbox)
        self.btnReg.clicked.connect(self.registration)
        self.lnkAutor.clicked.connect(self.switchToAuthorisation)


    def switchToAuthorisation(self):
        """
        Переключение на авторизацию
        """
        window.resize(300, 200)
        self.clearLayout(self.vbox)

        self.title = QtWidgets.QLabel('Авторизация')
        self.title.setAlignment(QtCore.Qt.AlignHCenter)

        self.username = QtWidgets.QLineEdit()
        self.username.setPlaceholderText('Введите логин:')
        self.password = QtWidgets.QLineEdit()
        self.password.setPlaceholderText('Введите пароль:'),
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.btnAutor = QtWidgets.QPushButton("&OK")

        self.lnkReg = QtWidgets.QPushButton('&Регистрация')

        self.vbox.addWidget(self.title)
        self.vbox.addWidget(self.username)
        self.vbox.addWidget(self.password)
        self.vbox.addWidget(self.btnLogin)
        self.vbox.addWidget(self.lnkReg)

        self.setLayout(self.vbox)
        self.btnAutor.clicked.connect(self.authorisation)
        self.lnkReg.clicked.connect(self.switchToRegistration)


    def authorisation(self):
        """
        Авторизация
        """
        url = self.url_base + 'auth/login'
        data = {'username': self.username.text(), 'password': self.password.text()}
        r = requests.post(url, json=data)

        #print(r.status_code, r.reason)
        #print(r.request.headers)

        res_u = r.text
        #print(res_u)
        res_usr = json.loads(res_u)
        #print(res_usr['status'])
        if res_usr['status'] == 'ok':
            self.main_id = res_usr['id']
            #print(self.main_id)
            self.getChat()
        elif res_usr['status'] == 'no':
            self.showError(res_usr)


    def registration(self):
        """
        Регистрация
        """
        url = self.url_base + 'auth/register'
        data = {'username': self.username.text(), 'password': self.password.text()}
        r = requests.post(url, json=data)

        #print(r.status_code, r.reason)
        #print(r.request.headers)

        res_u = r.text
        #print(res_u)
        res_usr = json.loads(res_u)
        if res_usr['status'] == 'ok':
            self.switchToAuthorisation()
        elif res_usr['status'] == 'no':
            self.showError(res_usr)


    def clearLayout(self, layout):
        """
        Очистка окошка
        """
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)


    def showError(self, res_usr):
        """
        Показать ошибки
        """
        self.label = QtWidgets.QLabel(res_usr['error'])
        self.label.setAlignment(QtCore.Qt.AlignHCenter)
        self.vbox.addWidget(self.label)

    def showSuccess(self, res_usr):
        """
        Показать успех
        """
        self.label = QtWidgets.QLabel(res_usr['success_msg'])
        self.label.setAlignment(QtCore.Qt.AlignHCenter)
        self.vbox.addWidget(self.label)


    def sendmessage(self):
        """
        Отправка сообщения
        """
        print(self.main_id)
        url = self.url_base + 'blog/create/{}'.format(self.main_id)
        data = {'message': self.message.text()}
        #print(data)
        r = requests.post(url, json=data)

        #print(r.status_code, r.reason)
        #print(r.request.headers)

        res_m = r.text
        #print(res_m)
        #res_usr = r.json()
        res_usr = json.loads(res_m)
        if res_usr['status'] == 'ok':
            self.showSuccess(res_usr)
        elif res_usr['status'] == 'no':
            self.showError(res_usr)

        self.message.clear()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle("Простой Мессенжер")
    window.setGeometry(500, 300, 600, 600)
    window.resize(300, 200)
    window.show()
    sys.exit(app.exec_())
