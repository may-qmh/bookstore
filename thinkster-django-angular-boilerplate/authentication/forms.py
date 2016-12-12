from django import forms
from books.models import Book, OrderHistory, Feedback

class AddBookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = '__all__'


class SearchBookForm(forms.ModelForm):
	class Meta:
		model = Book
		fields = ('isbn10',)

class EditBookForm(forms.ModelForm):
    bookset = Book.objects.all().order_by('isbn10')
    bookset=list(bookset)
    book_choices = [(bookset[i].isbn10,'('+bookset[i].isbn10+') '+bookset[i].title) for i in range(len(bookset))]
    isbn10 = forms.ChoiceField(choices=book_choices)

    stock = forms.IntegerField(min_value=1)
    class Meta:
        model = Book
        fields = ('isbn10','stock',)
		
		
class FilterBookForm(forms.Form):
    month_choices = (
        ('1', 'Jan'),
        ('2', 'Feb'),
        ('3', 'Mar'),
        ('4', 'Apr'),
        ('5', 'May'),
        ('6', 'Jun'),
        ('7', 'Jul'),
        ('8', 'Aug'),
        ('9', 'Sep'),
        ('10', 'Oct'),
        ('11', 'Nov'),
        ('12', 'Dec')
    )

    month = forms.ChoiceField(choices=month_choices)
    views = forms.IntegerField(min_value=1)
	
class FeedbackForm(forms.Form):
    ISBN10 = forms.CharField(
    widget=forms.TextInput(attrs={'readonly':'readonly'})
)
    title = forms.CharField(
    widget=forms.TextInput(attrs={'readonly':'readonly'})
)
    score = forms.IntegerField(min_value=0,max_value=10)
    opinion = forms.CharField(min_length=1)

class UsefulnessForm(forms.Form):
    ISBN10 = forms.CharField(
    widget=forms.TextInput(attrs={'readonly':'readonly'})
)
    title = forms.CharField(
    widget=forms.TextInput(attrs={'readonly':'readonly'})
)   
    rating_on = forms.CharField(
    widget=forms.TextInput(attrs={'readonly':'readonly'})
)   
    score = forms.IntegerField(min_value=0,max_value=2)

class AdvanceSearchForm(forms.Form):
    title = forms.CharField(required=False)
    authors = forms.CharField(required=False)
    publisher = forms.CharField(required=False)
    subject = forms.CharField(required=False)
    # class Meta:
    #     model = Book 
    #     fields = ('authors','publisher','title','subject',)


class UsefulFeedbackForm(forms.Form):
    top_n = forms.IntegerField(min_value=1,max_value=500)