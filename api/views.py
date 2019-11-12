from django.db import transaction, IntegrityError, DatabaseError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from .models import Category, PostCategorySerializer, FullResponseCategorySerializer


class CategoryViewSet(ViewSet):

    def create(self, request):
        serializer = PostCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            new_category = Category(**serializer.validated_data)
            new_category.save()
        return Response({'id': new_category.id})

    def retrieve(self, request, pk=None):
        categories = Category.relatives.load(pk=pk)
        field_names = FullResponseCategorySerializer().fields
        result = dict((k, v) for k, v in zip(field_names, categories))
        return Response(FullResponseCategorySerializer(result).data)
