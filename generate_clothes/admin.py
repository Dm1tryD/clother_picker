from django.contrib import admin
from .models import *


class ClothesCategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'gender']

class ClothesSubCategoryAdmin(admin.ModelAdmin):
    list_display = ['clothes_category', 'subcategory']


admin.site.register(ClothesCategory, ClothesCategoryAdmin)
admin.site.register(ClothesSubCategory, ClothesSubCategoryAdmin)
admin.site.register(StyleCategory)
admin.site.register(Colour)
admin.site.register(CountrySettings)

