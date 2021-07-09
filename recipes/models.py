from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

from .helpers import metric_converter

# Create your models here.
class Recipe(models.Model):
    recipe_name = models.CharField(max_length=200)
    url = models.URLField(max_length=300, blank=True, default='')
    total_time = models.SmallIntegerField(blank=True, default=0, help_text='in minutes')
    yields = models.CharField(max_length=200, blank=True, default='')
    instructions = models.TextField()
    image = models.URLField(max_length=300, blank=True, default='', help_text='optional link to image')
    host = models.CharField(max_length=200, blank=True, default='')
    pub_date = models.DateTimeField('date added', default=timezone.now)

    def __str__(self):
        return self.recipe_name
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now 

class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=200)
    uses = models.ManyToManyField(Recipe, through='Recipe_Ingredient')

    def __str__(self):
        return self.ingredient_name

class Recipe_Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(blank=True, default=1.0)
    unit = models.CharField(max_length=200, blank=True, default='')
    comment = models.CharField(max_length=200, blank=True, default='')
    original_string = models.CharField(max_length=200)

    def __str__(self):
        return self.original_string


class Menu(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    menu = models.ManyToManyField(Recipe)

class Limit(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    limit_ingredient = models.ManyToManyField(Ingredient)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, default='', verbose_name="my comments")