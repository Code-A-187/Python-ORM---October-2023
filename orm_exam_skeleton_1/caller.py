import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from django.db.models import Q, Count, Avg, F
from main_app.models import Director, Actor, Movie


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

    return f"Top Director: {director.full_name}, movies: {director.total_movies_by_director}."


def get_top_actor():
    actor = Actor.objects.prefetch_related('starring_movies') \
        .annotate(
        num_of_movies=Count('starring_movies'),
        movies_avg_rating=Avg('starring_movies__rating')) \
        .order_by('-num_of_movies', 'full_name') \
        .first()

    if not actor or not actor.num_of_movies:
        return ""

    movies = ", ".join(movie.title for movie in actor.starring_movies.all() if movie)

    return f"Top Actor: {actor.full_name}, starring in movies: {movies}, " \
           f"movies average rating: {actor.movies_avg_rating:.1f}"


def get_actors_by_movies_count():
    actors = Actor.objects.annotate(
        num_movies=Count('actor_movies')
    ).order_by('-num_movies', 'full_name')[:3]

    if not actors or actors[0].num_movies == 0:
        return ""

    result = []

    for actor in actors:
        result.append(f'{actor.full_name}, participated in {actor.num_movies} movies')

    return '\n'.join(result)


def get_top_rated_awarded_movie():
    movie = Movie.objects.select_related(
        'starring_actor'
    ).prefetch_related(
        'actors'
    ).filter(
        is_awarded=True
    ).order_by('-rating', 'title').first()

    if movie is None:
        return ""

    starring_actor = movie.starring_actor.full_name if movie.starring_actor else "N/A"

    participating_actors = movie.actors.order_by('full_name').values_list('full_name', flat=True)

    cast = ", ".join(participating_actors)

    return (f'Top rated awarded movie: {movie.title}, '
            f'rating: {movie.rating:.1f}. '
            f'Starring actor: {starring_actor}. '
            f'Cast: {cast}.')


def increase_rating():
    movies_to_update = Movie.objects.filter(is_classic=True, rating__lt=10)

    if not movies_to_update:
        return "No ratings increased."

    movies_to_update.update(rating=F('rating') + 0.1)

    return f'Rating increased for {movies_to_update} movies.'
