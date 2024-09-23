from PyQt6.QtWidgets import QApplication, QLabel,QMainWindow,QVBoxLayout,QWidget,QPushButton,QLineEdit,QComboBox,QListWidget,QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QEventLoop,QTimer,Qt


from sql_exe import list_books_f,returnBookID_f,returnReturnedBooks_f,db

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library app")
        self.listB = []
        self.loop = QEventLoop()
        self.msgBox = QMessageBox()
        
        self.layout = QVBoxLayout()
        self.label1 = QLabel(text="")
        self.label2 = QLabel(text="")

        self.new_window= QWidget()

        self.button1 = QPushButton()
        self.button2 = QPushButton()
        self.button3 = QPushButton()
        self.button4 = QPushButton()
        self.button5 = QPushButton()

        self.inputLine1 = QLineEdit()
        
        self.inputLine2 = QLineEdit()
        self.inputLine3 = QLineEdit()
        self.inputLine4 = QLineEdit()
        self.inputLine5 = QLineEdit()

        self.comboBox1 = QListWidget()
        self.comboBox2 = QListWidget()
    def exit(self):
        exit()
    def confirmP(self,text = "",error = None):
        try:
            for i in reversed(range(self.ConfirmW.layout.count())):
                self.ConfirmW.layout.itemAt(i).widget().setParent(None)
        except:
            pass
        answr = self.msgBox.question(self, 'Confirmation', text, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)        
        if answr == QMessageBox.StandardButton.Yes:
            pass
        else:
            raise error
    def clear_layout(self):
        try:
            self.button1.disconnect()
            self.button2.disconnect()
            self.button3.disconnect()
            self.button4.disconnect()
            self.button5.disconnect()
        except:
            pass
        try:
            self.inputLine1.setText("")
            
            self.inputLine2.setText("")
            self.inputLine3.setText("")
            self.inputLine4.setText("")
            self.inputLine5.setText("")

            self.inputLine2.setEchoMode(QLineEdit.EchoMode.Normal)

        except:
            pass
        try:
            self.comboBox1.clear()
            self.comboBox2.clear()
        except:
            pass
        try:
            self.label1.setText("")
            self.label2.setText("")
            self.label1.setFont(QFont('Arial',10))
            self.label2.setFont(QFont('Arial',10))
            self.label2.setAlignment(Qt.AlignmentFlag.AlignJustify)
        except:
            pass
        try:
            for i in reversed(range(self.layout.count())):
                self.layout.itemAt(i).widget().setParent(None)
        except:
            pass
        
    def clearJinput(self,*args):
        for item in args:
            item.setText("")

    def set_layout(self,*args):
        for layout in args:
            self.layout.addWidget(layout)

    def main_page(self):    
        self.clear_layout()

        self.button1.setText("Login")
        self.button2.setText("Sign in")
        self.button3.setText("Exit the app")
        self.button1.clicked.connect(self.loginPrompt)
        self.button2.clicked.connect(self.signInPrompt)
        self.button3.clicked.connect(self.exit)

        self.label2.setText("Welcome to Library 'DS'")

        self.set_layout(self.label2,self.button1,self.button2,self.button3)
        font = self.label2.font()
        font.setPointSize(20)
        self.label2.setFont(font)

        self.setLayout(self.layout)
    def loginPrompt(self):
        self.clear_layout()    

        self.inputLine1.setPlaceholderText("Username")
        self.inputLine2.setPlaceholderText("Password")
        self.inputLine2.setEchoMode(QLineEdit.EchoMode.Password)

        self.button1.setText("Login")
        self.button2.setText("Go Back")
        self.set_layout(self.inputLine1,self.inputLine2,self.button1,self.button2)

        self.setLayout(self.layout)
        self.button1.clicked.connect(self.clickLogin)
        self.button2.clicked.connect(self.main_page)

    def login_page(self):
        self.clear_layout()
        self.label2.setText(f"User Login ({self.lgn[1]})")
        self.button1.setText("Borrow a book")
        self.button2.setText("Return a book")
        self.button4.setText("My books")
        self.button3.setText("Log out")

        font = self.label2.font()
        font.setPointSize(20)
        self.label2.setFont(font) 
        self.label2.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.set_layout(self.label2,self.button1,self.button2,self.button4,self.button3)

        self.button1.clicked.connect(self.borrow_B)
        self.button2.clicked.connect(self.return_B)
        self.button3.clicked.connect(self.main_page)
        self.button4.clicked.connect(self.myBookP)

    def signInPrompt(self):
        self.clear_layout()
        self.button1.setText("Sign in")
        self.button3.setText("Go back")
        self.inputLine1.setPlaceholderText("Username")
        self.inputLine4.setPlaceholderText("Password")  
        self.inputLine2.setPlaceholderText("First name")
        self.inputLine3.setPlaceholderText("Surname")
        self.inputLine5.setPlaceholderText("Day of birth dd.mm.yyyy")
        
        self.set_layout(self.inputLine1,self.inputLine2,self.inputLine3,self.inputLine4,self.inputLine5,self.label1,self.button1,self.button3)    
        self.setLayout(self.layout)
        self.button1.clicked.connect(self.clickSignIn)       
        self.button3.clicked.connect(self.main_page)

    def borrow_B(self):
        self.clear_layout()
        self.button1.setText("Borrow")
        self.button2.setText("Go back to menu")
        for book in list_books_f():
            self.comboBox1.addItem(f"{book[0]}. {book[1]}, {book[2]}")
        
        self.set_layout(self.comboBox1,self.label1,self.button1,self.button2)
        
        self.button1.clicked.connect(self.borrowB)
        self.button2.clicked.connect(self.login_page)

    def return_B(self): 
        self.clear_layout()
        self.button1.setText("Return")
        self.button2.setText("Go back to menu")
        
        if (books := returnBookID_f(self.lgn[0])) != []:

            for book in books:
                self.comboBox2.addItem(f"{book[0]}. {book[1]}, {book[2]} ID: {book[6]}")
            self.set_layout(self.comboBox2,self.button1,self.button2,self.label2)
            self.button1.clicked.connect(self.returnB)
        else:
            self.label1.setText("No borrowed book.")
            self.set_layout(self.label1,self.button2)
            self.setLayout(self.layout)
        self.button2.clicked.connect(self.login_page)

    def myBookP(self):
        self.clear_layout()
        self.label1.setText("Borrowed:")
        self.label2.setText("Returned:")
        self.button1.setText("Go back to menu")
        if (books := returnBookID_f(self.lgn[0])) != []:
            for book in books:
                self.comboBox1.addItem(f"{book[0]}. {book[1]}, {book[2]} ")
                # self.set_layout(self.label1,self.comboBox1,self.label2,self.button1)
                # self.setLayout(self.layout)
        if (books2 := returnReturnedBooks_f(self.lgn[0])) != []:
             for book in books2:
                self.comboBox2.addItem(f"{book[0]}. {book[1]}, {book[2]} ")
        self.set_layout(self.label1,self.comboBox1,self.label2,self.comboBox2,self.button1)
        self.setLayout(self.layout)
        self.button1.clicked.connect(self.login_page)

    def adminPage(self):
        self.clear_layout()
        self.label2.setText("Admin Login")
        self.button1.setText("Insert(Register) a book")
        self.button4.setText("Set book's amount")
        self.button2.setText("Remove a book from Database")
        self.button5.setText("Remove a user from Database")

        self.button3.setText("Log out")

        font = self.label2.font()
        font.setPointSize(20)
        self.label2.setFont(font) 
        self.label2.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.set_layout(self.label2,self.button1,self.button4,self.button2,self.button5,self.button3)
        self.setLayout(self.layout)

        self.button1.clicked.connect(self.insertBookP)
        self.button2.clicked.connect(self.removeBookP)
        self.button3.clicked.connect(self.main_page)
        self.button4.clicked.connect(self.setBamount)
        self.button5.clicked.connect(self.removeUserP)

    def insertBookP(self):
        self.clear_layout()
        self.inputLine1.setPlaceholderText("Book name")
        self.inputLine2.setPlaceholderText("Author")
        self.inputLine3.setPlaceholderText("Published dd.mm.YYYY")
        self.inputLine4.setPlaceholderText("Genre")

        
        self.button1.setText("Insert book")
        self.button2.setText("Go back")
        self.set_layout(self.inputLine1,self.inputLine2,self.inputLine3,self.inputLine4,self.label1,self.button1,self.button2)
        self.setLayout(self.layout)

        self.button1.clicked.connect(self.insertB)
        self.button2.clicked.connect(self.adminPage)

    def removeBookP(self):
        self.clear_layout()
        for book in list_books_f():
            self.comboBox1.addItem(f"{book[0]}. {book[1]}, {book[2]}")
        self.button1.setText("Remove book")
        self.button2.setText("Go back")
        self.set_layout(self.comboBox1,self.label1,self.button1,self.button2)
        self.setLayout(self.layout)
        self.button1.clicked.connect(self.removeB)
        self.button2.clicked.connect(self.adminPage)

    def setBamount(self):
        self.clear_layout()
        for book in list_books_f():
            self.comboBox1.addItem(f"{book[0]}. {book[1]}, {book[2]}")
        self.inputLine1.setPlaceholderText("Amount")
        self.button1.setText("Set amount")
        self.button2.setText("Go back")
        self.set_layout(self.comboBox1,self.inputLine1,self.label1,self.button1,self.button2)
        self.setLayout(self.layout)
        self.button1.clicked.connect(self.setB)
        self.button2.clicked.connect(self.adminPage)
    
    def removeUserP(self):
        self.clear_layout()
        
        users = db.execute("select UserName from users").fetchall()
        for user in users:
            self.comboBox1.addItem(user[0])
        self.button1.setText("Remove user")
        self.button2.setText("Go back")
        self.set_layout(self.comboBox1,self.label1,self.button1,self.button2)
        self.setLayout(self.layout)
        self.button1.clicked.connect(self.removeU)
        self.button2.clicked.connect(self.adminPage)

        




  
    



    

    




