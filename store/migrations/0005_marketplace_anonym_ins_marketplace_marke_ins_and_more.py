# Generated by Django 4.1.4 on 2023-02-10 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_remove_marketplace_anonym_remove_marketplace_brand_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='marketplace',
            name='anonym_ins',
            field=models.CharField(choices=[('Ja', 'Ja'), ('Nein', 'Nein')], default='Ja', max_length=255),
        ),
        migrations.AddField(
            model_name='marketplace',
            name='marke_ins',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='marketplace',
            name='typ_marke_ins',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
