# Generated by Django 4.1.2 on 2023-02-24 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='measure',
            field=models.CharField(choices=[('d', 'Daily'), ('w', 'This week'), ('m', 'This month')], max_length=1, verbose_name='the measure of your goal'),
        ),
    ]
