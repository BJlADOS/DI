-- Создание таблицы Authors
CREATE TABLE Authors (
    author_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    country TEXT
);

-- Создание таблицы Books
CREATE TABLE Books (
    book_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author_id INTEGER,
    price REAL,
    stock INTEGER,
    FOREIGN KEY (author_id) REFERENCES Authors (author_id)
);

-- Создание таблицы Sales
CREATE TABLE Sales (
    sale_id INTEGER PRIMARY KEY,
    book_id INTEGER,
    sale_date TEXT,
    quantity INTEGER,
    FOREIGN KEY (book_id) REFERENCES Books (book_id)
);
