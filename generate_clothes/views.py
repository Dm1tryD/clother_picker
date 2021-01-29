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
    success_url = '/'

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


class Home(generic.ListView):

    model = Season
    template_name = 'generate_clothes/home.html'
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
        context.update(Clothes(clothes, colours, user_settings).get_items_by_category())
        return context

    def get_clothes_by_style(self, queryset):
        categories = self.get_categories_from_style(queryset)
        clothes = dict()
        for subcategory in categories:
            item = {subcategory: [i['subcategory_num'] for i in queryset if
                                 i['clothes_category__category_name'] == subcategory]}
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