# Generated by Django 2.2.13 on 2021-02-13 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0006_auto_20210213_1459'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255, null=True)),
                ('status', models.CharField(max_length=10, null=True)),
            ],
        ),
    ]