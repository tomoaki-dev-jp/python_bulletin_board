from rest_framework import serializers
from .models import Thread, Post

class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = [
            "id",
            "title",
            "posts_count",
            "created_at",
            "last_post_at",
            "is_sticky",
            "is_archived",
        ]

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "number",
            "name",
            "trip",
            "poster_id",
            "body",
            "created_at",
        ]
