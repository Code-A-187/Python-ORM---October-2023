from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.db import models


# Create your models here.
class PublishMixin(models.Model):
    class Meta:
        abstract = True

    published_on = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )


class AuthorManager(models.Manager):
    def get_authors_by_article_count(self):
        return self.annotate(
            total_authors_by_article=models.Count('authors_articles')
            ).order_by('-total_authors_by_article', 'email')


class Author(models.Model):
    full_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)]
    )

    email = models.EmailField(
        unique=True,
    )
    is_banned = models.BooleanField(
        default=False,
    )

    birth_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2005)]
    )

    website = models.URLField(
        null=True,
        blank=True,
    )

    objects = AuthorManager()


class Article(PublishMixin):

    CHOICE_ARTICLES = [
        ('Technology', 'Technology'),
        ('Science', 'Science'),
        ('Education', 'Education'),


    ]

    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(5)],
    )

    content = models.TextField(
        validators=[MinLengthValidator(10)]
    )

    category = models.CharField(
        max_length=10,
        choices=CHOICE_ARTICLES,
        default='Technology',
    )

    authors = models.ManyToManyField(
        Author,
        related_name='authors_articles'
    )


class Review(PublishMixin):
    content = models.TextField(
        validators=[MinLengthValidator(10)]
    )

    rating = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)]
    )

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='author_reviews'
    )

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='review_articles'
    )
