# Generated by Django 4.2.1 on 2023-05-05 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskMangerAPI', '0004_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]