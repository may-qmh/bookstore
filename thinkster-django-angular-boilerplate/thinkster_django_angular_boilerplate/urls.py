from django.conf.urls import patterns, url, include



from thinkster_django_angular_boilerplate.views import IndexView

from authentication.views import LoginView, LogoutView, SearchView

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

    url(r'^api/v1/search/$', SearchView.as_view(), name='search_books'),

    url('^.*$', IndexView.as_view(), name='index')
)
