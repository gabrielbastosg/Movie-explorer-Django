from django.db import models

# Create your models here.
class FavoriteMovie(models.Model):
    movie_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    poster_path = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title