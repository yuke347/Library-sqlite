import psycopg2
import socket
import sqlite3
import datetime
#check the name of the PC
def get_db():
    db = sqlite3.connect("../instance/db_inst.sqlite")
    return db
def init_db():

    db = get_db()
    with open("init_db/init_tables.sql") as f:
        db.executescript(f.read())

#tables creation
CT =["""create table if not exists books(
        ID serial primary key,
        Name text,
        Author text,
        Published date,
        Genre text,
        amount int default 0 check(amount>-1),
        Constraint unique_text Unique (Name))
        """,
    """create table if not exists users(
        ID serial primary key,
        UserName text,
        First_name text,
        Surname text,
        Password text,
        DOB Date,
        admin int default 0,
        Constraint unique_name Unique(UserName)
    )""","""create table if not exists borrowings(
            ID serial primary key,
            username_id int,
            book_id int,
            borrow_date date,
            return_date date)""",
            """create table if not exists booksArchive(
            book_id integer,
            Name text,
            Author text,
            Published date,
        Genre text,Constraint unique_book Unique(Name))"""]
# vloženie hodnot
insert_users_Q = """insert into users(username,first_name,surname,password,dob) values(
                    ?,?,?,?,?)"""
insert_book_Q = """insert into books(Name,Author,Published,Genre) values
                    (?,?,?,?)"""
insert_book_Qarchive = """insert into booksArchive(book_id,Name,Author,Published,Genre) values
                    (?,?,?,?,?)"""
borrow_book_Q = """insert into borrowings(username_id,book_id,borrow_date)values(
                    ?,?,?)"""


update_amount_Q = """update books set amount = amount + 1 where name = ?"""
update_amount_minus_Q = """update books set amount = amount - 1 where id = ?"""
update_amount_return_Q = """update books set amount = amount + 1 where id = ?"""

# return queries
check_login = """select * from users where username = ? and password = ?"""
return_books_selection = """select * from books"""
returnBooksID = """select * from books
                    inner join borrowings
                    on books.id = borrowings.book_id
                    where borrowings.username_id = ? and borrowings.return_date is NULL"""
returnReturnedBooks_Q = """select * from booksarchive where book_id in (select book_id from borrowings where username_id = ? and return_date is not NULL)"""


#remove a thing 
delete_content = """truncate table users"""
remove_book_Q = """delete from books 
where books.ID not in (select book_id from borrowings where borrowings.return_date is NULL) and books.ID = ? returning ID"""
return_book_Q = """DELETE FROM borrowings
WHERE ctid IN (
    SELECT ctid
    FROM borrowings
	where book_id = ? and username_id = ?
    ORDER BY id
    LIMIT 1
)"""
return_book_Q = "update borrowings set return_date = current_date where id=? and book_id = ? and username_id= ?"
set_book_Q = "update books set amount = ? where id = ?"
removeUser = "delete from users where UserName = ? and UserName not in(select users.UserName from users inner join borrowings on borrowings.username_id = users.ID where users.UserName = 'dusan' and borrowings.return_date is NULL) returning UserName"






