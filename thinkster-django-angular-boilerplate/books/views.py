import json
from django.http import Http404
from rest_framework import status, views, permissions, viewsets
from rest_framework.response import Response
from books.models import Book, BookOrdered, Feedback, OrderHistory, UsefulnessRating
from authentication.models import Account
from django.shortcuts import render
from rest_framework import status, views, permissions
from django.contrib.staticfiles.templatetags.staticfiles import static
from authentication.forms import UsefulnessForm, AdvanceSearchForm, UsefulFeedbackForm
from collections import Counter
from django.db.models import Q

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
        print "POST request in BookView"


        form = UsefulnessForm(request.POST)
        form_rank = UsefulFeedbackForm(request.POST)
        if form.is_valid() or form_rank.is_valid():
            isbn10 = request.POST.get('ISBN10',False)
            print "check isbn10"
            print isbn10
            if not isbn10:
                isbn10 = request.POST.get('id_book',False)
                avg_fb_score = get_score(isbn10)
            bookinfo = Book.objects.get(pk=isbn10)
            feedback2 = Feedback.objects.filter(isbn10=isbn10)
            fbnum = len(feedback2)
            book_display = book_display_individual(request,isbn10)
            entry = list(zip(book_display['scoreList'],feedback2))
            views = int(request.POST['top_n'])
            entry.sort()
            entry.reverse()
            print entry
            entry= entry[:views]
            if not form_rank.is_valid():  
                avg_fb_score = get_score(isbn10)          
                score = request.POST['score']
                
                ratee = request.POST['rating_on']
                
                
                feedback = Feedback.objects.filter(login_id=ratee).get(isbn10=isbn10)

                form = UsefulnessForm()

                rating = UsefulnessRating(usefulness=score, rater=account[0], ratee=feedback.login, isbn10=feedback.isbn10)
        
                try:
                    rating.full_clean() #checks if rater==ratee
                    rating.save()
                    #return HttpResponseRedirect('/books/' + feedback.book.isbn)
                except Exception as e:
                    #when rater = ratee OR when rater rates same feedback again
                    raise Http404('invalid')
            return render(request,'book_info.html',{'bookinfo':bookinfo, 'feedback':entry, 'form':form, 'fbnum': fbnum, 'display':book_display,'fbscore':avg_fb_score})
        else:            
            print "UsefulnessForm and UsefulFeedbackForm input invalid"
            return render(request,'book_info.html',{})
        

    def get(self, request, isbn10):
        print "test bookview"
        print "GET request in BookView"
        form = UsefulnessForm()
        isbn10 = str(isbn10)

        if len(isbn10)!=10:
            diff = 10-len(isbn10)
            isbn10="0"*diff+isbn10

        avg_fb_score = get_score(isbn10)

        bookinfo = Book.objects.get(pk=isbn10)
        feedback = Feedback.objects.filter(isbn10=isbn10)
        fbnum = len(feedback)
        book_display = book_display_individual(request,isbn10)
        entry = list(zip(book_display['scoreList'],feedback))

        return render(request,'book_info.html',{'bookinfo':bookinfo, 'feedback': entry, 'fbnum': fbnum, 'form':form, 'display':book_display,'fbscore':avg_fb_score})

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

        return render(request, 'confirmation.html', {})

    def get(self, request, isbn10):
        print "test confirmationview"

        isbn10 = str(isbn10)
        print(isbn10)
        if len(isbn10)!=10:
            diff = 10-len(isbn10)
            isbn10="0"*diff+isbn10

        recommendedbooks = recommendations(request,isbn10)
        print recommendedbooks
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

        return render(request,'confirmation.html',{'recommended':recommendedbooks})

