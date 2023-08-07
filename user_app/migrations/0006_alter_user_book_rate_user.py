# Generated by Django 3.2 on 2022-05-22 21:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_app', '0005_rename_book_views_user_book_rate_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_book_rate',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
