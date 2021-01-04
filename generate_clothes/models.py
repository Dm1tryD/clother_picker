from django.db import models

class ClotherCategory(models.Model):
    """Stores categories of all basic clothes"""

    GENDER_CHOISES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    category_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOISES)


    def __str__(self):
        return self.category_name

class SubCategoryClother(models.Model):
    """Stores all the names and id of the subcategory of the main categories"""

    menclother_category = models.ForeignKey(ClotherCategory, on_delete=models.CASCADE)
    subcategory = models.CharField(max_length=255)
    subcategory_id = models.IntegerField(unique=True)

    def __str__(self):
        return f"{self.menclother_category}, {self.subcategory}, {self.subcategory_id}"


class SizeCategory(models.Model):
    """Stores varieties of size categories"""

    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name


class SubCategorySize(models.Model):
    """Stores size according to category"""

    category_name = models.ForeignKey(SizeCategory, on_delete=models.CASCADE)
    size_id = models.IntegerField(unique=True)
    size_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.category_name}, {self.size_name}, Size id: {self.size_id}"


class CustomStyleCategory(models.Model):


    style_name = models.CharField(max_length=255)
    item = models.ManyToManyField('SubCategoryClother', related_name="item")


    def __str__(self):
        return self.style_name