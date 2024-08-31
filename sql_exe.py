from sql_queries import *
import datetime
import time
altn = "\n \n \n \n"
#funkcie pre connection
db = get_db()
def create_tables(tbls:list):
            for tbl in tbls:
                db.execute(tbl)
                db.commit()
# def insert_users_f(username,first_name,surname,password,DOB):
#             db.execute(insert_users_Q,(username,first_name,surname,password,DOB))
#             db.commit()
def truncate_t():
            db.execute(delete_content)
            db.commit()
def login_f(name:str,password:str):
            return db.execute(check_login,(name,password)).fetchone()
            

def list_books_f(): 
            return db.execute(return_books_selection).fetchall()
            
        
# def insert_book_f(Name,Author,Published,Genre):
#     try:
#         cur = connection.db()
#         cur.execute(insert_book_Q,(Name,Author,Published,Genre))
#         connection.commit()
#         cur.close()        
#         # connection.close()        

#     except psycopg2.errors.UniqueViolation:
#         cur.execute("ROLLBACK")
#         db = connection.db()
#         db.execute(update_amount_Q,(Name,))
#         connection.commit()
#         db.close()
#         # connection.close()  
def insert_existing_book_f(id): 
            db.execute("select amount from books where id = %s",(id,))
            if db.fetchone() != None:
                db.execute(update_amount_return_Q,(id,))
                db.commit()
                print(altn)
                print("---------------------------------------------")
                print("Book was added!")
            else:
                print(altn)
                print("---------------------------------------------")
                print("Probably wrong ID!")



             


def returnBookID_f(username_id):
            return db.execute(returnBooksID,(username_id,)).fetchall()
            
        
def returnReturnedBooks_f(username_id):
            return db.execute(returnReturnedBooks_Q,(username_id,)).fetchall()
             

