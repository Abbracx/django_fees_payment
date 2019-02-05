from django.urls import path
from djapp import views

# SET THE NAMESPACE!
app_name = 'djapp'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns = [
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
]
