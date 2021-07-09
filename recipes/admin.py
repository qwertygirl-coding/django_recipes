from django.contrib import admin

# Register your models here.
from .models import Recipe, Ingredient, Recipe_Ingredient, Menu, Comment

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Recipe_Ingredient)
admin.site.register(Menu)
admin.site.register(Comment)