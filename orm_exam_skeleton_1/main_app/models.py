from django.core.validators import MinValueValidator, MaxLengthValidator, MinLengthValidator, MaxValueValidator
from django.db import models

from main_app.managers import DirectorManager
from main_app.validators import name_length_validator, nationality_validator


class Director(models.Model):

    full_name = models.CharField(
        max_length=120,
        validators=[name_length_validator],
    )

    birth_date = models.DateField(
        default='1900-01-01',
    )

    nationality = models.CharField(
        max_length=50,
        validators=[nationality_validator],
        default='Unknown'
    )

    years_of_experience = models.SmallIntegerField(
        default=0,
        validators=[MinValueValidator(0, 'year must be 0 or higher')],
    )

    objects = DirectorManager()


class Actor(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[name_length_validator]
    )

    birth_date = models.DateField(
        default='1900-01-01',
    )

    nationality = models.CharField(
        max_length=50,
        validators=[nationality_validator],
        default='Unknown'
    )

    is_awarded = models.BooleanField(
        default=False,
    )

    last_updated = models.DateTimeField(
        auto_now=True,
    )


class Movie(models.Model):
    GENRE_CHOICES = [
        ('Action', 'Action'),
        ('Comedy', 'Comedy'),
        ('Drama', 'Drama'),
        ('Other', 'Other'),
    ]

    title = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(5, 'Movie title should be at least 5 characters'),
                    MaxLengthValidator(150, 'Movie title should not exceed 150 characters')
                    ]
    )

    release_date = models.DateField()

    storyline = models.TextField(
        null=True,
        blank=True,
    )

    genre = models.CharField(
        max_length=6,
        choices=GENRE_CHOICES,
        validators=[MaxLengthValidator(6, 'Genre must be at least 6 characters')],
        default='Other'
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0.0, 'Minimum value must be 0.0'),
                    MaxValueValidator(10.0, 'Maximum value can not exceed 10.0')
                    ],
        default=0.0
    )

    is_classic = models.BooleanField(
        default=False
    )

    is_awarded = models.BooleanField(
        default=False
    )

    last_updated = models.DateTimeField(
        auto_now=True,
    )

    director = models.ForeignKey(Director,
                                 on_delete=models.CASCADE,
                                 related_name='director_movies')
    starring_actor = models.ForeignKey(Actor,
                                       on_delete=models.SET_NULL,
                                       related_name='starring_movies',
                                       null=True, blank=True)
    actors = models.ManyToManyField(Actor,
                                    related_name='actor_movies')

    def __str__(self):
        return self.title
