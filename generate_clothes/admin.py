from django.contrib import admin
from .models import *


class ClothesSubCategoryAdmin(admin.ModelAdmin):
    list_display = ['gender', 'season', 'clothes_category', 'subcategory']


admin.site.register(ClothesCategory)
admin.site.register(ClothesSubCategory, ClothesSubCategoryAdmin)
admin.site.register(StyleCategory)
admin.site.register(Colour)
admin.site.register(CountrySettings)
admin.site.register(Season)

