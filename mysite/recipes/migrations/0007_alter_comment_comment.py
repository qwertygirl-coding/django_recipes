# Generated by Django 3.2.4 on 2021-07-03 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_alter_comment_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(blank=True, default='', verbose_name='comments'),
        ),
    ]
