from django.urls import path
from . import views
from .views import (QuestionCreateView, QuestionDetailView,
                    QuestionListView, QuestionUpdateView,
                    QuestionDeleteView, CommentCreateView,
                    CommentUpdateView, CommentDeleteView, UserQuestionListView)

app_name = 'quiz'


urlpatterns = [
    path('', views.index, name='devs-home'),
    path('home/', QuestionListView.as_view(), name='quiz-index'),
    path('user/<str:username>/', UserQuestionListView.as_view(), name='user-questions'),
    path('<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
    path('create_new/', QuestionCreateView.as_view(), name='question-create'),
    path('<int:pk>/update/', QuestionUpdateView.as_view(), name='question-update'),
    path('<int:pk>/comment/', CommentCreateView.as_view(), name='question-comment'),
    path('<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('<int:pk>/delete/', QuestionDeleteView.as_view(), name='question-delete'),
    path('about/', views.about, name='devox-about'),
]