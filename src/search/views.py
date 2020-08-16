from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product


class ProductSearchView(ListView):
    template_name = "products/list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = request.GET.get('q', None)
        print(query)
        if query is not None:
            return Product.objects.filter(title__icontains=query)
        else:
            return Product.objects.none()

        '''
        __icontains = field contains this
        __iexact = Field is exactly this

        '''
