"""
URL configuration for library_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import list_books, borrowed_books, renew_book, borrow_book, return_book, add_book, delete_book, get_book, check_borrowed_books, check_by_user

urlpatterns = [
    path('books/', list_books), # Task 1 (a & b)
    path('books/add/', add_book),
    path('books/<int:book_id>/', get_book),
    path('books/delete/<int:book_id>/', delete_book),
    path('student/borrowed/', borrowed_books), # Task 2 a
    path('student/renew/<int:book_id>/', renew_book), # Task 2 b
    path('librarian/check/', check_borrowed_books), # Task 3 a{"student_id" : "2", "book_id" : "4"}
    path('librarian/check_by_user/', check_by_user), # Task 3 a{"student_id" : "2", "book_id" : "4"}
    path('librarian/borrow/<int:book_id>/', borrow_book), # Task 3 b
    path('librarian/return/<int:book_id>/', return_book), # Task 3 c
]