from django.urls import path
from django.conf.urls import url 
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from . import views

app_name = 'ask'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'), 
    path('questions/', views.QuestionList.as_view(), name='question_list'),
    path('detail/<int:pk>/', views.Question_Detail.as_view(), name='question_detail'),
    path('post/', views.QuestionPost.as_view(), name='question_post'),
    path('comment/create/<int:pk>/', views.CommentCreation.as_view(), name='comment_create'),
    path('reply/create/<int:pk>/', views.ReplyCreation.as_view(), name='reply_create'),

    path('login/', auth_views.LoginView.as_view(template_name='ask/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='ask/home.html'), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]