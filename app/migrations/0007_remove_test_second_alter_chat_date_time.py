# Generated by Django 4.2 on 2023-05-07 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_chat_date_time_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='second',
        ),
        migrations.AlterField(
            model_name='chat',
            name='date_time',
            field=models.CharField(default='05:57 PM', max_length=100),
        ),
    ]
