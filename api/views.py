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
        category = Category.relatives.filter(id=pk).first()
        if not category:
            return Response({})
        parent = category.parent
        children = list(category.children.all())
        siblings = list(Category.objects.filter(parent_id=(parent.id if parent else None)).exclude(id=pk))
        result = {
            'id': category.id,
            'name': category.name,
            'parents': [parent] if parent else [],
            'children': children,
            'siblings': siblings
        }
        return Response(FullResponseCategorySerializer(result).data)

