from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Thread, Post
from .serializers import ThreadSerializer, PostSerializer

@api_view(["GET"])
def thread_list_api(request, board_slug):
    threads = Thread.objects.filter(
        board__slug=board_slug,
        is_deleted=False
    ).order_by("-last_bumped_at")
    return Response(ThreadSerializer(threads, many=True).data)

@api_view(["GET"])
def thread_detail_api(request, board_slug, thread_id):
    thread = get_object_or_404(Thread, id=thread_id, board__slug=board_slug, is_deleted=False)
    posts = thread.posts.filter(is_deleted=False).order_by("number")
    return Response({
        "thread": ThreadSerializer(thread).data,
        "posts": PostSerializer(posts, many=True).data,
    })

# ★追加：レス投稿API
@api_view(["POST"])
def post_create_api(request, board_slug, thread_id):
    thread = get_object_or_404(Thread, id=thread_id, board__slug=board_slug, is_deleted=False)

    if not thread.can_post():
        return Response({"detail": "このスレには書き込めません（ロック/落ち/上限）"}, status=status.HTTP_403_FORBIDDEN)

    name = (request.data.get("name") or "名無しさん")[:50]
    email = (request.data.get("email") or "")[:100]
    body = (request.data.get("body") or "").strip()

    if not body:
        return Response({"detail": "本文が空です"}, status=status.HTTP_400_BAD_REQUEST)

    next_no = thread.posts_count + 1

    post = Post.objects.create(
        thread=thread,
        number=next_no,
        name=name,
        email=email,
        body=body,
        is_sage=("sage" in email.lower()),
        # poster_id / trip 等は後でAPI用にも付与できる（まずは最小）
    )

    thread.posts_count = next_no
    thread.last_post_at = post.created_at
    if (not post.is_sage) and thread.can_bump():
        thread.last_bumped_at = post.created_at
    thread.save()

    return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
