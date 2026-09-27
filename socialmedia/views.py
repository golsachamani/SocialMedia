from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, request
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from django.http import HttpResponseNotAllowed
import uuid
from django.utils.text import slugify

from . import models, forms


class CommunityList(generic.ListView):
    model = models.Community
    template_name = "community_list.html"
    context_object_name = "communities"


class Home(LoginRequiredMixin, generic.TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        communities = models.Community.owner_or_member(self.request.user)
        ctx["communities"] = communities
        return ctx


class CommunityAdd(LoginRequiredMixin, generic.CreateView):
    model = models.Community
    form_class = forms.Community
    template_name = "community_add.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class CommunityDelete(LoginRequiredMixin, generic.DeleteView):
    model = models.Community
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("home")
    slug_field = "slug"
    slug_url_kwarg = "community_slug"

    def dispatch(self, request, *args, **kwargs):
        community = self.get_object()
        if community.created_by != request.user:
            return HttpResponseForbidden("Only community owned can delete post.")
        if not community.can_be_delete():
            return HttpResponseForbidden("Community has posts.")

        return super().dispatch(request, *args, **kwargs)


class CommunityUpdate(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.Community
    model = models.Community
    template_name = "community_update.html"
    success_url = reverse_lazy("home")
    slug_field = "slug"
    slug_url_kwarg = "community_slug"

    def get_queryset(self):
        user = self.request.user

        return models.Community.objects.filter(created_by=user)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class CommunityDetail(generic.DetailView):
    model = models.Community
    template_name = "community_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        community = ctx["community"]
        ctx["is_member"] = not self.request.user.is_anonymous and (
            community.created_by == self.request.user
            or models.Membership.objects.filter(
                user=self.request.user, community=ctx["community"]
            ).count()
            > 0
        )

        return ctx


class PostAdd(LoginRequiredMixin, generic.CreateView):
    model = models.Post
    form_class = forms.Post
    template_name = "post_add.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.community = models.Community.objects.get(
            slug=self.kwargs.get("community_slug")
        )
        return super().form_valid(form)

    def get_success_url(self):
        community= models.Community.objects.get(slug=self.kwargs.get("community_slug"))
        return community.get_absolute_url()


class PostDetail(generic.DetailView):
    model = models.Post
    template_name = "post_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "post_slug"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        post = self.get_object()
        # فقط کامنت‌های ریشه‌ای (direct replies)
        ctx["comments"] = post.replies().filter(parent=post)
        return ctx


class PostUpdate(LoginRequiredMixin, generic.UpdateView):
    model = models.Post
    form_class = forms.Post
    template_name = "post_update.html"

    def get_object(self, queryset=None):
        return get_object_or_404(
            models.Post,
            slug=self.kwargs["post_slug"],
            community__slug=self.kwargs["community_slug"],
            author=self.request.user,
        )

    def get_success_url(self):
        return self.object.get_grandparent_absolute_url()

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDelete(LoginRequiredMixin, generic.DeleteView):
    model = models.Post
    template_name = "post_delete.html"
    slug_field = "slug"
    slug_url_kwarg = "post_slug"

    def get_queryset(self):
        user = self.request.user
        return models.Post.objects.filter(author=user)

    def get_success_url(self):
        if self.object.parent:
            return self.object.parent.get_grandparent_absolute_url()

        return self.object.community.get_absolute_url()


class CommentAdd(LoginRequiredMixin, generic.View):
    model = models.Post
    form_class = forms.Post

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(
            models.Post,
            slug=self.kwargs.get("post_slug"),
            community__slug=self.kwargs.get("community_slug"),
        )
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(["POST"])

    def post(self, request, *args, **kwargs):
        community_slug = kwargs["community_slug"]
        post_slug = kwargs["post_slug"]

        root_post = get_object_or_404(
            models.Post, slug=post_slug, community__slug=community_slug, parent=None
        )

        parent_id = request.POST.get("parent_id")
        parent = None

        if parent_id:
            parent = get_object_or_404(models.Post, id=parent_id)

        content = request.POST.get("content")

        if content:
            unique_slug = slugify(f"{root_post.slug}-comment-{uuid.uuid4().hex[:6]}")
            models.Post.objects.create(
                community=root_post.community,
                parent=parent or root_post,
                author=request.user,
                title=f"Comment: {content[:20]}",
                content=content,
            )

        return redirect(root_post.get_absolute_url())


class JoinCommunity(LoginRequiredMixin, View):

    def post(self, request, community_slug):
        community = get_object_or_404(models.Community, slug=community_slug)
        models.Membership.objects.get_or_create(
            user=self.request.user,
            community=community,
            defaults={"role": models.Membership.MEMBER},
        )
        return redirect(community.get_absolute_url())


class leaveCommunity(LoginRequiredMixin, View):
    def post(self, request, community_slug):
        community = get_object_or_404(models.Community, slug=community_slug)
        models.Membership.objects.filter(
            user=request.user, community=community
        ).delete()
        return redirect(community.get_absolute_url())


class ToggleVote(LoginRequiredMixin, View):

    def post(self, request, community_slug, post_slug, vote_type):
        value = 1 if vote_type == "up" else -1
        post = get_object_or_404(
            models.Post,
            slug=post_slug,
            community__slug=community_slug,
        )

        vote, created = models.Vote.objects.get_or_create(
            user=request.user,
            post=post,
            defaults={"value": value},
        )

        if not created:
            if vote.value == value:
                vote.delete()
            else:
                vote.value = value
                vote.save()

        return redirect(post.get_grandparent_absolute_url())
