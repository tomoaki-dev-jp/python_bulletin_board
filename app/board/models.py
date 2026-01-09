from django.db import models
from django.utils import timezone

class Board(models.Model):
    slug = models.SlugField(unique=True)  # it, news, vip...
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)

    # 2ch風：レス数制限など板ごと設定
    max_posts_per_thread = models.PositiveIntegerField(default=1000)
    bump_limit = models.PositiveIntegerField(default=500)  # ここ超えるとsageじゃなくても上がらない

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.slug} - {self.name}"


class Thread(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="threads")
    title = models.CharField(max_length=200)

    # 管理系
    is_sticky = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)  # dat落ち相当（閲覧のみ）
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    last_post_at = models.DateTimeField(default=timezone.now)
    last_bumped_at = models.DateTimeField(default=timezone.now)

    posts_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def can_bump(self) -> bool:
        return self.posts_count < self.board.bump_limit

    def can_post(self) -> bool:
        return (not self.is_locked) and (not self.is_archived) and (self.posts_count < self.board.max_posts_per_thread)


class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="posts")
    number = models.PositiveIntegerField()  # 1,2,3...

    name = models.CharField(max_length=50, default="名無しさん")
    trip = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=100, blank=True, default="")
    body = models.TextField()

    # 2ch風ID/ログ
    poster_id = models.CharField(max_length=12, blank=True, default="")  # ID:XXXXXXXX
    ip_hash = models.CharField(max_length=64, blank=True, default="")
    user_agent = models.CharField(max_length=255, blank=True, default="")

    is_sage = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("thread", "number")]
        ordering = ["number"]

    def __str__(self):
        return f"{self.thread_id}#{self.number} {self.name}"


class Report(models.Model):
    """通報（削除・規制の判断材料）"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reports")
    reason = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
