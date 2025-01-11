import click
import sqlite3
from faker import Faker
import random


fake = Faker()

# SQLite database file
DB_FILE = "books.db"


def LMS_initialize_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        language TEXT NOT NULL,
                        author TEXT NOT NULL,
                        location TEXT NOT NULL,
                        year INTEGER NOT NULL
                    )''')
    conn.commit()
    conn.close()

# Add a book to the database
def LMS_add_book_to_db(book):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (id, name, language, author, location, year) VALUES (?, ?, ?, ?, ?, ?)", 
                   (book["id"], book["name"], book["language"], book["author"], book["location"], book["year"]))
    conn.commit()
    conn.close()

# Retrieve all books from the database
def LMS_get_all_books():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return books

# Delete a book from the database
def LMS_delete_book_from_db(book_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

# Update a book in the database
def LMS_update_book_in_db(book_id, updated_book):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''UPDATE books 
                      SET name = ?, language = ?, author = ?, location = ?, year = ? 
                      WHERE id = ?''', 
                   (updated_book["name"], updated_book["language"], updated_book["author"], 
                    updated_book["location"], updated_book["year"], book_id))
    conn.commit()
    conn.close()

# Search for books in the database
def LMS_search_books_in_db(metric, term):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    query = f"SELECT * FROM books WHERE {metric} LIKE ?"
    cursor.execute(query, (f"%{term}%",))
    books = cursor.fetchall()
    conn.close()
    return books

# Execute custom SQL queries on the database
def LMS_execute_custom_query(query):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(query)
        if query.strip().lower().startswith("select"):
            results = cursor.fetchall()
            for row in results:
                print(row)
        else:
            conn.commit()
            click.echo("Query executed successfully.")
    except sqlite3.Error as e:
        click.echo(f"Error executing query: {e}")
    finally:
        conn.close()

@click.group()
def LMS_cli():
    pass

# Command: Add a book
@LMS_cli.command()
@click.option('--id', prompt=True, type=int)
@click.option('--name', prompt=True)
@click.option('--language', prompt=True)
@click.option('--author', prompt=True)
@click.option('--location', prompt=True)
@click.option('--year', prompt=True, type=int)
def LMS_add(id, name, language, author, location, year):
    book = {"id": id, "name": name, "language": language, "author": author, "location": location, "year": year}
    LMS_add_book_to_db(book)
    click.echo(f"Book '{name}' added successfully!")

# Command: List all books
@LMS_cli.command()
def LMS_list():
    books = LMS_get_all_books()
    if books:
        for book in books:
            print(f"{book[0]:<6}| {book[1]:<50}| {book[2]:<20}| {book[3]:<20}| {book[4]:<10}| {book[5]:<5}")
    else:
        click.echo("No books found in the database.")

# Command: Delete a book
@LMS_cli.command()
@click.option('--id', prompt=True, type=int)
def LMS_delete(id):
    LMS_delete_book_from_db(id)
    click.echo(f"Book with ID {id} deleted successfully!")

# Command: Update a book
@LMS_cli.command()
@click.option('--id', prompt=True, type=int)
@click.option('--name', prompt=True)
@click.option('--language', prompt=True)
@click.option('--author', prompt=True)
@click.option('--location', prompt=True)
@click.option('--year', prompt=True, type=int)
def LMS_update(id, name, language, author, location, year):
    book = {"name": name, "language": language, "author": author, "location": location, "year": year}
    LMS_update_book_in_db(id, book)
    click.echo(f"Book with ID {id} updated successfully!")

# Command: Search for books
@LMS_cli.command()
@click.option('--metric', prompt='Enter search metric (name, language, author, location, year)', type=str)
@click.option('--term', prompt='Enter search term', type=str)
def LMS_search(metric, term):
    books = LMS_search_books_in_db(metric, term)
    if books:
        for book in books:
            print(f"{book[0]:<6}| {book[1]:<50}| {book[2]:<20}| {book[3]:<20}| {book[4]:<10}| {book[5]:<5}")
    else:
        click.echo(f"No books found with {metric} matching '{term}'.")

# Command: Execute a custom SQL query
@LMS_cli.command()
@click.option('--query', prompt='Enter your custom SQL query')
def LMS_custom_query(query):
    LMS_execute_custom_query(query)

# Generate random books if the database is empty
def LMS_generate_random_books():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    for _ in range(50):
        id = fake.unique.random_number(digits=5)
        name = fake.catch_phrase()
        language = fake.language_name()
        author = fake.name()
        location = f"Floor {random.randint(1, 5)}"
        year = fake.year()
        cursor.execute("INSERT INTO books (id, name, language, author, location, year) VALUES (?, ?, ?, ?, ?, ?)",
                       (id, name, language, author, location, year))
    conn.commit()
    conn.close()

# Initialize the database and add random books if it's empty
LMS_initialize_database()
if not LMS_get_all_books():
    LMS_generate_random_books()

if __name__ == '__main__':
    LMS_cli()
