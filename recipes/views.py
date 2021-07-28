from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Max
from django.core.exceptions import SuspiciousOperation 

from .models import Recipe, Ingredient, Recipe_Ingredient, Menu, Limit, Comment
from .forms import RecipeForm, IngredientForm, WebForm, CommentForm

# for handeling scraped recipe info
from .helpers import recipe_to_dict, metric_converter
import random

# Create your views here.
def index(request):
    latest_recipe_list = Recipe.objects.order_by('-pub_date')[:6]
    context = {'latest_recipe_list': latest_recipe_list,}
    return render(request, 'recipes/index.html', context)

def detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredient_list = Recipe_Ingredient.objects.filter(recipe=recipe)
    # split instructions into steps by sentences
    try:
        instruction_list = sent_tokenize(recipe.instructions) 
    except:
        instruction_list = [recipe.instructions]
    # menu and comment forms for logged in user
    if request.user.is_authenticated:
        # get comment if already exists
        if Comment.objects.filter(user=request.user, recipe = recipe):
            comment = Comment.objects.get(user=request.user, recipe = recipe)
        else:
            comment = Comment(user=request.user, recipe=recipe)
        # initial form
        comment_form = CommentForm(instance = comment)
        menu_form = True
        # process submitted forms
        if request.method == 'POST':
            # comment form 
            if 'save_comment' in request.POST:
                comment_form = CommentForm(request.POST, instance = comment)
                if comment_form.is_valid():
                    comment_form.save()
            # menu form
            if 'save_menu' in request.POST:
                if Menu.objects.filter(user=request.user):
                    menu = Menu.objects.get(user=request.user)    
                else:
                    menu = Menu(user=request.user)
                    menu.save()
                menu.menu.add(recipe)
                messages.success(request, "Added to menu!")           
        context = {'recipe': recipe, 'ingredient_list': ingredient_list, 'instruction_list': instruction_list, 'comment_form': comment_form, 'menu_form': menu_form}
    # no menu or comment form if user not logged in
    else:
        context = {'recipe': recipe, 'ingredient_list': ingredient_list, 'instruction_list': instruction_list}
    return render(request, 'recipes/detail.html', context)

@login_required
def menu(request):
    user = request.user
    menu = Recipe.objects.filter(menu__user=user)
    # remove recipe from menu
    if request.method == "POST":
        for item in request.POST:
            if 'remove' in item:
                try:
                    remove_recipe = int(item.strip('remove_'))
                    remove_menu = Menu.objects.get(user=user)
                    remove_menu.menu.remove(remove_recipe)
                except:
                    raise SuspiciousOperation('Something went wrong.')

    # generate shopping list dictionary
    shopping_dict = {}
    for recipe in menu:
        ingredients = Recipe_Ingredient.objects.filter(recipe = recipe.pk)
        for item in ingredients:
            ingredient = Ingredient.objects.get(pk=item.ingredient_id)
            name = ingredient.ingredient_name
            # get current amounts of ingredient or create new dictionary
            i_dict = shopping_dict.get(name, {})
            quantity = item.quantity
            unit = item.unit
            # convert to metric
            q,u = metric_converter(quantity, unit)
            old_q = i_dict.get(u, 0)
            new_q = old_q + q
            i_dict.update({u: new_q})
            shopping_dict.update({name: i_dict})
    return render(request, 'recipes/menu.html', {'menu': menu, 'shopping_dict': shopping_dict})


def search(request):
    recipe_search = request.GET.get('search')
    result_set = set()
    if recipe_search:
        # find matching ingredient(s)
        ingredients= Ingredient.objects.filter(ingredient_name__icontains=recipe_search)
        # find matching recipes from ingredients
        for ing in ingredients:
            recipes = ing.uses.all()
            for recipe in recipes:
                result_set.add(recipe)
        # find matching recipe names
        names = Recipe.objects.filter(recipe_name__icontains=recipe_search) 
        for name in names:
            result_set.add(name)
        if not result_set:
            messages.warning(request, "Your search didn't return any results.")
            return HttpResponseRedirect(reverse('recipes:index'))
    else:
        messages.warning(request, "Please enter a search term.")
        return HttpResponseRedirect(reverse('recipes:index'))
    return render(request, 'recipes/search.html', {'result_set': result_set})

