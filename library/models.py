from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)

    def __str__(self):
        return self.title

class BorrowRecord(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrowed_books")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    renewed = models.BooleanField(default=False)

    def renew(self):
        if not self.renewed:
            self.return_date += timedelta(days=30)
            self.renewed = True
            self.save()