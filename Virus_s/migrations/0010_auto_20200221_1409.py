# Generated by Django 3.0.3 on 2020-02-21 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Virus_s', '0009_auto_20200221_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='sourceUrl',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
