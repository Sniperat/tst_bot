# Generated by Django 4.1.6 on 2023-02-02 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TgUserModel',
            fields=[
                ('chat_id', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('full_name', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('steps', models.SmallIntegerField(choices=[(0, 'add fullname'), (1, 'add phone number'), (2, 'add email'), (3, 'add address'), (4, 'ready to chat')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ServerMessageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg_type', models.SmallIntegerField(choices=[(0, 'Text'), (1, 'Image'), (2, 'File')], default=0)),
                ('text', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('file', models.FileField(blank=True, null=True, upload_to='files/')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('m_status', models.SmallIntegerField(choices=[(0, 'New message'), (1, 'read')], default=0)),
                ('is_admin', models.BooleanField(default=True)),
                ('send_type', models.SmallIntegerField(choices=[(0, 'Private'), (1, 'Broad')], default=0)),
                ('is_recive', models.BooleanField(default=True)),
                ('tg_user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='bot.tgusermodel')),
            ],
        ),
        migrations.CreateModel(
            name='MessageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg_type', models.SmallIntegerField(choices=[(0, 'Text'), (1, 'Image'), (2, 'File')], default=0)),
                ('text', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('file', models.FileField(blank=True, null=True, upload_to='files/')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('m_status', models.SmallIntegerField(choices=[(0, 'New message'), (1, 'read')], default=0)),
                ('tg_user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='bot.tgusermodel')),
            ],
        ),
    ]