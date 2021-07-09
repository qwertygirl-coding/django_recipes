# Generated by Django 3.2.4 on 2021-06-25 11:37

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe_name', models.CharField(max_length=200)),
                ('url', models.URLField(blank=True, default='', max_length=300)),
                ('total_time', models.SmallIntegerField(blank=True, default=0, help_text='in minutes')),
                ('yields', models.CharField(blank=True, default='', max_length=200)),
                ('instructions', models.TextField()),
                ('image', models.URLField(blank=True, default='', help_text='optional link to image', max_length=300)),
                ('host', models.CharField(blank=True, default='', max_length=200)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date added')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe_Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(blank=True, default=0.0)),
                ('unit', models.CharField(blank=True, default='', max_length=200)),
                ('comment', models.CharField(blank=True, default='', max_length=200)),
                ('original_string', models.CharField(max_length=200)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe')),
            ],
        ),
        migrations.AddField(
            model_name='ingredient',
            name='uses',
            field=models.ManyToManyField(through='recipes.Recipe_Ingredient', to='recipes.Recipe'),
        ),
    ]
