import json
from django.contrib.auth import authenticate, login, logout

from rest_framework import status, views, permissions, viewsets
from rest_framework.response import Response

from authentication.models import Account
from authentication.permissions import IsAccountOwner
from authentication.serializers import AccountSerializer

from django.shortcuts import render

from .forms import AddBookForm, EditBookForm, SearchBookForm, FilterBookForm
from operator import itemgetter
from authentication.forms import AddBookForm, EditBookForm, SearchBookForm, FilterBookForm, FeedbackForm
from books.models import *

class AccountViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(), IsAccountOwner(),)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            Account.objects.create_user(**serializer.validated_data)

            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(views.APIView):
    def post(self, request, format=None):
        data = json.loads(request.body)

        username = data.get('username', None)
        password = data.get('password', None)

        account = authenticate(username=username, password=password)

        if account is not None:
            if account.is_active:
                login(request, account)

                serialized = AccountSerializer(account)

                return Response(serialized.data)
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This account has been disabled.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        logout(request)

        return Response({}, status=status.HTTP_204_NO_CONTENT)

class UserView(views.APIView):
    def post(self, request, format=None):
        #logout(request)

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request):
        print "test bookview"

        print username

       #userinfo = Book.objects.get(pk=isbn10)
        return render(request,'user_info.html',{'bookinfo':"test"}) 

######################################################################
################### Admin Account Side ################################
######################################################################

# Add new book
def book_new(request):
    message = ""
    if request.method == 'POST':
        form = AddBookForm(request.POST)
        if form.is_valid():
            post = form.save()
            print "successful update"
            message="BOOK SUCCESSFULY ADDED. BOOK INVENTORY UPDATED."

    else:
        form = AddBookForm()
        
    return render(request, 'addbook.html',{'form': form, 'msg':message})
        
# Edit number of copies of a book   
def book_edit(request):
    message = ""
    if request.method == 'POST':
        isbn10 = request.POST['isbn10']
        form = EditBookForm(request.POST, instance = Book.objects.get(isbn10= isbn10))
        if form.is_valid():
            form.save()
            print "YOUR EDIT WAS SUCCESSFUL. BOOK INVENTORY UPDATED."
            message="YOUR EDIT WAS SUCCESSFUL. BOOK INVENTORY UPDATED."
    else:
        form = EditBookForm()
    
    return render(request, 'book_update_form.html', {'form' : form, 'msg':message})
    
# Show a list of inventories    
# def book_display(request):
#     data = Book.objects.all()
#     return TemplateResponse(request, 'book_show.html',{'data' : data})
    
# Show individual book 
def book_display_individual(request , isbn10):
    data = Book.objects.get(pk = isbn10 )
    return TemplateResponse(request, 'book_show_individual.html', {'data': data})
    
    
# Statistics of book - top m books, authors and publishers  
def book_popular(request):
    temp = BookOrdered.objects.all()
    data = []
    authors_count={}
    publisher_count={}
    for entry in temp:
        title, authors, publisher = get_book(entry.isbn10.isbn10)
        date = get_date(entry.oid.oid)
        data.append({'date':date, 'isbn10':entry.isbn10.isbn10, 'title': title, 'authors':authors, 'publisher':publisher,'quantity':entry.quantity})
    
    form = FilterBookForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            month = request.POST['month']
            views = int(request.POST['views'])
            for entry in data[::-1]:
                if entry['date'] != int(month):
                    data.remove(entry)
            
            for entry in data:
                if entry['authors'] not in authors_count.keys():
                    authors_count[entry['authors']] =0
                authors_count[entry['authors']] += entry['quantity']
                
                if entry['publisher'] not in publisher_count.keys():
                    publisher_count[entry['publisher']] =0
                publisher_count[entry['publisher']] += entry['quantity']
            
            authors_count = sorted(authors_count.items(), key = itemgetter(1),reverse=True)[:views]
            publisher_count = sorted(publisher_count.items(), key =itemgetter(1), reverse = True)[:views]
            n = len(data)
            new_data=[]
            for i in range(n-1):
                print i
                for j in range(i+1,n):
                    if data[i]['isbn10'] == data[j]['isbn10']:
                        data[i]['quantity']+=data[j]['quantity']
                        new_data.append(data[j])
            for j in new_data:
                data.remove(j)
                
                    
            data = sorted(data, key = lambda user: user['quantity'], reverse=True)[:views]

    else:
        form = FilterBookForm()
    
    return render(request, 'book_popular.html', {'data': data,'form':form, 'authors_count':authors_count, 'publisher_count':publisher_count})
    
def account_admin(request):
    data = Book.objects.all()
    return render(request, 'adminpage.html',{'data' : data})
# get title, author and publisher 
def get_book(isbn10):
    data = Book.objects.get(isbn10=isbn10)
    return data.title, data.authors, data.publisher
# get isbn10 and quantity   
def get_isbn(oid):
    data = BookOrdered.objects.get(oid = oid)
    return data.isbn10.isbn10, data.quantity
# get month     
def get_date(oid):
    data = OrderHistory.objects.get(oid = oid)
    return data.order_date.month


######################################################################
################### User Account Side ################################
######################################################################

def user_account(request,user):
    #need to get username of current user
    username = request.user

    account_info = Account.objects.filter(username=username)
    print account_info[0].username
    o_history = OrderHistory.objects.filter(login=username)
    ob = [ BookOrdered.objects.filter(oid=i).all() for i in o_history ]
    books = []
    isFeedback = []
    for o in ob:
        for i in o:
            books.append(i.isbn10)
            isFeedback.append(check_feedback(i.isbn10,username))
    
    order_info = list(zip(o_history, books, ob, isFeedback))
    feedbacks = Feedback.objects.filter(login=username)
    feedbacks_books = [ f.isbn10 for f in feedbacks ]
    feedback_info = list(zip(feedbacks, feedbacks_books))

    


    usefulnessratings = UsefulnessRating.objects.filter(rater=username)
    ratees = [ rating.ratee for rating in usefulnessratings ]
    books = [ rating.isbn10 for rating in usefulnessratings ]
    ratings_feedbacks = [ Feedback.objects.get(login=ratee,isbn10=book) for ratee, book in zip(ratees, books) ]
    rating_info = list(zip(usefulnessratings, ratees, books, ratings_feedbacks))

    form = FeedbackForm(request.POST)
    if request.method == 'POST':
        msg=""
        if form.is_valid():
            text = request.POST['opinion']
            score = request.POST['score']
            isbn10 = request.POST['ISBN10']
            book_obj = Book.objects.get(isbn10=isbn10)
            feedback = Feedback(score=score, login=username, opinion=text, isbn10=book_obj)
            try:
                feedback.full_clean()
                feedback.save()
                msg="Feedback Successful!"
            except:
                msg="Feedback Failed! Please try again."
    else:
        msg = ""
        form = FeedbackForm()
    return render(request, 'user_info.html', {
            'account_info': account_info[0],
            'orders': order_info,
            'feedbacks': feedback_info,
            'ratings': rating_info,
            'form':form,
            'msg':msg

        })



# check whether user feedback before or not
def check_feedback(isbn10,login_id):
    
    username = login_id
    user = Account.objects.filter(username=username)

    try:
        feedback = Feedback.objects.get(login=user[0], isbn10=isbn10)
    except Feedback.DoesNotExist:
        return True
    return False

