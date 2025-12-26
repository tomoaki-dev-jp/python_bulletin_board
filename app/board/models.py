from django.db import models

class Thread(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="posts")
    name = models.CharField(max_length=50, default="名無しさん")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