#book search 
def book_search(request):
    data = []
    queries = []
    temp = Book.objects.all()
    if request.method == 'GET' :
        print "basic search"
        form = AdvanceSearchForm(request.GET)
        if form.is_valid():

            authors = form.cleaned_data['authors']
            queries.append(authors)
            publisher = form.cleaned_data['publisher']
            queries.append(publisher)
            title = form.cleaned_data['title']
            queries.append(title)
            subject = form.cleaned_data['subject']
            queries.append(subject)
            
            for i in range(0,len(queries)):
                if queries[i] != "":
                    if i ==0:
                        temp = temp.filter(authors__icontains = queries[i])
                    elif i==1:
                        temp = temp.filter(publisher__icontains = queries[i])
                    elif i==2:
                        temp = temp.filter(title__icontains = queries[i])
                    else:
                        temp = temp.filter(subject__icontains = queries[i])
        

            for entry in temp:
                score = get_score(entry.isbn10)
                data.append({'image':entry.image, 'isbn10':entry.isbn10, 'title':entry.title, 'authors':entry.authors, 'publisher':entry.publisher, 'year':entry.year, 'stock':entry.stock, 'price':entry.price, 'format':entry.format, 'keyword':entry.keyword, 'subject':entry.subject, 'score':score})
         
            
    else:
        search = request.POST.get('search',False)
        query = Q(title__icontains=search) | Q(authors__icontains=search) | Q(publisher__icontains=search) | Q(keyword__icontains=search) | Q(subject__icontains=search) 
        data = Book.objects.filter(query)
        form = AdvanceSearchForm()
        
    return render(request, 'advance_search.html', {'form' :form, 'data':data})
def get_score(isbn10):
    data = Feedback.objects.filter(isbn10=isbn10)
    score =0.0
    count =0.0
    for entry in data:
        score+= entry.score
        count+=1.0
    if count == 0:
        return 0
    else:
        average_score= score/count

        return average_score


def recommendations(request, isbn10):
    #user's order
    username = request.user
    print username
    if len(isbn10)!=10:
            diff = 10-len(isbn10)
            isbn10="0"*diff+isbn10
    book = Book.objects.get(isbn10=isbn10)

    # queryset of all bookordered with this isbn10
    orders = book.bookordered_set.all()


    if len(orders)==0:
        return None
    else:
                # get orderhistory
        orderhistory = [ order.oid for order in orders ]

        # get users who bought this book using oid
        usernames =set(i.login_id for i in orderhistory)
        if str(username) in usernames:
            usernames.remove(str(username))
        # get all the oids of these users
        # allorders: nested list of orderhistories
        allorders = []
        for i in usernames:
            allorders.append(OrderHistory.objects.filter(login=i))

        allorders = [ item for sublist in allorders for item in sublist ]

        other_books = []
        for i in allorders:
            bookordered = BookOrdered.objects.filter(oid=i.oid)
            for o in bookordered:
                if o.isbn10.isbn10!=isbn10:
                    other_books.append(o.isbn10)
        count_book = Counter(other_books)
        l = [(count_book[key],key) for key in count_book]
        l.sort()
        l.reverse()
        recommendedbooks = []
        for i in l:
            recommendedbooks.append(i[1])
            
        return recommendedbooks

#######################################################
################ BOOK USEFULNESS SORT #################
#######################################################

def book_display_individual(request,isbn10):
    print "in book display individual"
    temp = Book.objects.get(isbn10 = isbn10)
    temp1 = Feedback.objects.filter(isbn10=isbn10)
    data=[]
    data1=[]
    scoreList =[]
    for entry in temp1:
        data1.append({'opinion':entry.opinion, 'login':entry.login.username})
    
    for entry in data1:
        avgscore = get_usefulness(isbn10,entry['login'])
        scoreList.append(avgscore)
        
    
    data.append({'isbn10':isbn10, 'title':temp.title, 'authors':temp.authors, 'publisher':temp.publisher, 'year':temp.year, 'stock':temp.stock, 'price':temp.price, 'format':temp.format, 'keyword':temp.keyword, 'subject':temp.subject})
    
    # if request.method=='POST':
    #     print "POST detected in book display individual"
    #     form = UsefulFeedbackForm(request.POST)
    #     if form.is_valid():
    #         views = int(request.POST['views'])
    #         scoreList= scoreList[:views]
    
    print "NON POST in book display individual"
    form = UsefulFeedbackForm()
    
    return {'data':data, 'data1':data1, 'scoreList':scoreList, 'form':form}





def get_usefulness(isbn10, ratee):
    data = UsefulnessRating.objects.filter(isbn10=isbn10, ratee_id = ratee)
    score =0.0
    count =0.0
    for entry in data:
        score+= entry.usefulness
        count+=1.0
    if count == 0:
        return 0
    else:
        average_score= score/count
        print average_score
        return average_score