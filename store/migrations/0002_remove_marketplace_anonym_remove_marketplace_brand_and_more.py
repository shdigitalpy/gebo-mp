# Generated by Django 4.1.4 on 2023-02-10 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='marketplace',
            name='anonym',
        ),
        migrations.RemoveField(
            model_name='marketplace',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='marketplace',
            name='typ_marke',
        ),
    ]
