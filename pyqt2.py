from pyqt import *
from sql_exe import *
from psycopg2 import errors
# from table_inputs_handler import *
#zmena
class returnIsNone(Exception):
    pass

class ConReturnNo(Exception):
     pass

class Login(MainWindow):
       
    def __init__(self):
        super().__init__()
        create_tables(CT)
    def pause(self,time,setL1):
        QTimer.singleShot(time, self.loop.quit)
        self.loop.exec()
        
        if setL1 == 1:
            self.label1.setText("") 

    def clickLogin(self):
        self.lgn = login_f(self.inputLine1.text(),self.inputLine2.text())
        if self.lgn != None and self.lgn[6] == 1:
            self.adminPage()
        elif self.lgn != None:
            self.login_page()
        else:
            self.label1.setText("Invalid username or password, try again!")
            self.layout.addWidget(self.label1)
            self.setLayout(self.layout)
            
    def logout(self):
        self.lgn = None
        self.main_page()

    def borrowB(self):   
        
        try:
            self.borrow_book_f(self.lgn[0],int(self.comboBox1.currentItem().text().partition(".")[0]))
        except AttributeError:
            self.label1.setText("Select one of the books!")
        self.pause(1000,1)

    def returnB(self):
        try:
            self.return_book_f(self.comboBox2.currentItem().text().partition("ID:")[2],int(self.comboBox2.currentItem().text().partition(".")[0]),self.lgn[0])
            self.comboBox2.clear()
            if (books := returnBookID_f(self.lgn[0])) != []:

                for book in books:
                    self.comboBox2.addItem(f"{book[0]}. {book[1]}, {book[2]} ID:{book[6]}")
        except AttributeError:
            self.label1.setText("Please select a book to be removed!")

    def checkEmptines(self,*args):
        for item in args:
            if  item == "":
                   return False
        else:
            return True
            
    def insertB(self): 
        try:
            if self.checkEmptines(self.inputLine1.text(),self.inputLine2.text(),(self.inputLine3.text().strip()),self.inputLine4.text()) == False:
                raise ValueError
        except ValueError:
             self.label1.setText("Wrong input")
             self.pause(2000,1)
        else:
            self.insert_book_f(self.inputLine1.text(),self.inputLine2.text(),self.inputLine3.text(),self.inputLine4.text())
            self.pause(1000,1)
        

        
    def removeB(self): 

        try: 
            self.confirmP("Are you sure?",ConReturnNo)
            if self.remove_book_f(self.comboBox1.currentItem().text().partition(".")[0]) == None:
                raise returnIsNone
            
            self.label1.setText("Book was removed")
            db.commit()
            self.comboBox1.clear() 
            for book in list_books_f():
                self.comboBox1.addItem(f"{book[0]}. {book[1]}, {book[2]}")
            self.pause(1000,1)
        except returnIsNone:
            self.label1.setText("The book is still borrowed, return before deletion from DB!")
            self.pause(2000,1)
        except AttributeError:
            self.label1.setText("Select a book!")
            self.pause(1000,1)
        except ConReturnNo:
                pass  

    def setB(self):
        try:    
            self.set_book_f(int(self.inputLine1.text()),self.comboBox1.currentItem().text().partition(".")[0])
        except AttributeError:
            self.label1.setText("Please select a book.")
        except ValueError:
            self.label1.setText("Did not select a book or Invalid amount input.")


    def clickSignIn(self):
        try:
            if self.checkEmptines(self.inputLine1.text().strip(),self.inputLine2.text().strip(),self.inputLine3.text().strip(),self.inputLine4.text().strip(),self.inputLine5.text().strip()) == False:
                raise ValueError  
        except ValueError:
            self.label1.setText("Empty field!")
            self.pause(1000,1)
        else: 
            self.insert_users_f(self.inputLine1.text().strip(),self.inputLine2.text().strip(),self.inputLine3.text().strip(),self.inputLine4.text().strip(),(self.inputLine5.text().strip()))

    def removeU(self):
        print(self.comboBox1.currentItem().text())
        try:
            if db.execute(removeUser,(self.comboBox1.currentItem().text(),)).fetchone() == None:
                raise returnIsNone
            db.commit()
        except AttributeError:
            self.label1.setText("Select a User") 
        except returnIsNone:
            self.label1.setText("The user has a book still borrowed")
            self.pause(2000,1)
        users = db.execute("select UserName from users").fetchall()
        self.comboBox1.clear() 
        for user in users:
            self.comboBox1.addItem(user[0])
    def borrow_book_f(self,username_id,book_id): 
                
                try:
                    self.confirmP("Are you sure?",ConReturnNo)
                    db.execute(borrow_book_Q,(username_id,book_id,datetime.date.today()))
                    db.execute(update_amount_minus_Q,(book_id,))
                    
                    db.commit()
                    self.label1.setText("Book borrowed!")

                except sqlite3.IntegrityError:
                    self.label1.setText("Book is not available")
                except ConReturnNo:
                     pass
        
    def return_book_f(self,id,book_id,username_id): 
                var = db.execute(f"select * from borrowings where book_id = {book_id} and username_id = {username_id}").fetchall()
                try:
                    if var != []:
                        self.confirmP("Are you sure?",ConReturnNo)
                        db.execute(return_book_Q,(id,book_id,username_id))
                        db.execute(update_amount_return_Q,(book_id,)) 
                        
                        db.commit() 
                        self.label1.setText("Book returned")
                        self.pause(1000,1)
                    else:
                        self.label1.setText("Book was not returned")
                except ConReturnNo:
                     print("error")
                     pass

    def insert_book_f(self,book_name,author,published,genre): 
                try:
                    db.execute(insert_book_Q,(book_name,author,datetime.datetime.strptime((published.strip()),r"%d.%m.%Y"),genre))
                # db.execute(update_amount_Q,(book_name,))
                    db.commit()
                    self.label1.setText("Book inserted!")
                    self.clearJinput(self.inputLine1,self.inputLine2,self.inputLine3,self.inputLine4)
                except ValueError:
                    self.label1.setText("Wrong date format, try again")
                    self.pause(1000,1)
                except sqlite3.IntegrityError:
                    self.label1.setText("Username already in use")
                    self.pause(1000,1)
                try: 
                        id = db.execute("select id from books where name = ?",(book_name,)).fetchone()
                        print(id)
                        db.execute(insert_book_Qarchive,(id[0],book_name,author,published,genre))
                        db.commit()
                except sqlite3.IntegrityError:
                    print("books archive")
                    pass
                except TypeError:
                     pass
                
    def set_book_f(self,amount,id): 
            try:
                db.execute(set_book_Q,(amount,id))
                db.commit()
                self.label1.setText("Amount was set")  
                self.clearJinput(self.inputLine1)
            except sqlite3.IntegrityError:
                self.label1.setText("Only positive values")
                self.pause(1000,1)
    def insert_users_f(self,username,first_name,surname,password,DOB):
        try:
            db.execute(insert_users_Q,(username,first_name,surname,password,datetime.datetime.strptime((DOB),r"%d.%m.%Y")))
            db.commit()
            self.clearJinput(self.inputLine1,self.inputLine2,self.inputLine3,self.inputLine4,self.inputLine5)
            self.label1.setText("Successfull sign in!")
            self.pause(1000,1)
            
        except sqlite3.IntegrityError:
            self.label1.setText("Username already in use")
            self.pause(1000,1)
        except ValueError:
            self.label1.setText("Wrong date format, try again")
            self.pause(1000,1)
    def remove_book_f(self,id): 
           
                
        return db.execute(remove_book_Q,(id,)).fetchone()   
                  
            
       
        
app = QApplication([])

window = Login()

window.main_page()
window.show()

app.exec()