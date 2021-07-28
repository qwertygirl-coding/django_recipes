# Mary's Recipe Box
### Video Demo:  <URL HERE>
### Description:
Mary's Recipe box is a website for recipies. Users can add recipes to the site as well as using previously added recipies. A user can add a recipe automatically from another site on the web. They can also manuallly add their own recipies. In additon, users can write, save, and edit comments on each recipe. Finally, users can add or remove recipes to their own menus. A shopping list is generated based on the ingredients in all of the user's menu recipes. These ingredient's amounts are converted to metric if possible and added together to generate the shopping list. 

#### Django
This website is created using Django and hosted on Heroku. I decided to switch from Flask to Django early on in working on this project. The reason for this is because of the way that Django can support databases and forms. Since the websites functions involve adding to and changing database items using user form input, Django seemed like a better solution even though we learned Flask in class. I followed the tutorial on the Django documentation in order to learn how to do basic projects. For more advanced or complicted issues, I was able to find answers on StackExchange or Youtube tutorials. Learning a new framework outside of the course was challenging, but it gave me confidence that I can do it with other frameworks in the future as needed.

##### models.py
In Django models are used to manage the database. They can be used with many types of databases. I originally used SQLite in development. However, Heroku uses Postgres, so I needed to switch to Postgres for production. This points to a benefit of using Django. While switching databeses, I didn't have to change my Django code. Django takes care of actually creating, deleting, updating, and searching the database using their code as a go-between.

For my database, I used a few different tables represented in Django as models. 

###### Recipe
The foundational model is the recipe. This stores recipe name, instructions, yield, time, publication date, source website and image (if applicable) for each recipe on the site.

###### Ingredient
Each ingredient name is stored in the ingredient model with a many-to-many link to recipes that require that ingredient.

###### Recipe_Ingredient
Since each recipe has many ingredients and the same ingredient can be included in many recipes, I used a many-to-many relationship reflected in the recipe-ingredient model. One complication here is that there is additional information that needs to be stored. Besides which ingredients are connected with which recipes and vice-versa, each recipe will require different amounts and quantites of those ingredients. In Django, this is accomplished by a through table, here the recipe-ingredient model. This stores, for each recipe ingredient pairing, the quantity, units, comments, and the original string. 

###### Menu
This model stores the recipes in each user's menu. Each user has one menu, but the menu can contain many recipes so users are one-to-one and recipes are many-to-one.


###### Comment
This model stores a user's comments on recipes. The comment model includes the user and recipe ids as foreign keys as well as the text of the comment. 


##### forms.py
Django allows for forms to be generated from models making it easier to generate forms, clean them, and use the input to modify those models. However, I also added additional forms. 

###### RecipeForm
This form is used when users manually input their own recipes. That input is used later in the add view to create a new Recipe object using the Recipe model.

###### IngredientForm
This is another form used to manually input recipes. For each ingredient, the user fills out a separate version of this form that asks for the ingredient name, quantity, a selection from the choices of accepted unit, and optionally a comment. Since the package I used to parse the ingredients scraped from the web, parse-ingredient (discussed below), returns quantities as floats, the clean function for this form insures that integer inputs are converted to floats. This form is used to create Ingredient and Recipe_Ingredient objects. (More detail when I discuss the add view later.)

###### WebForm
This form is not connected to any model, but is used for users to enter the url of a recipe to be automatically added by scraping the web. The form's clean method checks that the url can be scraped using my method, otherwise the user will be shown an error message. This form is used in the add_auto view to be discussed below.

###### CommentForm
This form is connected to the Comment model. It allows users to add or edit a comment on each recipe in that recipe's detail view discussed below.

##### views.py
This file contains the bulk of the work on this project. In Django, each webpage is dynamically constructed using a view function. I will go over each in more detail below.

###### index
This view generates the homepage of the site. 


#### Heroku
I decided to host this project on Heroku because it offers free website hosting as well as database hosting. While it took much more work to host the site on Heroku than I anticipated, it offers scalability to my project in case I wanted to make improvements in the future requiring more features. 

#### Bootstrap
I used Bootstrap v.5 to style the website. Even though we learned Bootstrap v.4 in class, since the new vesrion had been released in the meantime, I went with that. It has some changes vs v.4 but it was easy to follow the new changes using their documentation.

Bootstrap's card layout was ideal for my project's homepage. It allowed me to list recently added recipes with photos and links to the recipe details in a visually appealing manner. Bootstrap's navbar was used to create a top navbar. Integrating links and search in a central location for easy navigation. I also used some of bootstraps new icons to give more interest to my website's design. 

