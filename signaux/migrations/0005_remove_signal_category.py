# Generated by Django 3.2.13 on 2022-05-27 21:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signaux', '0004_alter_signal_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signal',
            name='category',
        ),
    ]
