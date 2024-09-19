import sqlite3
from faker import Faker
import random

# Create a Faker instance
fake = Faker()

# Connect to the SQLite3 database
connection = sqlite3.connect('library.db')
cursor = connection.cursor()

# Create the Book table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Book (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        number_of_pages INTEGER NOT NULL,
        release_date DATE NOT NULL,
        author_id INTEGER,
        FOREIGN KEY (author_id) REFERENCES Author(ID)
    )
''')

# Create the Author table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Author (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        firstname TEXT NOT NULL,
        lastname TEXT NOT NULL,
        birthdate DATE NOT NULL,
        birthplace TEXT NOT NULL
    )
''')

connection.commit()


# Function to insert authors
def insert_authors(num_authors):
    for _ in range(num_authors):
        firstname = fake.first_name()
        lastname = fake.last_name()
        birthdate = fake.date_of_birth().strftime('%d.%m.%Y')
        birthplace = fake.city()

        cursor.execute('''
            INSERT INTO Author (firstname, lastname, birthdate, birthplace)
            VALUES (?, ?, ?, ?)
        ''', (firstname, lastname, birthdate, birthplace))

    connection.commit()


# Function to insert books
def insert_books(num_books):
    cursor.execute("SELECT ID FROM Author")
    author_ids = cursor.fetchall()

    for _ in range(num_books):
        title = fake.sentence(nb_words=4)
        category = random.choice(['Fiction', 'Non-Fiction', 'Sci-Fi', 'Fantasy', 'Mystery', 'Romance', 'History'])
        number_of_pages = random.randint(100, 1200)
        release_date = fake.date_between(start_date='-150y', end_date='now').strftime('%d.%m.%Y')
        author_id = random.choice(author_ids)[0]

        cursor.execute('''
            INSERT INTO Book (title, category, number_of_pages, release_date, author_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, category, number_of_pages, release_date, author_id))

    connection.commit()


# Insert 500 authors and 1000 books into the database
insert_authors(500)
insert_books(1000)

# Close the connection
connection.close()

print("DB is created successfully")
