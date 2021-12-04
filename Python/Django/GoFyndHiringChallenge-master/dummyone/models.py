from django.db import models
from django.utils import timezone
from django.conf import settings




class imdb(models.Model): 
    popularity = models.FloatField( null = True)
    director = models.CharField( max_length=21, null = True,blank=True)
    genre = models.CharField( max_length=12, null = True)
    imdb_score = models.FloatField( null = True)
    name = models.CharField(max_length=69, null = True)