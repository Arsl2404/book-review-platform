from django.urls import path
from .views import (
    BookListCreateAPIView,
    BookRetrieveAPIView,
    AddReviewAPIView,
    BookReviewListAPIView,
    TopRatedBooksAPIView,
    UsersWithMoreThanFiveReviewsAPIView,
    MostActiveReviewerAPIView
)

urlpatterns = [
    # ---------------------------
    # BOOK Endpoints
    # ---------------------------
    path('books/', BookListCreateAPIView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookRetrieveAPIView.as_view(), name='book-retrieve'),

    # ---------------------------
    # REVIEW Endpoints
    # ---------------------------
    path('books/<int:book_id>/review/', AddReviewAPIView.as_view(), name='add-review'),
    path('books/<int:book_id>/reviews/', BookReviewListAPIView.as_view(), name='list-book-reviews'),

    # ---------------------------
    # ANALYTICS / ORM QUERIES
    # ---------------------------
    path('books/top-rated/', TopRatedBooksAPIView.as_view(), name='top-rated-books'),
    path('users/more-than-5-reviews/', UsersWithMoreThanFiveReviewsAPIView.as_view(), name='users-more-than-5-reviews'),
    path('users/most-active/', MostActiveReviewerAPIView.as_view(), name='most-active-reviewer'),
]

