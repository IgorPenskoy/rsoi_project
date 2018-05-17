# Generated by Django 2.0.4 on 2018-05-18 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='URL репозитория')),
                ('username', models.CharField(max_length=150, verbose_name='Имя пользователя Gitlab')),
                ('repository', models.CharField(max_length=150, verbose_name='Название репозитория')),
                ('last_activity', models.DateTimeField(auto_now_add=True, verbose_name='Время послденей активности')),
            ],
            options={
                'ordering': ('username', 'repository'),
            },
        ),
    ]
