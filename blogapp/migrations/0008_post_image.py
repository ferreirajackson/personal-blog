# Generated by Django 2.2.13 on 2021-02-21 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0007_newsletter'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image/'),
        ),
    ]
