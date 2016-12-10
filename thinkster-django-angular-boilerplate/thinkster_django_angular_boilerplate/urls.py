from django.conf.urls import patterns, url, include

from thinkster_django_angular_boilerplate.views import IndexView

from authentication.views import LoginView, LogoutView, UserView

from books.views import SearchView, HomeView, BookView, ConfirmationView
# .. Imports
from rest_framework_nested import routers

from authentication.views import AccountViewSet



router = routers.SimpleRouter()
router.register(r'accounts', AccountViewSet)

urlpatterns = patterns(
     '',
    # ... URLs
    url(r'^api/v1/', include(router.urls)),

    url(r'^api/v1/auth/login/$', LoginView.as_view(), name='login'),

    url(r'^api/v1/auth/logout/$', LogoutView.as_view(), name='logout'),   

    url(r'^search/$', SearchView.as_view(), name='search_books'),
	
	url(r'^book/([a-zA-Z0-9-]+)$', BookView.as_view(), name='book_info'),

    url(r'^account/([a-zA-Z0-9-]+)$', UserView.as_view(), name='user_info'),

    url(r'^confirmation/([a-zA-Z0-9-]+)$', ConfirmationView.as_view(), name='user_info'),
    
	url(r'^$', HomeView.as_view(), name='home_page'),

    url('^.*$', IndexView.as_view(), name='index')
)
