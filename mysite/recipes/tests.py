import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Recipe


# Create your tests here.
class RecipeModelTests(TestCase):

    def test_was_published_recently_with_future_recipe(self):
        """
        was_published_recently() returns False for recipes whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_recipe = Recipe(pub_date=time)
        self.assertIs(future_recipe.was_published_recently(), False)

    def test_was_published_recently_with_old_recipe(self):
        """
        was_published_recently() returns False for recipes whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_recipe = Recipe(pub_date=time)
        self.assertIs(old_recipe.was_published_recently(), False)

    def test_was_published_recently_with_recent_recipe(self):
        """
        was_published_recently() returns True for recipes whose pub_date
        is within the last day
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_recipe = Recipe(pub_date=time)
        self.assertIs(recent_recipe.was_published_recently(), True)

def create_recipe(recipe_name):
    time = timezone.now()
    return Recipe.objects.create(recipe_name=recipe_name, pub_date=time)

class RecipeIndexViewTests(TestCase):
    def test_no_recipes(self):
        """
        If no recipes exist, an appropriate message is displayed
        """
        response = self.client.get(reverse('recipes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No recipes currently available.")

        self.assertQuerysetEqual(response.context['latest_recipe_list'], [],)

    def test_two_recipes(self):
        """
        The recipes index page may display multiple questions
        """
        recipe1 = create_recipe('Test Recipe 1')
        recipe2 = create_recipe('Test Recipe 2')

        response = self.client.get(reverse('recipes:index'))
        self.assertQuerysetEqual(response.context['latest_recipe_list'], [recipe2, recipe1],)

    def test_seven_recipes(self):
        """
        The recipes index should only show most recent 6 recipies.
        """
        recipe1 = create_recipe('Test Recipe 1')
        recipe2 = create_recipe('Test Recipe 2')
        recipe3 = create_recipe('Test Recipe 3')
        recipe4 = create_recipe('Test Recipe 4')
        recipe5 = create_recipe('Test Recipe 5')
        recipe6 = create_recipe('Test Recipe 6')
        recipe7 = create_recipe('Test Recipe 7')

        response = self.client.get(reverse('recipes:index'))
        self.assertQuerysetEqual(response.context['latest_recipe_list'], [recipe7, recipe6, recipe5, recipe4,
            recipe3, recipe2],)


