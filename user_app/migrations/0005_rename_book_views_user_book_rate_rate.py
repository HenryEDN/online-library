# Generated by Django 3.2 on 2022-05-22 21:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0004_auto_20220522_2059'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_book_rate',
            old_name='book_views',
            new_name='rate',
        ),
    ]
