# Generated by Django 4.0.6 on 2022-07-25 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productdetails',
            name='user_email',
            field=models.EmailField(max_length=100),
        ),
    ]
