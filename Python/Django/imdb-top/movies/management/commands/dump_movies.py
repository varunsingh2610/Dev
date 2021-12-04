import json
from django.core.management.base import BaseCommand
from django.conf import settings

from ...models import Movie


class Command(BaseCommand):
    """
    To dump movies data to database
    """
    def handle(self, *args, **options):
        filepath = settings.BASE_DIR + '/imdb.json'
        with open(filepath, 'r') as f:
            raw_movie_data = f.read()
            movie_data = json.loads(raw_movie_data)
            dMovie = {}
            for item in movie_data:
                dMovie['popularity'] = item.get('99popularity')
                dMovie['director'] = item.get('director')
                dMovie['imdb_score'] = item.get('imdb_score')
                dMovie['name'] = item.get('name')
                dMovie['genre'] = ', '.join(item.get('genre'))
                movie, created = Movie.objects.get_or_create(**dMovie)
                movie.save()
                print (movie)
