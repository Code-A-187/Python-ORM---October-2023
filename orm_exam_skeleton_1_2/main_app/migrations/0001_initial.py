# Generated by Django 4.2.4 on 2023-11-24 09:00

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=120, validators=[django.core.validators.MinLengthValidator(2)])),
                ('birth_date', models.DateField(default='1900-01-01')),
                ('nationality', models.CharField(default='Unknown', max_length=50)),
                ('is_awarded', models.BooleanField(default=False)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=120, validators=[django.core.validators.MinLengthValidator(2)])),
                ('birth_date', models.DateField(default='1900-01-01')),
                ('nationality', models.CharField(default='Unknown', max_length=50)),
                ('years_of_experience', models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0.0)])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_awarded', models.BooleanField(default=False)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=150, validators=[django.core.validators.MinLengthValidator(5)])),
                ('release_date', models.DateField()),
                ('storyline', models.TextField(blank=True, null=True)),
                ('genre', models.CharField(choices=[('Action', 'Action'), ('Comedy', 'Comedy'), ('Drama', 'Drama'), ('Other', 'Other')], default='Other', max_length=6)),
                ('rating', models.DecimalField(decimal_places=1, default=0.0, max_digits=3, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)])),
                ('is_classic', models.BooleanField(default=False)),
                ('actors', models.ManyToManyField(related_name='actors_movie', to='main_app.actor')),
                ('director', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='director_movie', to='main_app.director')),
                ('starring_actor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='starring_actor_movie', to='main_app.actor')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
