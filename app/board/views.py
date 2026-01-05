from django.shortcuts import render, get_object_or_404, redirect
from .models import Thread
from .forms import ThreadCreateForm

def index(request):
    if request.method == "POST":
        form = ThreadCreateForm(request.POST)
        if form.is_valid():
            thread = form.save()
            return redirect("thread_detail", thread_id=thread.id)
    else:
        form = ThreadCreateForm()

    threads = Thread.objects.order_by("-created_at")
    return render(request, "board/index.html", {"threads": threads, "form": form})

def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    posts = thread.posts.order_by("created_at")
    return render(request, "board/thread_detail.html", {"thread": thread, "posts": posts})
