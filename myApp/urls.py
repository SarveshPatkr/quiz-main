from django.urls import path
from . import views
from .views import *

urlpatterns = [
	path('', views.home, name="home"),
	path('create-quiz/', views.create_quiz, name="create-quiz"),
	path('set-quiz/<quiz_id>/', views.set_quiz, name="set-quiz"),
	path('share-quiz/<quiz_id>/', views.share_quiz, name="share-quiz"),
	path('quiz/<quiz_id>/', views.quiz, name="quiz"),
	path('result/<quiz_id>/', views.quiz, name="quiz"),
]