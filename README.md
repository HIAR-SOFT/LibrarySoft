# LibrarySoft
Library Management Command Line Program for alleviating Work     
Furkan KIR
Daria Babuchenka
## Contents 
1. Contents 
2. Abstract 
3. Introduction 
4. Calling the function initially 
5. lms-add 
6. lms-delete 
7. lms-list 
8. lms-search 
9. lms-update 
10. lms-custom-query 
11. Discussion 
12. Advantages and applications 
13. Conclusion 
14. References 
15. Appendix
## Abstract

This project is a Python-based program designed to simplify library management via the command line. It uses SQLite for database management and supports CRUD (Create, Read, Update, Delete) operations alongside additional functionalities. The program is open source to support underfunded libraries in rural Turkey, promoting the standardization of open-source software.

---

## Introduction

The system addresses the digital service challenges faced by rural libraries in Turkey. Unlike proprietary software that requires significant investment, this open-source solution allows libraries to manage their collections efficiently using a free and adaptable platform.

---

## Calling the Function Initially

To use the program:
1. Ensure that Python, SQLite, and the required libraries (`Faker`, `sqlite3`, and `click`) are installed.
2. Run the program with the command:
   ```bash
   python libManSys.py
   ```
3. A dummy SQLite database is generated upon the first run.

---

## Commands

### lms-add

- **Purpose**: Add a new book to the library.
- **Command**: 
  ```bash
  lms-add --id <ID> --name <Name> --language <Language> --author <Author> --location <Location> --year <Year>
  ```
- **Database Query**:
  ```sql
  INSERT INTO books (id, name, language, author, location, year) VALUES (?, ?, ?, ?, ?, ?);
  ```

### lms-delete

- **Purpose**: Remove a book by ID.
- **Command**:
  ```bash
  lms-delete --id <ID>
  ```
- **Database Query**:
  ```sql
  DELETE FROM books WHERE id = ?;
  ```

### lms-list

- **Purpose**: List all books in the library.
- **Command**:
  ```bash
  lms-list
  ```
- **Database Query**:
  ```sql
  SELECT * FROM books;
  ```

### lms-search

- **Purpose**: Search for books based on specific criteria (e.g., name, author).
- **Command**:
  ```bash
  lms-search --metric <Metric> --term <Search Term>
  ```
- **Database Query**:
  ```sql
  SELECT * FROM books WHERE {metric} LIKE ?;
  ```

### lms-update

- **Purpose**: Update details of an existing book.
- **Command**:
  ```bash
  lms-update --id <ID> --name <Name> --language <Language> --author <Author> --location <Location> --year <Year>
  ```
- **Database Query**:
  ```sql
  UPDATE books SET name = ?, language = ?, author = ?, location = ?, year = ? WHERE id = ?;
  ```

### lms-custom-query

- **Purpose**: Execute a custom SQL query.
- **Command**:
  ```bash
  lms-custom-query --query "<SQL Query>"
  ```

---

## Discussion

The tool provides a foundational framework for library management, enabling rural libraries to streamline their operations. The flexibility of the custom query feature allows for advanced usage and scalability.

---

## Advantages and Applications

1. **Free and Open Source**: No licensing costs.
2. **Adaptability**: Can be integrated into GUIs.
3. **Longevity**: Independent of company stability.

---

## Conclusion

This program serves as a step towards standardizing open-source tools in rural Turkish libraries, bridging the gap between underfunded institutions and proprietary software solutions.

---

## References

- West, J., & Dedrick, J. (2001). *Open source standardization: The rise of Linux in the network era*. Springer.
- Yılmaz, B., & Cevher, N. (2015). *Future of public libraries: Opinions of public librarians in Turkey*. SAGE Journals.

---

## Appendix

The full code is available in the `libManSys.py` script. Key functions include:

- `LMS_initialize_database()`
- `LMS_add_book_to_db()`
- `LMS_get_all_books()`
- `LMS_delete_book_from_db()`
- `LMS_update_book_in_db()`
- `LMS_search_books_in_db()`
- `LMS_execute_custom_query()`
