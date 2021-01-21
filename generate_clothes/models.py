from django.db import models
from django.urls import reverse

from django.utils.text import slugify

def gen_slug(s):
    new_slug = slugify(s.lower().replace(' ','-'), allow_unicode=True)
    return new_slug


class ClothesCategory(models.Model):
    """Stores categories of all basic clothes"""

    GENDER_CHOISES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    category_name = models.CharField(max_length=255, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOISES)


    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name =  "Clothes category"
        verbose_name_plural  = "Clothes categories"

class ClothesSubCategory(models.Model):
    """Stores all the names and id of the subcategory of the main categories"""

    clothes_category = models.ForeignKey(ClothesCategory, on_delete=models.CASCADE, related_name="clothes_category")
    subcategory = models.CharField(max_length=255)
    subcategory_num = models.IntegerField(unique=True)

    def __str__(self):
        return f"{self.clothes_category.category_name}, {self.subcategory},"

    class Meta:
        verbose_name =  "Clothes subcategory"
        verbose_name_plural  = "Clothes subcategories"


class StyleCategory(models.Model):
    """Stores user-created clothing styles"""

    style_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    item = models.ManyToManyField('ClothesSubCategory', related_name="item")
    colour = models.ManyToManyField('Colour', related_name="colour")


    def __str__(self):
        return self.style_name


    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = gen_slug(self.style_name)
        super().save(*args, *kwargs)


    def get_absolute_url(self):
        return reverse('show_style', kwargs={"slug": self.slug})


    class Meta:
        verbose_name =  "Style category"
        verbose_name_plural  = "Style categories"


class Colour(models.Model):
    """Colours id"""

    colour_name = models.CharField(max_length=255)
    colour_id = models.IntegerField(unique=True)

    def __str__(self):
        return f"{self.colour_id} - {self.colour_name}"

class CountrySettings(models.Model):


    country = models.CharField(max_length=3, unique=True)
    currency = models.CharField(max_length=3)
    language = models.CharField(max_length=7)
    store = models.CharField(max_length=5)

    def __str__(self):
        return self.country