#### Other Libraries

##### django-crispy-forms
I used django-crispy-forms to improve the look of my forms. As mentioned earlier, my project involves the use of many kinds of forms throughout the site. In fact, every page includes some sort of form. Originally, I was unsatisfied with the appearance of these forms. The form styling provided by bootstrap did not integrate easily with the Django method of creating forms. Because of this, I searched for a Django specific solution. Using the `{% crispy %}` tag immeditaly made the forms look more uniform across the site. I only scratched the surface with the simplest usage of this library, but as I improve this site in the future, I look forward to exploring the additional features. 

##### django-heroku
I used the django-heroku package to automate and streamline the transition to hosting the site on Heroku. Following the Mozilla tutorial and using this package helped me with a task that seemed impossible given my current level after solely reading the Heroku tutorial. From this, I learned the skill of seeking out additional sources of information when I am stuck on a problem. I'm discovering that often others have faced similar problems and have created a solution. There will be more examples of this as we go on to the other libraries and packages I used. The other packages listed in requirements.txt were also used to facilitate the move to hosting the Django site on Heroku. I will not discuss them individually here.

##### recipe-scrapers
This package can scrape recipes from many popular recipe sites and blogs. You input the URL of the site and it returns the title, ingredients, instructions, total time, yield, images, and other information contained at that URL. I used this to form the basis for adding recipes from the web to my own database. 

##### parse-ingredient
I used this package in conjunction with recipe-scrapers. After scraping the ingredient information for a recipe with recipe-scrapers, I could input it to parse ingredient to further break it down into ingredient name, quantity, unit, and any comments. I slightly improved on parse-ingredient's output by cleaning the ingredient name using Regex. This was important since only items with exactly matching ingredient names will be added together on the shopping list. There is a lot of room for improvement in this area. For example, including plurals of ingredient names and recognizing more types of measurements like 'can' and 'bottle'. This would be a good task for the future to learn more about natural language processing.

##### nltk
This package was used to split instructions into separate steps. Running a recipe URL through recipe-scraper gives the ingredients as a single text string. Nltk was used to split the string by sentences. This made the display page for each recipe easier to read. My plan was to use this simple feature of nltk as a start in natural language processing to be expanded on more in the future. While this worked in development, I could not get it to work once moving to Heroku. This is a package that I want to learn in the future as I am very interested in natural language processing. This current project is a good jumping off point for that in the future. But, as of now, I had to abandon this feature of my website, leaving it for a future version outside of this course. 

This was the most serious bug that I had to deal with when transitioning my project from development to  production. In order to fix this issue, I learned a valuable lesson. I added a fail-safe to my views.py details function to display the entire instructions string as step 1 if the nltk splitting failed. This way, the core functionality of my site is not affected while I work out the issue. In the future, it would be a good idea to be proactive and consider how to maintain core functionality if some additional feature fails for whatever reason. Especially as a project gets more complicated. 

##### helpers.py
This is a file of helper functions that I created. There were 2 functions:
- `recipe_to_dict`
- `metric_converter`

###### `recipe_to_dict`:
This function takes a URL as input. If the URL links to a recipe on one of the sites supported by recipe-scrapers, it returns a dictionary containing the information scraped from the URL. If recipe-scrapers fails for any reason (invalid URL, otherwise unparsable) the function returns None. Additionally, the ingredient list provided by recipe-scrapers is converted into it's own dictionary nested in the recipe's dictionary. This is accomplished by passing each ingredient string in the list to parse-ingredient. This function is one of the most important functions in my project. It takes a user provided URL of a recipe to add to the site and converts it into a dictionary format that can then be added to the project's Django models that store recipes and ingredients. 

###### `metric-converter`:
This function takes any measurement units and converts them to metric if possible, necessary. If an imperial measurement is input to the function, it is returned converted to the appropriate metric unit. Otherwise, it is returned unchanged. This is used to improve the shopping list. For example, suppose one recipe on a user's menu calls for 1 tsp of salt and another recipe calls for 5 ml. Without this function, these amounts would not be added together on the user's shopping list. Applying metric-converter to each ingredient amount will convert the first measurement to 5 ml. Then the quantities in mls can be added together as one item on the shopping list (10 ml). This is a small step towerds improving the shopping list feature. While, as mentioned above, this feature is the weakest, I think that by continually making small improvements where possible, it can be improved over time. 

