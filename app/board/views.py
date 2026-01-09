from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostCreateForm, ThreadCreateForm
from .models import Board, Post, Thread
from .utils import compute_ip_hash, compute_thread_id, link_anchors, render_trip


def _rate_limit(request, key: str, seconds: int) -> bool:
    """True=許可, False=規制"""
    k = f"rl:{key}"
    if cache.get(k):
        return False
    cache.set(k, "1", timeout=seconds)
    return True


def board_list(request):
    boards = Board.objects.order_by("slug")
    return render(request, "board/board_list.html", {"boards": boards})


def thread_list(request, board_slug="vip"):
    board = get_object_or_404(Board, slug=board_slug)

    # スレ立て
    if request.method == "POST":
        # 連投規制（スレ立ては重め）
        ip = getattr(request, "client_ip", "0.0.0.0")
        if not _rate_limit(request, f"thread:{ip}", seconds=10):
            return HttpResponseForbidden("連投規制中（少し待ってね）")

        form = ThreadCreateForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.board = board
            thread.save()
            return redirect("thread_detail", board_slug=board.slug, thread_id=thread.id)
    else:
        form = ThreadCreateForm()

    threads = (
        Thread.objects.filter(board=board, is_deleted=False)
        .order_by("-is_sticky", "-last_bumped_at", "-last_post_at")
    )

    return render(request, "board/thread_list.html", {
        "board": board,
        "threads": threads,
        "form": form,
    })


def thread_detail(request, board_slug: str, thread_id: int):
    board = get_object_or_404(Board, slug=board_slug)
    thread = get_object_or_404(Thread, id=thread_id, board=board, is_deleted=False)

    # レス投稿
    if request.method == "POST":
        ip = getattr(request, "client_ip", "0.0.0.0")
        if not _rate_limit(request, f"post:{thread_id}:{ip}", seconds=3):
            return HttpResponseForbidden("連投規制中（少し待ってね）")

        if not thread.can_post():
            return HttpResponseForbidden("このスレには書き込めません（ロック/落ち/上限）")

        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)

            # name/trip
            display_name, trip = render_trip(post.name, settings.SECRET_KEY)
            post.name = display_name
            post.trip = trip

            # sage判定
            post.is_sage = "sage" in (post.email or "").lower()

            # スレ内連番
            next_no = thread.posts_count + 1
            post.number = next_no

            # ID
            post.poster_id = compute_thread_id(ip=ip, thread_id=thread.id, secret=settings.SECRET_KEY)
            post.ip_hash = compute_ip_hash(ip=ip, secret=settings.SECRET_KEY)
            post.user_agent = (request.META.get("HTTP_USER_AGENT", "") or "")[:255]

            post.thread = thread
            post.save()

            # thread更新
            thread.posts_count = next_no
            thread.last_post_at = post.created_at
            if (not post.is_sage) and thread.can_bump():
                thread.last_bumped_at = post.created_at
            # 1000到達で落ち（閲覧のみ）にする例
            if thread.posts_count >= board.max_posts_per_thread:
                thread.is_archived = True
            thread.save()

            return redirect("thread_detail", board_slug=board.slug, thread_id=thread.id)
    else:
        form = PostCreateForm()

    posts = thread.posts.filter(is_deleted=False)

    # アンカーlink化（テンプレで safe 使う）
    rendered_posts = []
    for p in posts:
        rendered_posts.append({
            "number": p.number,
            "name": p.name,
            "trip": p.trip,
            "created_at": p.created_at,
            "poster_id": p.poster_id,
            "body_html": link_anchors(p.body).replace("\n", "<br>"),
        })

    return render(request, "board/thread_detail.html", {
        "board": board,
        "thread": thread,
        "posts": rendered_posts,
        "form": form,
    })


def dat_view(request, board_slug: str, thread_id: int):
    """2ch風 dat 出力（超簡易）"""
    board = get_object_or_404(Board, slug=board_slug)
    thread = get_object_or_404(Thread, id=thread_id, board=board, is_deleted=False)
    posts = thread.posts.filter(is_deleted=False).order_by("number")

    lines = []
    for p in posts:
        name = p.name
        if p.trip:
            name = f"{name}{p.trip}"
        # 本当の2ch datは区切り等あるけど雰囲気版
        body = p.body.replace("\n", "<br>")
        lines.append(f"{name}<> {p.created_at:%Y/%m/%d %H:%M:%S} ID:{p.poster_id}<> {body}<> {thread.title}")

    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")
