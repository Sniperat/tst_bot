# Generated by Django 4.1.6 on 2023-02-03 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messagemodel',
            name='image',
        ),
        migrations.RemoveField(
            model_name='servermessagemodel',
            name='image',
        ),
        migrations.AlterField(
            model_name='servermessagemodel',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
