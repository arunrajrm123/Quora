from django.urls import path
from. import views

urlpatterns = [
    path('', views.register_user, name='reg'),
     path('logout/', views.logout, name='logout'),
     path('question/', views.post_question, name='questions'),
      path('home/', views.home, name='home'),
      path("answer-question/<int:id>/", views.answer_question, name="answer_question"),
      path('like-answer/<int:answer_id>/', views.like_answer, name='like_answer'),
]

    
    
