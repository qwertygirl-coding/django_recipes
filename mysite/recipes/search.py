def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        result_set = set()
        if form.is_valid():
            search = form.cleaned_data['search']
            # find matching ingredient(s)
            ingredients= Ingredient.objects.filter(ingredient_name__icontains=search)
            # find matching recipes from ingredients
            for ing in ingredients:
                recipes = ing.uses.all()
                for recipe in recipes:
                    result_set.add(recipe)
            # find matching recipe names
            names = Recipe.objects.filter(recipe_name__icontains=search) 
            for name in names:
                result_set.add(name)
            # go to random recipe matching search results 
            if form.cleaned_data['dom'] == 'T':
                if result_set:
                    result = random.choice(list(result_set))
                    return HttpResponseRedirect(reverse('recipes:detail', args=(result.id,)))
    else:
        result_set=set()
        form = SearchForm()
    return render(request, 'recipes/search.html', {'form': form, 'result_set': result_set})
