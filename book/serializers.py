from rest_framework import serializers
from .models import Book, Author


class AuthorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Author
        fields = ('id', 'name', 'country')


class BookDetailSerializer(serializers.HyperlinkedModelSerializer):

    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'url', 'author')


class BookListSerializer(serializers.HyperlinkedModelSerializer):

    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'author')

    def to_representation(self, instance):
        data = super(BookListSerializer, self).to_representation(instance)
        author = data.pop('author')
        data['author'] = author.get('name')
        return data
