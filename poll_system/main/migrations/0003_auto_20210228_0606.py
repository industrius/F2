# Generated by Django 3.1.5 on 2021-02-28 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210228_0551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.CharField(blank=True, max_length=200, verbose_name='Ответ'),
        ),
    ]
