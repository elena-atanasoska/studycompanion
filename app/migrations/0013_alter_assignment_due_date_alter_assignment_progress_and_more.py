# Generated by Django 4.2.3 on 2023-08-15 10:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_assignment_due_date_alter_assignment_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2023, 8, 22, 12, 38, 15, 186819)),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='progress',
            field=models.IntegerField(choices=[(0, '0'), (10, '1'), (20, '2'), (30, '3'), (40, '4'), (50, '5'), (60, '6'), (70, '7'), (80, '8'), (90, '9'), (100, '10')], default=0),
        ),
        migrations.AlterField(
            model_name='reminder',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 22, 12, 38, 15, 188818)),
        ),
        migrations.AlterField(
            model_name='task',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
