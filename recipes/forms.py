from django import forms
from django.forms import ModelForm
from .models import Recipe, Ingredient, Limit, Comment, Menu
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper

# Import recipe scraper https://pypi.org/project/recipe-scrapers/
from recipe_scrapers import scrape_me

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['recipe_name', 'total_time', 'yields', 'instructions', 'image']

class IngredientForm(forms.Form):
    UNIT_CHOICES = [("", "---"),
        ("l", "liter"), 
        ("ml", "milliliter"),
        ("g", "gram"),
        ("mg", "milligram"),
        ("kg", "kilogram"),
        ("oz", "ounce"),
        ("lb", "pound"),
        ("fl", "fluid ounce"),
        ("tsp", "teaspoon"),
        ("tbsp", "tablespoon"),
        ("cup", "cup"),
        ("pint", "pint"),
        ("gal", "gallon"),
        ("pinch", "pinch"),
        ("bunch", "bunch")]

    ingredient_name = forms.CharField(max_length=200)
    quantity = forms.FloatField()
    unit = forms.ChoiceField(choices = UNIT_CHOICES)
    comment = forms.CharField(max_length=100, required=False)

    def clean_quantity(self):
        data = self.cleaned_data['quantity']
        try:
            data = float(data)
        except:
            data = 1.0
        return data


class WebForm(forms.Form):
    url = forms.URLField(max_length=300)

    def clean_url(self):
        data = self.cleaned_data['url']
        try:
            scrape_me(data)
        except:
            try:
                scrape_me(data, wild_mode=True)
            except:
                raise forms.ValidationError("Cannot retrieve recipe from this url")
        return data

class LimitForm(forms.ModelForm):
    class Meta:
        model = Limit
        fields = '__all__'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
