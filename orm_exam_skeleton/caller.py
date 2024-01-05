import os
import django



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from django.db.models import Q, Count, Avg, F, Max
from main_app.models import Author, Article, Review

from django.db.models import Q


def get_authors(search_name=None, search_email=None):
    if search_name is None and search_email is None:
        return ""

    query = Q()
    query_name = Q(full_name__icontains=search_name)
    query_email = Q(email__icontains=search_email)

    if search_name is not None and search_email is not None:
        query |= query_name & query_email
    elif search_name is not None:
        query |= query_name
    else:
        query |= query_email

    authors = Author.objects.filter(query).order_by('-full_name')

    if not authors:
        return ""

    result = []

    for author in authors:
        status = 'Banned' if author.is_banned else 'Not Banned'
        result.append(f"Author: {author.full_name}, email: {author.email}, status: {status}")

    return '\n'.join(result)


def get_top_publisher():
    authors_with_articles = Author.objects.get_authors_by_article_count().filter(total_authors_by_article__gt=0)
    top_author = authors_with_articles.order_by('-total_authors_by_article', 'email').first()

    if not top_author:
        return ""

    return f"Top Author: {top_author.full_name} with {top_author.total_authors_by_article} published articles."


def get_top_reviewer():
    authors_with_reviews = Author.objects.annotate(num_of_reviews=Count('author_reviews')).filter(num_of_reviews__gt=0)
    top_reviewer = authors_with_reviews.order_by('-num_of_reviews', 'email').first()

    if not top_reviewer:
        return ""

    return f'Top Reviewer: {top_reviewer.full_name} with {top_reviewer.num_of_reviews} published reviews.'


def get_latest_article():
    latest_article = Article.objects.prefetch_related('authors').last()

    if not latest_article:
        return ""

    authors_names = ", ".join(sorted([author.full_name for author in latest_article.authors.all()]))

    avg_rating_formatted = "{:.2f}".format(
        latest_article.avg_reviews_rating) if latest_article.avg_reviews_rating else ""

    return f"The latest article is: {latest_article.title}. Authors: {authors_names}. " \
           f"Reviewed: {latest_article.num_reviews} times. Average Rating: {avg_rating_formatted}."


def get_top_rated_article():
    top_rated_article = Article.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        num_reviews=Count('reviews')
    ).filter(num_reviews__gt=0).order_by('-avg_rating', 'title').first()

    if not top_rated_article:
        return ""

    avg_rating_formatted = "{:.2f}".format(top_rated_article.avg_rating)

    return f"The top-rated article is: {top_rated_article.title}, with an average rating of {avg_rating_formatted}, " \
           f"reviewed {top_rated_article.num_reviews} times."


def ban_author(email=None):
    if email is None:
        return "No authors banned."

    try:
        author_to_ban = Author.objects.get(email=email)

        num_reviews = Review.objects.filter(author=author_to_ban).count()

        author_to_ban.is_banned = True
        author_to_ban.save()
        Review.objects.filter(author=author_to_ban).delete()

        return f"Author: {author_to_ban.full_name} is banned! {num_reviews} reviews deleted."
    except Author.DoesNotExist:
        return "No authors banned."
