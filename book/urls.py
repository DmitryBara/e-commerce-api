from django.urls import path
from .views import BookDetail, BookList

# /api/book/
urlpatterns = [
    path('all/', BookList.as_view()),
    path('<int:book_id>/', BookDetail.as_view())
]