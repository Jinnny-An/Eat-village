# Generated by Django 3.0.7 on 2022-04-26 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20220426_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeboardimage',
            name='image',
            field=models.ImageField(null=True, upload_to='recipeboard/', verbose_name=''),
        ),
    ]
