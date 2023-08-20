# articles/views.py
from django.contrib.auth.mixins import (
    # Only author can edit and delet views
    LoginRequiredMixin,
    UserPassesTestMixin,
)

from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy, reverse


from .models import Article
from .forms import CommentForm


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "article_list.html"


# class ArticleDetailView(LoginRequiredMixin, DetailView):
class CommentGet(DetailView):
    model = Article
    template_name = "article_detail.html"

    def get_context_data(self, **kwargs):
        """
        Pull all existing information into the context using super()
        Add the variable name <form> with the value of commentForm()
        return updated context
        """
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


class CommentPost(SingleObjectMixin, FormView):
    model = Article
    form_class = CommentForm
    template_name = "article_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        article = self.object
        return reverse("article_detail", kwargs={"pk": article.pk})


class ArticleDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)


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
