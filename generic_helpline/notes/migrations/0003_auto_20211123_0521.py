# Generated by Django 2.1.5 on 2021-11-22 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_auto_20211123_0348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='image',
            field=models.ImageField(blank=True, upload_to='notes'),
        ),
    ]
