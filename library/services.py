from .models import Book, BorrowRecord
from rest_framework.response import Response
from .serializers import BookSerializer, BorrowRecordSerializer
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.utils.timezone import now
import traceback

class MasterService : 
    def __init__(self, model) -> None:
        self.model = model
        self.book_serializer = BookSerializer
        self.borrow_serializer = BorrowRecordSerializer

class BookService(MasterService) :
    def __init__(self) -> None:
        model = Book
        super().__init__(model)

    def fetch_books(self) : 
        books = self.model.objects.all()
        book_list = [
        {
            'title': book.title,
            'author': book.author,
            'available_copies': book.available_copies,
        }
        for book in books
        ]
        book_list = []
        for book in books : 
            _book = {
            'title': book.title,
            'author': book.author,
            'available_copies': book.available_copies,
            }
            if book.available_copies > 0 :
                book_list.append(_book)
            else : 
                book = self.model.objects.get(id=book.id)
                borrowed_books = BorrowRecord.objects.filter(book=book)
                borrowed_list = [
                    {
                    'title': record.book.title,
                    'author': record.book.author,
                    'available_copies': record.book.available_copies,
                    'borrowed_at': record.borrowed_at,
                    'return_date': record.return_date,
                    'renewed': record.renewed,
                    'student': record.student.id,
                    'book_id': record.book.id}
                    for record in borrowed_books
                    ]
                sorted_book_list = sorted(borrowed_list, key=lambda x: x['return_date'])
                _now = now()
                for borrowed_book in sorted_book_list : 
                    if borrowed_book.get('return_date') >= _now : 
                        book_list.append(borrowed_book)
        return Response(book_list)
    
    def create_book(self, _form) : 
        _title = _form.get('title')
        _author = _form.get('author')
        _total_copies = _form.get('total_copies')
        _available_copies = _form.get('available_copies')
        self.model.objects.create(title=_title, author=_author, total_copies=_total_copies, available_copies=_available_copies)

        return Response(self.book_serializer(), 200)
    
    def delete_book(self, book_id) :
        try:
            book = self.model.objects.get(id=book_id)
            book.delete()
            return Response({"message": "Book deleted successfully"}, status=204)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=404)
    
    def get_book_by_id(self, book_id) : 
        book = self.model.objects.get(id=book_id)
        return Response(self.book_serializer(book).data)

    
class BorrowService(MasterService) :
    def __init__(self) -> None:
        model = BorrowRecord
        self.book = Book
        super().__init__(model)

    def fetch_borrowed_books(self, student) : 
        records = self.model.objects.filter(student=student)
        # print([self.borrow_serializer(r).data for r in records])
        borrowed_list = [
            {
                'book': record.book.title,
                'borrowed_at': record.borrowed_at,
                'return_date': record.return_date,
                'renewed': record.renewed,
                'student': record.student.id,
                'book_id': record.book.id,
            }
            for record in records
        ]
        return Response(borrowed_list)
    
    def renew_books(self, book_id, student) : 
        print(book_id, student)
        records = self.model.objects.filter(book_id=book_id, student=student)
        flag = False
        for record in records : 
            if not record.renewed:
                record.renew()
                flag = True
        if flag == True : 
            return Response({"message": "Book renewed successfully!"})
        return Response({"message": "Book can't be renewed."}, status=400)

    def borrow_book(self, student, book_id) : 
        book = self.book.objects.get(id=book_id)
        _student = User.objects.get(id=student)
        records = BorrowRecord.objects.filter(student=_student)
        if len([r.student.id for r in records]) >= 10 : 
            return Response({"message": "Limit : This user has borrowed 10 books."})
        # print(self.book_serializer(book).data)
        if book.available_copies > 0:
            self.model.objects.create(student=_student, book=book, return_date=now() + timedelta(days=30))
            book.available_copies -= 1
            book.save()
            return Response({"message": "Book borrowed successfully!"})
        return Response({"message": "No copies available!"}, status=400)

    def return_book(self, student, book_id) : 
        try :
            _student = User.objects.get(id=student)
            records = BorrowRecord.objects.filter(book=book_id, student=_student)
            flag = False
            for record in records:
                book = record.book
                book.available_copies += 1
                book.save()
                record.delete()
                flag = True
            if flag == True : 
                return Response({"message": "Book returned successfully!"})
            return Response({'message' : 'This book is already returned.'})
        except : 
            traceback.print_exc()
            return Response({"message": "Error"})
        
    def check_history(self, _form) : 
        try :
            student_id = _form.get('student_id')
            book_id = _form.get('book_id')
            if student_id and not book_id : 
                _student = User.objects.get(id=student_id)
                records = BorrowRecord.objects.filter(student=_student)
            elif book_id and not student_id : 
                _book = self.book.objects.get(id=book_id)
                records = BorrowRecord.objects.filter(book=_book)
            elif not book_id and not student_id :
                records = BorrowRecord.objects.all()
            else : 
                _student = User.objects.get(id=student_id)
                _book = self.book.objects.get(id=book_id)
                records = BorrowRecord.objects.filter(book=_book, student=_student)
            records = [
                {'book': record.book.title,
                'borrowed_at': record.borrowed_at,
                'return_date': record.return_date,
                'renewed': record.renewed,
                'student': record.student.id,
                'book_id': record.book.id}
                for record in records
            ]
            return Response(records)
        except : 
            traceback.print_exc()
            return Response({"message": "Error"})
        
    def check_by_user(self, _form) : 
        try :
            students = User.objects.all() 
            records = []
            for record in students : 
                data = {
                    'id': record.id,
                    'name': record.username,
                 }
                borrowed_book = self.model.objects.filter(student=record)
                amount_borrowed_book = [{'book_id' : d.book.id} for d in borrowed_book]
                data.update({'borrowed_book' : len(amount_borrowed_book)})
                records.append(data)
            return Response(records)
        except : 
            traceback.print_exc()
            return Response({"message": "Error"})
