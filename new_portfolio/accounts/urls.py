from django.urls import path
from . import views
from . views import HomeView

app_name = 'accounts'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('regist', views.regist, name='regist'),
    path('activate_user/<uuid:token>', views.activate_user, name='activate_user') # type: ignore
]
