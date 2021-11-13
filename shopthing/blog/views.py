from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

from .models import Article,BlogComment,Tag
# Create your views here.

#
# def blog (request):
#     articles = Article.objects.all()
#     return render(request,'blog.html',{'articles': articles})
#
#
# def single_blog(re):
#     pass
#
#
#



class BlogList(ListView):
    model = Article
    template_name = "blog.html"
    context_object_name = "articles"
    paginate_by = 10

    def get_queryset(self):
        article_qs = super().get_queryset()
        tag_filter = self.request.GET.get('tags', None)
        print(tag_filter)
        if tag_filter:
            article_qs = article_qs.filter(tags__name=tag_filter)
        return article_qs.order_by('created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()

        return context


class BlogDetail(DetailView):
    model = Article
    template_name = "blog-single.html"
    context_object_name = "article"
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()

        return context


def add_comment(request,aid):
    if request.method == 'POST':

        author = request.POST.get('author')
        body = request.POST.get('comment')
        article = Article.objects.filter(id=aid)[0]
        slug = article.slug
        if author:
            BlogComment.objects.create(author=author,body=body,article_id=aid)
        else:
            BlogComment.objects.create(author=request.user.username,body=body,article_id=aid)

        return redirect(reverse('blog-detail',kwargs={'slug': slug}))


