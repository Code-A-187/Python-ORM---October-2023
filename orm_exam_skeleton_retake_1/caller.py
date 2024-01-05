import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()
from django.db.models import Q, Count
from main_app.models import TennisPlayer, Tournament, Match


def get_tennis_players(search_name=None, search_country=None):
    if search_name is None and search_country is None:
        return ""

    query = Q()
    query_name = Q(full_name__icontains=search_name)
    query_country = Q(country__icontains=search_country)

    if search_name is not None and search_country is not None:
        query |= query_name & query_country
    elif search_name is not None:
        query |= query_name
    else:
        query |= query_country

    players = TennisPlayer.objects.filter(query).order_by('ranking')

    if not players:
        return ""

    result = []

    for player in players:
        result.append(f"Tennis Player: {player.full_name}, country: {player.country}, ranking: {player.ranking}")

    return '\n'.join(result)


def get_top_tennis_player():
    top_player = TennisPlayer.objects.get_tennis_players_by_wins_count().filter(wins_count__gt=0).first()

    if not top_player:
        return ""

    return f"Top Tennis Player: {top_player.full_name} with {top_player.wins_count} wins."


def get_tennis_player_by_matches_count():
    players_with_matches = TennisPlayer.objects.annotate(num_of_matches=Count('match'))

    top_player = players_with_matches.order_by('-num_of_matches', 'ranking').first()

    if not top_player or top_player.num_of_matches == 0:
        return ""

    return f'Tennis Player: {top_player.full_name} with {top_player.num_of_matches} matches played.'


def get_tournaments_by_surface_type(surface=None):
        if surface is None:
            return ""
        tournaments = Tournament.objects.filter(surface_type__icontains=surface.lower()).order_by('-start_date')
        if not tournaments:
            return ""
        result = []
        for tournament in tournaments:
            num_matches = tournament.match_set.count()
            result.append(f"Tournament: {tournament.name}, start date: {tournament.start_date}, matches: {num_matches}")
        return '\n'.join(result)


def get_latest_match_info():
    latest_match = Match.objects.prefetch_related('players').order_by('-date_played', '-id').first()

    if latest_match is None:
        return ""

    # Extract information from the latest match
    tournament_name = latest_match.tournament.name
    score = latest_match.score

    # Ensure players' full names are ordered by full name in ascending order
    players_full_names = sorted(player.full_name for player in latest_match.players.all())

    # Get the winner's full name or set to "TBA" if the winner is None
    winner_full_name = latest_match.winner.full_name if latest_match.winner else "TBA"

    result = f"Latest match played on: {latest_match.date_played}, tournament: {tournament_name}, score: {score}, " \
             f"players: {players_full_names[0]} vs {players_full_names[1]}, winner: {winner_full_name}, " \
             f"summary: {latest_match.summary}"

    return result


def get_matches_by_tournament(tournament_name=None):
    if tournament_name is None:
        return "No matches found."

    try:
        tournament = Tournament.objects.get(name=tournament_name)
    except Tournament.DoesNotExist:
        return "No matches found."

    matches = Match.objects.filter(tournament=tournament).order_by('-date_played')

    if not matches.exists():
        return "No matches found."

    result = ""
    for match in matches:
        winner_full_name = match.winner.full_name if match.winner else "TBA"
        result += f"Match played on: {match.date_played}, score: {match.score}, winner: {winner_full_name}\n"
    return result