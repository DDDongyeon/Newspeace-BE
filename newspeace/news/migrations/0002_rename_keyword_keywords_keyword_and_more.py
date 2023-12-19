# Generated by Django 4.2 on 2023-12-18 07:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("news", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="keywords",
            old_name="Keyword",
            new_name="keyword",
        ),
        migrations.RemoveField(
            model_name="article",
            name="keyword",
        ),
        migrations.AddField(
            model_name="keywords",
            name="article",
            field=models.ManyToManyField(blank=True, to="news.article"),
        ),
    ]
