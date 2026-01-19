from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Avg, Count

from .models import Book, Review
from .serializers import BookSerializer, ReviewSerializer, ActiveUserSerializer, MostActiveReviewerSerializer


# ---------------------------
# BOOK APIs
# ---------------------------

class BookListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: List all books
    POST: Create a new book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookRetrieveAPIView(generics.RetrieveAPIView):
    """
    GET: Retrieve a single book by ID
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# ---------------------------
# REVIEW APIs
# ---------------------------

class AddReviewAPIView(generics.CreateAPIView):
    """
    POST: Add a review to a book
    Constraint: A user can review a book only once
    """
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        book_id = self.kwargs['book_id']
        user = self.request.user

        # Check if user already reviewed this book
        if Review.objects.filter(book_id=book_id, user=user).exists():
            raise ValidationError("You have already reviewed this book.")

        serializer.save(user=user, book_id=book_id)


class BookReviewListAPIView(generics.ListAPIView):
    """
    GET: List all reviews for a given book
    Sorted by highest rating first
    Paginated
    """
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can view reviews

    def get_queryset(self):
        return Review.objects.filter(
            book_id=self.kwargs['book_id']
        ).select_related('user').order_by('-rating')


# ---------------------------
# ANALYTICS / TASK-SPECIFIC QUERIES
# ---------------------------

class TopRatedBooksAPIView(generics.ListAPIView):
    """
    GET: Top 3 books with highest average rating
    Includes avg_rating and review_count
    """
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        ).order_by('-avg_rating')[:3]


class UsersWithMoreThanFiveReviewsAPIView(generics.ListAPIView):
    """
    GET: All users who reviewed more than 5 books
    Returns username and review count
    """
    serializer_class = ActiveUserSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return User.objects.annotate(
            review_count=Count('reviews')
        ).filter(review_count__gt=5)

class MostActiveReviewerAPIView(generics.RetrieveAPIView):
    """
    GET: User with the maximum number of reviews
    Returns username and total_reviews
    """
    serializer_class = MostActiveReviewerSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        user = User.objects.annotate(
            review_count=Count('reviews')
        ).order_by('-review_count').first()

        if not user:
            raise ValidationError("No reviews found")

        # Return a simple dict, serializer will handle it
        return {
            "username": user.username,
            "total_reviews": user.review_count
        }