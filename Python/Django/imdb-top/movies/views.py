from .models import Movie
from .serializers import MovieSerializer

from rest_framework import filters
from rest_framework import permissions
from movies.permissions import IsAdminOrReadOnly
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework


class MovieFilter(rest_framework.FilterSet):
    name = rest_framework.Filter(field_name="name", lookup_expr='icontains')
    director = rest_framework.Filter(field_name="director", lookup_expr='icontains')
    genre = rest_framework.Filter(field_name="genre", lookup_expr='icontains')

    class Meta:
        model = Movie
        fields = ['name', 'director', 'genre']

class MovieViewSet(viewsets.ModelViewSet):
    """
    ViewSet API for searching, filtering and ordering Movies.
    """
    serializer_class = MovieSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter)
    permission_classes = (IsAdminOrReadOnly, permissions.IsAuthenticated)
    search_fields = ("name", "imdb_score", "popularity", "director", "genre")
    ordering_fields = ('name', 'imdb_score', 'popularity')
    ordering = ['name']
    filterset_class = MovieFilter

    queryset = Movie.objects.all()

    def perform_create(self, serializer):
        serializer.save()
