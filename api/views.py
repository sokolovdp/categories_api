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
        head_id, head_name, parents, children, siblings = Category.relatives.load(pk=pk)
        result = {
            'id': head_id,
            'name': head_name,
            'parents': parents,
            'children': children,
            'siblings': siblings
        }

        return Response(FullResponseCategorySerializer(result).data)
