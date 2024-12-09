import sqlite3
import json

conn = sqlite3.connect('bookstore.db')
cursor = conn.cursor()

cursor.execute("""
    SELECT title, price FROM Books
    WHERE price > 500
    ORDER BY title
    LIMIT 3
""")
result1 = cursor.fetchall()

cursor.execute("""
    SELECT COUNT(*) FROM Books
""")
result2 = cursor.fetchone()

cursor.execute("""
    SELECT b.title, SUM(s.quantity) AS total_sold
    FROM Sales s
    JOIN Books b ON s.book_id = b.book_id
    GROUP BY b.title
""")
result3 = cursor.fetchall()

cursor.execute("""
    UPDATE Books
    SET stock = stock - 1
    WHERE book_id = 1
""")

cursor.execute("""
    SELECT title, stock FROM Books
    WHERE stock < 15
""")
result5 = cursor.fetchall()

cursor.execute("""
    SELECT AVG(price) FROM Books
""")
result6 = cursor.fetchone()

results = {
    "expensive_books": result1,
    "total_books": result2[0],
    "sales_by_book": result3,
    "low_stock_books": result5,
    "average_price": result6[0]
}

with open('results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=4, ensure_ascii=False)

conn.commit()
conn.close()
