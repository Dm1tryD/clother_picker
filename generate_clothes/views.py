from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .models import *
from .forms import UserSettingsForm
from django.views.generic.edit import FormView
from django.views import generic
from django.db.models import Q
from django.db import connection, reset_queries
import time
import functools
from .utils import Clothes


def query_debugger(func):
    """Измеряет кол-во запросов в базу данных django"""
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
    success_url = '/season/'

    def get_form_kwargs(self):

        session_data = {k:v for k,v in self.request.session.items()}
        kwargs = {'data': session_data}
        kwargs.update(super(Settings, self).get_form_kwargs())
        return kwargs

    def form_valid(self, form):

        self.set_user_config(form.cleaned_data)
        return super().form_valid(form)

    def set_user_config(self, user_data):

        for key, value in user_data.items():
            self.request.session[key] = value


class Seasons(generic.ListView):

    model = Season
    template_name = 'generate_clothes/seasons.html'
    context_object_name = 'seasons'

class StylesPage(generic.ListView):

    model = StyleCategory
    template_name = 'generate_clothes/styles.html'
    context_object_name = 'styles'

class Style(generic.ListView):

    model = StyleCategory
    template_name = 'generate_clothes/style_detail.html'

    @query_debugger
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self, **kwargs):
        return super().get_queryset().filter(slug=self.kwargs['slug'])[0]

    def get_context_data(self, **kwargs):

        context = super().get_context_data()
        gender = self.request.session['gender']
        season = self.kwargs['season']
        queryset_style = context['object_list']
        clothes_items_by_style = queryset_style.item.all().filter(
            Q(season__slug=season) | Q(season__slug='demi-season'), gender=gender).\
            values('clothes_category__category_name', 'subcategory', 'subcategory_num')
        colours = [i.colour_id for i in queryset_style.colour.all()]
        user_settings = self.get_user_settings()
        clothes = self.get_clothes_by_style(clothes_items_by_style)
        #items = Clothes(clothes, colours, user_settings).get_items_by_category()
        items = {'clothes': {'jacket': {'subcategory': 'Кожаные куртки', 'name': 'Коричневая кожаная куртка ASOS DESIGN', 'brandName': 'ASOS DESIGN', 'price': '9\xa0590,00 руб.', 'url': 'https://www.asos.com/asos-design/korichnevaya-kozhanaya-kurtka-asos-design/prd/21187196?clr=korichnevyj&colourwayid=60146711', 'img': 'http://images.asos-media.com/products/korichnevaya-kozhanaya-kurtka-asos-design/21187196-1-brown'}, 'sweater': {'subcategory': 'Cвитшоты', 'name': 'Черный свитшот Burton Menswear', 'brandName': 'Burton Menswear', 'price': '1\xa0790,00 руб.', 'url': 'https://www.asos.com/burton-menswear/chernyj-svitshot-burton-menswear/prd/22333796?clr=chernyj-tsvet&colourwayid=60390708', 'img': 'http://images.asos-media.com/products/chernyj-svitshot-burton-menswear/22333796-1-black'}, 'shirt': {'subcategory': 'Рубашки с принтами','name': 'Белая футболка со сплошным логотипом Versace Jeans Couture', 'brandName': 'Versace Jeans', 'price': '28\xa0190,00 руб.', 'url': 'https://www.asos.com/versace-jeans/belaya-futbolka-so-sploshnym-logotipom-versace-jeans-couture/prd/22072056?clr=belyj&colourwayid=60347443', 'img': 'http://images.asos-media.com/products/belaya-futbolka-so-sploshnym-logotipom-versace-jeans-couture/22072056-1-white'}, 'pants': {'subcategory': 'Темные джинсы', 'name': 'Серые узкие джинсы Only & Sons', 'brandName': 'Only & Sons', 'price': '2\xa0490,00 руб.', 'url': 'https://www.asos.com/only-sons/serye-uzkie-dzhinsy-only-sons/prd/22928017?clr=seryj-denim&colourwayid=60436987', 'img': 'http://images.asos-media.com/products/serye-uzkie-dzhinsy-only-sons/22928017-1-greydenim'}, 'shoes': {'subcategory': 'Кроссовки', 'name': 'Черные кроссовки с фактурной отделкой ASOS DESIGN', 'brandName': 'ASOS DESIGN', 'price': '2\xa0390,00 руб.', 'url': 'https://www.asos.com/asos-design/chernye-krossovki-s-fakturnoj-otdelkoj-asos-design/prd/21341710?clr=chernyj-tsvet&colourwayid=60158961', 'img': 'http://images.asos-media.com/products/chernye-krossovki-s-fakturnoj-otdelkoj-asos-design/21341710-1-black'}}}
        context.update(items)
        return context

    def get_clothes_by_style(self, queryset):
        categories = self.get_categories_from_style(queryset)
        clothes = dict()
        for category in categories:
            item = {category: [i['subcategory_num'] for i in queryset if
                                 i['clothes_category__category_name'] == category]}
            clothes.update(item)
        return clothes

    def get_categories_from_style(self, queryset):
        categories = list()
        for category in queryset:
            if category['clothes_category__category_name'] not in categories:
                categories.append(category['clothes_category__category_name'])
        return categories

    def get_user_settings(self):
        country_settings = CountrySettings.objects.get(country=self.request.session['country'])
        user_settings = dict(
            country=country_settings.country,
            currency=country_settings.currency,
            language=country_settings.language,
            store=country_settings.store,
            sweater_size=self.request.session['sweater_size'],
            pants_size=self.request.session['pants_size'],
            shoes_size=self.request.session['shoes_size'],
            gender=self.request.session['gender'],
        )
        return user_settings