# Generated by Django 5.1.1 on 2024-09-15 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FacultyApp', '0002_remove_faculty_id_alter_faculty_fid'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty',
            name='sNo',
            field=models.IntegerField(default=True),
        ),
    ]
