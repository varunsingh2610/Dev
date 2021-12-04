from django.db import models

class ConnectionsDB(models.Model):
    database = models.CharField(max_length=100)
    server = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.database
