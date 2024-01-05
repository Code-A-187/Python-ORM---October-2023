import os
import django



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Director, Actor
from django.db.models import Q,Count, Avg


def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ""

    query = Q()
    query_name = Q(full_name__icontains=search_name)
    query_nationality = Q(nationality__icontains=search_nationality)

    if search_name is not None and search_nationality is not None:
        query |= query_name & query_nationality
    elif search_name is not None:
        query |= query_name
    else:
        query |= query_nationality

    directors = Director.objects.filter(query).order_by('full_name')

    if not directors:
        return ""

    result = []

    [result.append(f"Director: {director.full_name}, nationality: {director.nationality}, "
                   f"experience: {director.years_of_experience}") for director in directors]

    return '\n'.join(result)


def get_top_director():
    director = Director.objects.get_directors_by_movies_count().first()

    if not director:
        return ""

    return f"Top Director: {director.full_name}, movies: {director.movies_count}."


def get_top_actor():
    actor = Actor.objects.prefetch_related('starring_actor_movie') \
        .annotate(
        num_of_movies=Count('starring_actor_movie'),
        movies_avg_rating=Avg('starring_actor_movie__rating')) \
        .order_by('-num_of_movies', 'full_name') \
        .first()

    if not actor or not actor.num_of_movies:
        return ""

    movies = ", ".join(movie.title for movie in actor.starring_actor_movie.all() if movie)

    return f"Top Actor: {actor.full_name}, starring in movies: {movies}, " \
           f"movies average rating: {actor.movies_avg_rating:.1f}"


def get_actors_by_movies_count():
    pass


def get_top_rated_awarded_movie():
    pass


def increase_rating():
    pass
