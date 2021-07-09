from django.urls import path, include
from . import views

app_name = 'recipes'

urlpatterns = [
    # ex: /recipes/
    path('', views.index, name='index'),
    # ex: /recipes/5/
    path('<int:recipe_id>/', views.detail, name='detail'),
    # /recipies/add
    path('add/', views.add, name='add'),
    # /recipies/success
    #/recipes/add_auto
    path('add_auto/', views.add_auto, name='add_auto'),
    #/recipes/search
    path('search/', views.search, name='search'),
    #/recipes/menu
    path('menu/', views.menu, name='menu'),
    #/recipes/food_dom
    path('food_dom/', views.food_dom, name='food_dom'),
]