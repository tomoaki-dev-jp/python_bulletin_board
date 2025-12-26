from django.shortcuts import render, get_object_or_404
from .models import Thread

def index(request):
    threads = Thread.objects.order_by("-created_at")
    return render(request, "board/index.html", {"threads": threads})

def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    posts = thread.posts.order_by("created_at")
    return render(request, "board/thread_detail.html", {"thread": thread, "posts": posts})
