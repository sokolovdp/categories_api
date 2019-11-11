from django.db import transaction, IntegrityError, DatabaseError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable
from rest_framework import status

from .models import Category, CategorySerializer


class CategoryViewSet(ViewSet):
    queryset = Category.objects
    category_serializer = CategorySerializer

    def create(self, request):
        serializer = self.category_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                new_category = Category(**serializer.validated_data)
                new_category.save()
        except (IntegrityError, DatabaseError, Exception) as e:
            raise NotAcceptable(detail=str(e))
        else:
            return Response({'id': new_category.id})

    def retrieve(self, request, pk=None):
        category = self.queryset.filter(id=int(pk)).first()
        return Response(self.category_serializer(category).data)
