# Generated by Django 4.2.1 on 2023-05-05 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TaskMangerAPI', '0005_alter_task_due_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='due_date',
        ),
    ]