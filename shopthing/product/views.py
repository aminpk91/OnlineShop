from django.shortcuts import render,redirect,reverse
from .models import Productbase,Category,Brands,ProductComment

from django.views.generic import ListView, DetailView
from django.db.models import Q


def index(request):
    qs = Productbase.objects.all()
    latest_products = qs.order_by('-added_time')[:8]
    fav_products = qs.order_by('-rate')[:8]
    categories = Category.objects.filter(cat_parent=None)
    return render(request,'index.html', {'products': latest_products,
                                            'fav_products': fav_products,
                                            'cats': categories,
                                            })


class ProductList(ListView):
    model = Productbase
    template_name = "shop.html"
    context_object_name = "products"
    paginate_by = 20

    def get_queryset(self):
        product_qs = super().get_queryset()
        device_filter = self.request.GET.get('device', None)
        cat_filter = self.request.GET.get('cat', None)
        price_min_filter = self.request.GET.get('pmin', None)
        price_max_filter = self.request.GET.get('pmax', None)
        stock_filter = self.request.GET.get('stock', None)
        if stock_filter:
            if stock_filter=='نو':
                product_qs = product_qs.filter(stock=False)
            else:
                product_qs = product_qs.filter(stock=True)
        if device_filter:
            product_qs = product_qs.filter(device__contains=device_filter)
        if cat_filter:
            product_qs = product_qs.filter(category__name__contains=cat_filter)
        if price_min_filter:
            price_min_filter = re.sub("[نامحدود]", "0", price_min_filter)
            price_min_filter=float(re.sub("[a-z A-Z -%,. ]","",price_min_filter))

            pmin = Q(price__gte=price_min_filter)
        else:
            pmin = Q(price__gte=0)
        if price_max_filter:
            price_max_filter = re.sub("[نامحدود]", "100000000000000", price_max_filter)
            price_max_filter = float(re.sub("[a-z A-Z -%,. ]", "", price_max_filter))

            pmax = Q(price__lte=price_max_filter)
        else:
            pmax = Q(price__lte=100000000000000000)
        product_qs = product_qs.filter(pmin & pmax)
        return product_qs.order_by('added_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cats'] = Category.objects.all()
        context['brands'] = Brands.objects.all()
        return context


class ProductDetail(DetailView):
    model = Productbase
    template_name = "product.html"
    context_object_name = "product"
    slug_url_kwarg = 'slug'



def add_comment(request,aid):
    if request.method == 'POST':
        author = request.POST.get('author')
        body = request.POST.get('comment')
        article = Productbase.objects.filter(id=aid)[0]

        slug = article.slug
        if author:
            ProductComment.objects.create(author=author,body=body,article_id=aid)
        else:
            ProductComment.objects.create(author=request.user.username, body=body, article_id=aid)
        return redirect(reverse('product-detail',kwargs={'slug': slug}))