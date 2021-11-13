from django.contrib import admin
from .models import Tag,Article,Paragraph,BlogComment
# Register your models here.
#admin.site.register(Paragraph)
admin.site.register(Tag)


class ParagraphInline(admin.StackedInline):
    model = Paragraph
    extra = 3


class CommentInline(admin.StackedInline):
    model = BlogComment
    extra = 3

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ParagraphInline,CommentInline]








