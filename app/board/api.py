from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Thread, Post
from .serializers import ThreadSerializer, PostSerializer
from .utils import compute_thread_id, compute_ip_hash, render_trip


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


@api_view(["POST"])
def post_create_api(request, board_slug, thread_id):
    thread = get_object_or_404(Thread, id=thread_id, board__slug=board_slug, is_deleted=False)

    if not thread.can_post():
        return Response({"detail": "このスレには書き込めません（ロック/落ち/上限）"}, status=status.HTTP_403_FORBIDDEN)

    raw_name = (request.data.get("name") or "名無しさん")
    email = (request.data.get("email") or "")[:100]
    body = (request.data.get("body") or "").strip()

    if not body:
        return Response({"detail": "本文が空です"}, status=status.HTTP_400_BAD_REQUEST)

    display_name, trip = render_trip(raw_name, settings.SECRET_KEY)
    is_sage = ("sage" in email.lower())

    next_no = thread.posts_count + 1

    ip = request.META.get("REMOTE_ADDR", "") or "0.0.0.0"
    ua = (request.META.get("HTTP_USER_AGENT", "") or "")[:255]

    poster_id = compute_thread_id(ip=ip, thread_id=thread.id, secret=settings.SECRET_KEY)
    ip_hash = compute_ip_hash(ip=ip, secret=settings.SECRET_KEY)

    post = Post.objects.create(
        thread=thread,
        number=next_no,
        name=display_name[:50],
        trip=trip,
        email=email,
        body=body,
        is_sage=is_sage,
        poster_id=poster_id,
        ip_hash=ip_hash,
        user_agent=ua,
    )

    thread.posts_count = next_no
    thread.last_post_at = post.created_at
    if (not is_sage) and thread.can_bump():
        thread.last_bumped_at = post.created_at
    if thread.posts_count >= thread.board.max_posts_per_thread:
        thread.is_archived = True
    thread.save()

    return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
