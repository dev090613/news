# articles/admin.py
from django.contrib import admin
from .models import Article, Comment


# class CommentInline(admin.StackedInline):  # To switch to Stackedinline
class CommentInline(admin.TabularInline):
    model = Comment
    # To change the default number of extra field
    extra = 0


class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]
    # stackedinline의 경우 list_display를 각주처리
    list_display = [
        "title",
        "body",
        "author",
    ]


# # To see more information in the admin about article
# class ArticleAdmin(admin.ModelAdmin):
#     list_display = [
#         "title",
#         "body",
#         "author",
#     ]


admin.site.register(Article, ArticleAdmin)
# LEGACY, without ArticleAdmin class
# admin.site.register(Article)

admin.site.register(Comment)
