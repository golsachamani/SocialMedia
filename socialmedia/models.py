from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.db.models import Q

User = settings.AUTH_USER_MODEL
# Programming In Django & Python
# programming-in-django-and-python


class Community(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(
        max_length=120, unique=True, default="", null=True, blank=True
    )
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_communities"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"r/{self.name}"

    def get_absolute_url(self):
        return reverse_lazy("community_detail", args=[self.slug])

    @classmethod
    def owner_or_member(cls, user):
        return cls.objects.filter(
            Q(created_by=user) | Q(memberships__user=user)
        ).distinct()

    def can_be_delete(self):
        return not self.post_set.exists()

    def root_posts(self):
        return self.post_set.filter(parent=None)


class Membership(models.Model):
    MEMBER = "member"
    MODERATOR = "moderator"

    ROLE_CHOICES = (
        (MEMBER, "Member"),
        (MODERATOR, "Moderator"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(
        Community, on_delete=models.CASCADE, related_name="memberships"
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "community")

    def __str__(self):
        return f"{self.user} → {self.community}"


class Post(models.Model):
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
    )
    parent = models.ForeignKey(
        "Post",
        on_delete=models.CASCADE,
        related_name="discussions",
        blank=True,
        null=True,
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=120, unique=True)
    content = models.TextField(blank=True)
    url = models.URLField(blank=True)
    score = models.IntegerField(default=0, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy("post_detail", args=[self.community.slug, self.slug])

    def get_grandparent_absolute_url(self):
        if self.parent:
            return self.parent.get_grandparent_absolute_url()
        return self.get_absolute_url()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def replies(self):
        return Post.objects.filter(parent=self)

    def score(self):
        return self.vote_set.aggregate(total=models.Sum("value"))["total"] or 0


class Vote(models.Model):
    UPVOTE = 1
    DOWNVOTE = -1

    VOTE_CHOICES = (
        (UPVOTE, "Upvote"),
        (DOWNVOTE, "Downvote"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)

    value = models.SmallIntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user} voted {self.value}"


class Save(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user} saved {self.post}"


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.user}"
