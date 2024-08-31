DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS borrowings;
DROP TABLE IF EXISTS booksArchive;
create table if not exists books(
        ID integer primary key AUTOINCREMENT,
        Name text,
        Author text,
        Published date,
        Genre text,
        amount int default 0 check(amount>-1),
        Constraint unique_text Unique (Name));
create table if not exists users(
        ID integer primary key AUTOINCREMENT,
        UserName text,
        First_name text,
        Surname text,
        Password text,
        DOB date,
        admin int default 0,
        Constraint unique_name Unique(UserName));
create table if not exists borrowings(
            ID integer primary key AUTOINCREMENT,
            username_id int,
            book_id int,
            borrow_date date,
            return_date date);
create table if not exists booksArchive(
            book_id integer,
            Name text,  
            Author text,
            Published date,
        Genre text,Constraint unique_book Unique(Name))        