from django.db import models


class DirectorManager(models.Manager):
    def get_directors_by_movies_count(self):
        return self.annotate(
            total_movies_by_director=models.Count('director_movies')
        ).order_by('-total_movies_by_director', 'full_name')
