# articles/views.py
from django.contrib.auth.mixins import (
    # Only author can edit and delet views
    LoginRequiredMixin,
    UserPassesTestMixin,
)

from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy

from .models import Article


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "article_list.html"


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = "article_detail.html"


# Add the specific attributes-title and body
# that can be changed.
class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    # I don't want a user change the author, which is why
    # ArticleUpdateView only has the attributes ['title', 'body',]
    fields = (
        "title",
        "body",
    )
    template_name = "article_edit.html"

    # True: allow it. else: throw error
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = "article_delete.html"
    success_url = reverse_lazy("article_list")

    # True: allow it. else: throw error
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


# LoginRequiredMixin: To restrict view access to only logged-in users
class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = "article_new.html"
    # fields = (
    #     "title",
    #     "body",
    #     "author",
    # )
    fields = ("title", "body")

    # The author on a new article should be
    # automatically set to the currently logged-in user.
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