def food_dom(request):
    m = Recipe.objects.all().aggregate(Max('id'))
    end = m['id__max']
    while True:
        result = random.randint(0,end)
        if Recipe.objects.filter(id=result):
            return HttpResponseRedirect(reverse('recipes:detail', args=(result,)))

#def limits(request):
    #userprofile_form = UserProfileForm(request.POST if request.POST else None, instance = UserProfile.objects.get(user=request.user))


@login_required
def add(request):
    IngredientFormSet = formset_factory(IngredientForm, min_num=1, validate_min=True)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        formR = RecipeForm(request.POST)
        formset1 = IngredientFormSet(request.POST, prefix='fs1')
        # check if valid
        if formR.is_valid() and formset1.is_valid():
            # save recipe or if already exists, edit
            r = formR.save()

            #process ingredient data for each ingredient
            for form in formset1:
                ingredient_name = form.cleaned_data['ingredient_name']
                # create ingredient if doesn't exist
                if Ingredient.objects.filter(ingredient_name=ingredient_name): 
                    ing = Ingredient.objects.get(ingredient_name=ingredient_name)
                else:
                    ing = Ingredient.objects.create(ingredient_name=ingredient_name)

                #create Recipe_Ingredients 
                quantity = form.cleaned_data['quantity']
                unit = form.cleaned_data['unit']
                try:
                    comment = form.cleaned_data['comment']
                    original_string = f'{quantity} {unit} {ingredient_name} {comment}'
                except: 
                    comment = ''
                    original_string = f'{quantity} {unit} {ingredient_name}'
                ingredient_details = Recipe_Ingredient(recipe=r, ingredient = ing, quantity=quantity, unit=unit, comment=comment, original_string=original_string)              
            # redirect to a new URL:
            messages.success(request, 'Recipe added!')
            return HttpResponseRedirect(reverse('recipes:detail', args=(r.id,)))
    # if a GET (or any other method) we'll create a blank form
    else:
        formR = RecipeForm()
        formset1 = IngredientFormSet(prefix='fs1')

    return render(request, 'recipes/add.html', {'formR': formR, 'formset1': formset1})

@login_required
def add_auto(request):
    if request.method == 'POST':
        form = WebForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            # scrape info into dictionary
            recipe_dict = recipe_to_dict(url)
            ingredient_list = recipe_dict.pop('ingredients')

            # save recipe object to db (if not already existing)
            if Recipe.objects.filter(url=url): 
                r = Recipe.objects.get(url=url)
            else:
                r = Recipe(**recipe_dict)
                r.save()

            # save each ingredient
            for ingredient_dict in ingredient_list:
                ingredient_name = ingredient_dict['ingredient_name']
                # create ingredient if doesn't exist
                if Ingredient.objects.filter(ingredient_name=ingredient_name): 
                    ing = Ingredient.objects.get(ingredient_name=ingredient_name)
                else:
                    ing = Ingredient.objects.create(ingredient_name=ingredient_name)

                #create Recipe_Ingredients if not exist
                original_string = ingredient_dict['original_string']
                if Recipe_Ingredient.objects.filter(recipe=r, ingredient = ing, original_string=original_string):
                    pass
                else:
                    quantity = ingredient_dict['quantity']
                    unit = ingredient_dict['unit']
                    comment = ingredient_dict['comment']
                    ingredient_details = Recipe_Ingredient(recipe=r, ingredient = ing, quantity=quantity, unit=unit, comment=comment, original_string=original_string)              
                    ingredient_details.save()
            messages.success(request, 'Recipe added!')
            return HttpResponseRedirect(reverse('recipes:detail', args=(r.id,)))
    else:
        form = WebForm()
    return render(request, 'recipes/add_auto.html', {'form': form})