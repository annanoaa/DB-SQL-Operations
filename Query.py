import sqlite3

# Connect to the SQLite3 database
connection = sqlite3.connect('library.db')
cursor = connection.cursor()


def books_with_max_pages():
    # Query to fetch books with the maximum number of pages
    cursor.execute('''
        SELECT * FROM Book
        WHERE number_of_pages = (
            SELECT MAX(number_of_pages) FROM Book
        );
    ''')

    # Fetch and print the results
    books = cursor.fetchall()
    print("Books with max pages:")
    for book in books:
        print(book)


def avg_number_of_pages():
    # Query to calculate the average number of pages
    cursor.execute('''SELECT AVG(number_of_pages) AS average_pages FROM Book;''')

    # Fetch and print the result
    average_pages = cursor.fetchone()[0]
    print(f"\nThe average number of pages is: {average_pages}")


def youngest_author():
    # Query to find the youngest author based on birthdate
    cursor.execute('''
        SELECT * FROM Author
        WHERE birthdate = (
            SELECT birthdate
            FROM Author
            ORDER BY substr(birthdate, 7, 4) || substr(birthdate, 4, 2) || substr(birthdate, 1, 2) DESC
            LIMIT 1
        );
    ''')

    # Fetch and print the results
    youngest_authors = cursor.fetchall()
    print("\nThe youngest authors are:")
    for author in youngest_authors:
        print(author)


def author_without_book():
    # Query to find authors without any books
    cursor.execute('''
        SELECT Author.*
        FROM Author
        LEFT JOIN Book ON Author.ID = Book.author_id
        WHERE Book.ID IS NULL;
    ''')

    # Fetch and print the results
    authors = cursor.fetchall()
    print("\nAuthors without books are:")
    for author in authors:
        print(author)


def author_with_3books():
    # Query to find 5 authors who have more than 3 books
    cursor.execute('''
        SELECT Author.*, COUNT(Book.ID) AS book_count
        FROM Author
        JOIN Book ON Author.ID = Book.author_id
        GROUP BY Author.ID
        HAVING COUNT(Book.ID) > 3
        LIMIT 5;
    ''')

    # Fetch and print the results
    authors = cursor.fetchall()
    print("\n5 authors with more than 3 books are:")
    for author in authors:
        print(author)


# Call the functions to execute queries
books_with_max_pages()
avg_number_of_pages()
youngest_author()
author_without_book()
author_with_3books()

# Close the database connection
connection.close()
