# Generated by Django 4.0.4 on 2022-05-05 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0009_tweet_users_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='hits',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
