# Generated by Django 3.2.13 on 2022-05-27 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signaux', '0003_signal_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signal',
            name='picture',
            field=models.ImageField(blank=True, upload_to='./pics'),
        ),
    ]
