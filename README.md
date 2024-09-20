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

GET : '/api/books/' -> list_books
POST : '/api/books/add/' -> add_book
GET : '/api/books/<int:book_id>/' -> get_book
DELETE : '/api/books/delete/<int:book_id>/' -> delete_book
GET : '/api/student/borrowed/' -> borrowed_books
POST : '/api/student/renew/<int:book_id>/' -> renew_book
PUT : '/api/librarian/check/' -> check_borrowed_books
POST : '/api/librarian/check_by_user/' -> check_by_user
POST : '/api/librarian/borrow/<int:book_id>/' -> borrow_book
POST : '/api/librarian/return/<int:book_id>/' -> return_book

   
