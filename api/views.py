from django.db import transaction, IntegrityError, DatabaseError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import Category, CreateCategoriesSerializer, RetrieveCategoriesSerializer


class CategoryViewSet(ViewSet):

    def create(self, request):
        serializer = CreateCategoriesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
        except IntegrityError:
            return Response(
                {'error': 'DB integrity error, category with the same already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except (DatabaseError, Exception) as e:
            return Response(
                {'error': f'internal error {repr(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response({'result': 'categories created'})

    def retrieve(self, request, pk=None):
        categories = Category.relatives.load(pk=pk)
        field_names = RetrieveCategoriesSerializer().fields
        result = dict((k, v) for k, v in zip(field_names, categories))
        return Response(RetrieveCategoriesSerializer(result).data)
