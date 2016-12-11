import json

from rest_framework import status, views, permissions, viewsets
from rest_framework.response import Response
from books.models import Book, BookOrdered, Feedback, OrderHistory, UsefulnessRating
from authentication.models import Account
from django.shortcuts import render
from rest_framework import status, views, permissions
from django.contrib.staticfiles.templatetags.staticfiles import static
from authentication.forms import UsefulnessForm

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
        username = request.user
        account = Account.objects.filter(username=username)

       
        form = UsefulnessForm(request.POST)
    
        if form.is_valid():
            
            score = request.POST['score']
            isbn10 = request.POST['ISBN10']
            ratee = request.POST['rating_on']
            

        #not sure
            feedback = Feedback.objects.filter(login_id=ratee).get(isbn10=isbn10)

            

            rating = UsefulnessRating(usefulness=score, rater=account[0], ratee=feedback.login, isbn10=feedback.isbn10)
        
            try:
                rating.full_clean() #checks if rater==ratee
                rating.save()
                #return HttpResponseRedirect('/books/' + feedback.book.isbn)
            except Exception as e:
                raise Http404('invalid')
        else:
            print "Usefulness form input invalid"

        return render(request,'book_info.html',{})

    def get(self, request, isbn10):
        print "test bookview"
        form = UsefulnessForm()
        isbn10 = str(isbn10)
        if len(isbn10)!=10:
            diff = 10-len(isbn10)
            isbn10="0"*diff+isbn10

        bookinfo = Book.objects.get(pk=isbn10)
        feedback = Feedback.objects.filter(isbn10=isbn10)
        fbnum = len(feedback)
        return render(request,'book_info.html',{'bookinfo':bookinfo, 'feedback': feedback, 'fbnum': fbnum, 'form':form})

class ConfirmationView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request, format=None):
        data = json.loads(request.body)

        isbn10 = data.get('isbn10', None)
        isbn10 = str(isbn10)
        if len(isbn10)!=10:
            diff = 10-len(isbn10)
            isbn10="0"*diff+isbn10
        print "test confirm"
        print isbn10
       
        username=request.user
        
        book = Book.objects.get(pk=isbn10)
        ordered = long(data.get('n',None))
        
        book.stock = book.stock - ordered
        book.save()
        new_order = OrderHistory(login=username, order_status = 'processing')
        new_order.save() 
        book_ordered = BookOrdered(oid=new_order, isbn10 = book, quantity = ordered)
        book_ordered.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request, isbn10):
        print "test confirmationview"

        isbn10 = str(isbn10)
        print(isbn10)
        if len(isbn10)!=10:
            diff = 10-len(isbn10)
            isbn10="0"*diff+isbn10

        #bookordered query sets with isbn10
        # book_order = BookOrdered.objects.filter(isbn10=isbn10)
        # oid = []
        # orders = []
        # book_buyer=[]

        #save all oids
        # for order in book_order:
        #     oid.append(order.oid)
        # #use oids to get orderhistory info
        # for o in oid:
        #     orders.append(OrderHistory.filter(oid=o))

        # #from orderhistoryinfo find users
        # for order in orders:
        #     all_buyer.append(order.filter(oid=order))


        # for user in all_buyer:

        # all_orders = OrderHistory.objects.get(login = book_buyer)
        # for i in all_orders:

        return render(request,'confirmation.html',{})