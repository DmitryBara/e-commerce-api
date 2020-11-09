from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Book
from .serializers import BookDetailSerializer, BookListSerializer
from django.http import Http404
from userprofile.utils import check_subscribe


class BookList(APIView):

    def get(self, request):
        books = Book.objects.all()
        serializer_context = {
            'request': request,
        }
        serializer = BookListSerializer(books, context=serializer_context, many=True)
        return Response(serializer.data)


# Чек proifle_id and token
class BookDetail(APIView):

    def _get_object(self, book_id):
        try:
            return Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            raise Http404

    @check_subscribe
    def get(self, request, book_id):
        book = self._get_object(book_id)
        serializer_context = {
            'request': request,
        }
        serializer = BookDetailSerializer(book, context=serializer_context)
        return Response(serializer.data)
