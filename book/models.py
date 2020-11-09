from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default=None)
    url = models.TextField()
    author = models.ForeignKey('Author', related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

