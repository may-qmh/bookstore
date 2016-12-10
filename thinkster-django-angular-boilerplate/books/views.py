import json

from rest_framework import status, views, permissions, viewsets
from rest_framework.response import Response
from books.models import Book, BookOrdered, Customer, Feedback, OrderHistory, UsefulnessRating
from django.shortcuts import render

from django.contrib.staticfiles.templatetags.staticfiles import static

class SearchView(views.APIView):
    def post(self, request, format=None):
        data = json.loads(request.body)

        author = data.get('author', None)
        publisher = data.get('publisher', None)
        bk_title = data.get('bk_title', None)
        subject = data.get('subject', None)
        print "testing from views.py"
        print author
        print publisher
        print bk_title 
        print subject

        return Response({}, status=status.HTTP_204_NO_CONTENT)

class HomeView(views.APIView):
    def get(self, request):
        print "test homeview"
        books = Book.objects.all()[1:4]
        first = Book.objects.all()[0]
        return render(request,'homepage.html',{'books':books,'first':first})

class BookView(views.APIView):
    def post(self, request, format=None):
        data = json.loads(request.body)

        isbn10 = data.get('isbn10', None)
        print "test post"
        
        print isbn10
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request, isbn10):
        print "test bookview"

        isbn10 = str(isbn10)
        if len(isbn10)!=10:
            diff = 10-len(isbn10)
            isbn10="0"*diff+isbn10

        bookinfo = Book.objects.get(pk=isbn10)
        return render(request,'book_info.html',{'bookinfo':bookinfo})