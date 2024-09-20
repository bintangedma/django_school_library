Hello, My name is Bintang Edma and this is my Django project.
Follow these steps to run the application : 

1. Create and activate the virtual environment.
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   
2. Install the required python dependencies.
   pip install -r requirements.txt
   
3. Run database migration.
   python manage.py migrate

4. Run Django.
   python manage.py runserver

5. Access the app.
   http://localhost:8000

1. GET : '/api/books/' -> list_books
2. POST : '/api/books/add/' -> add_book
3. GET : '/api/books/<int:book_id>/' -> get_book
4. DELETE : '/api/books/delete/<int:book_id>/' -> delete_book
5. GET : '/api/student/borrowed/' -> borrowed_books
6. POST : '/api/student/renew/<int:book_id>/' -> renew_book
7. PUT : '/api/librarian/check/' -> check_borrowed_books
8. POST : '/api/librarian/check_by_user/' -> check_by_user
9. POST : '/api/librarian/borrow/<int:book_id>/' -> borrow_book
10. POST : '/api/librarian/return/<int:book_id>/' -> return_book

   
