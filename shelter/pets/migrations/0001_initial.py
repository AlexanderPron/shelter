# Generated by Django 3.1.5 on 2021-01-11 13:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Пока без имени', help_text='Укажите кличку животного', max_length=100, verbose_name='Кличка')),
                ('pet_type', models.CharField(choices=[('Cat', 'Кошка'), ('Dog', 'Собака'), ('Parrot', 'Попугай')], default='Cat', max_length=10, verbose_name='Вид')),
                ('breed', models.CharField(default='Неизвестно', help_text='Укажите породу животного', max_length=100, verbose_name='Порода')),
                ('sex', models.CharField(choices=[('M', 'Мужской'), ('F', 'Женский'), ('n/a', 'Не известно')], default='n/a', max_length=3, verbose_name='Пол')),
                ('enter_date', models.DateField(default=datetime.date.today, verbose_name='Дата поступления')),
                ('exit_date', models.DateField(blank=True, verbose_name='Дата приюта')),
                ('approximate_age', models.SmallIntegerField(null=True, verbose_name='Возраст')),
                ('available', models.BooleanField(default=True, verbose_name='Доступен')),
                ('description', models.TextField(verbose_name='Описание')),
                ('avatar', models.ImageField(blank=True, upload_to='pet_avatars/%Y/%m/%d', verbose_name='Аватар')),
            ],
            options={
                'verbose_name': 'Питомец',
                'verbose_name_plural': 'Питомцы',
                'ordering': ['-name'],
            },
        ),
    ]
