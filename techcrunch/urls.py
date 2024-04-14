from django.urls import path
from .views import (HomeView, search_by_keyword_view,
                    logout_user, UserRegisterView,)

urlpatterns = [
    path(
        'search_by_keyword',
        search_by_keyword_view,
        name='search_by_keyword'
    ),
    path('', HomeView.as_view(), name='home'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
]
