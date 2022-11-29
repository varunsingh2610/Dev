from rest_framework import serializers
from .models import Movie
from django.contrib.auth.models import User

class MovieSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    """
    Serializer for Movie model
    """

    class Meta:
        model = Movie
        fields = ('url', "name", "imdb_score", "popularity", "director", "genre")
