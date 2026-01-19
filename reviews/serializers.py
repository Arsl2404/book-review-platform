from rest_framework import serializers
from .models import Book, Review

class BookSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'isbn', 'avg_rating', 'review_count']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    book = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'user', 'book', 'rating', 'review_text', 'created_at']
        read_only_fields = ['user', 'created_at']

class ActiveUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    review_count = serializers.IntegerField()

class MostActiveReviewerSerializer(serializers.Serializer):
    username = serializers.CharField()
    total_reviews = serializers.IntegerField()