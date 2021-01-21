from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponse
from .models import *
from .forms import UserSettingsForm
from django.views.generic.edit import FormView
from django.views import generic
from django.db import connection, reset_queries
import time
import functools
from .utils import Clothes




def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()

        start_queries = len(connection.queries)

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        end_queries = len(connection.queries)

        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {end_queries - start_queries}")
        print(f"Finished in : {(end - start):.2f}s")
        return result

    return inner_func

class Settings(FormView):


    template_name = 'generate_clothes/settings.html'
    form_class = UserSettingsForm
    success_url = '/'

    def get_form_kwargs(self):

        kwargs = {'data': self.request.session.get('form_data', None)}
        kwargs.update(super(Settings, self).get_form_kwargs())
        return kwargs

    def form_valid(self, form):
        self.set_user_config(form.cleaned_data)
        return super().form_valid(form)

    def set_user_config(self, user_data):

        for key,v in user_data.items():
            self.request.session[key] = v


class Home(generic.ListView):
    model = StyleCategory
    template_name = 'generate_clothes/home.html'
    context_object_name = 'styles'



@query_debugger
def show_style(request, slug):


    country_settings = CountrySettings.objects.get(country=request.session['country'])
    user_settings = dict(
        country = country_settings.country,
        currency = country_settings.currency,
        language = country_settings.language,
        store = country_settings.store,
        clothes_size = request.session['clothes_size'],
        shoes_size = request.session['shoes_size'],
        gender = request.session['gender'],
    )


    style = StyleCategory.objects.filter(slug=slug).prefetch_related('item__clothes_category', 'colour')[0]
    categories = list()
    for category in style.item.all():
        category_name = category.clothes_category.category_name
        if category_name not in categories:
            categories.append(category_name)

    clothes = dict()
    for subcategory in categories:
        item = {subcategory:[i.subcategory_num for i in style.item.all() if i.clothes_category.category_name == subcategory]}
        clothes.update(item)


    colours = [i.colour_id for i in style.colour.all()]

    context = Clothes(clothes, colours, user_settings).get_items_by_category()
    context.update({'style':style})
    return render(request, 'generate_clothes/style_detail.html', context=context)
