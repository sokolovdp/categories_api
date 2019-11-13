from django.db import transaction, IntegrityError, DatabaseError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import Category, CreateCategoriesSerializer, RetrieveCategoriesSerializer

field_names = RetrieveCategoriesSerializer().fields


class CategoryViewSet(ViewSet):
    lookup_value_regex = '[0-9]+'

    def create(self, request):
        serializer = CreateCategoriesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
        except IntegrityError:
            return Response(
                {'error': 'DB integrity error, category with the same name already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except (DatabaseError, Exception) as e:
            return Response(
                {'error': f'internal error {repr(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        else:
            return Response(None, status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        categories = Category.relatives.load(pk=pk)
        result = dict((k, v) for k, v in zip(field_names, categories))
        if result['id'] is None:
            return Response({'error': f'wrong category id'}, status=status.HTTP_404_NOT_FOUND)

        return Response(RetrieveCategoriesSerializer(result).data)
