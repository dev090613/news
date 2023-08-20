# articles/admin.py
from django.contrib import admin
from .models import Article


# To see more information in the admin about article
class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "body",
        "author",
    ]


admin.site.register(Article, ArticleAdmin)
# LEGACY, without ArticleAdmin class
# admin.site.register(Article)
