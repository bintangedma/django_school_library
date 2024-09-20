from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book, BorrowRecord
from django.utils.timezone import now
from django.contrib.auth.models import User
from datetime import timedelta
import traceback
from .services import MasterService, BookService, BorrowService

books_svc = BookService()
borrow_svc = BorrowService()

# API to list all available books
@api_view(['GET'])
def list_books(request):
    return books_svc.fetch_books()

@api_view(['GET'])
def get_book(request, book_id):
    return books_svc.get_book_by_id(book_id)

@api_view(['POST'])
def renew_book(request, book_id):
    return borrow_svc.renew_books(book_id, request.user)

@api_view(['POST'])
def add_book(request):
    return books_svc.create_book(request.data)

@api_view(['DELETE'])
def delete_book(request, book_id):
    return books_svc.delete_book(book_id)

# API for a student to check borrowed books and renew if possible
@api_view(['GET'])
def borrowed_books(request):
    return borrow_svc.fetch_borrowed_books(request.user)

# API for a student to check borrowed books and renew if possible
@api_view(['PUT'])
def check_borrowed_books(request):
    return borrow_svc.check_history(request.data)

@api_view(['POST'])
def check_by_user(request):
    return borrow_svc.check_by_user(request.data)

# Librarian marking books as borrowed or returned
@api_view(['POST'])
def borrow_book(request, book_id):
    student = request.data.get('student_id')
    return borrow_svc.borrow_book(student, book_id)

@api_view(['POST'])
def return_book(request, book_id):
    student = request.data.get('student_id')
    return borrow_svc.return_book(student, book_id)
    