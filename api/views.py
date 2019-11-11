from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from .models import Category, PostCategorySerializer, FullResponseCategorySerializer


class CategoryViewSet(ViewSet):
    queryset = Category.objects.select_related('parent').prefetch_related('children')
    category_serializer = PostCategorySerializer

    def create(self, request):
        serializer = self.category_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = serializer.save()
        return Response({'id': category.id})

    def retrieve(self, request, pk=None):
        category = self.queryset.filter(id=pk).first()
        if not category:
            return Response({})
        parent = category.parent
        children = list(category.children.all())
        if parent:
            siblings = list(Category.objects.filter(parent_id=parent.id).exclude(id=pk))
        else:
            siblings = list(Category.objects.filter(parent_id=None).exclude(id=pk))
        result = {
            'id': category.id,
            'name': category.name,
            'parents': [parent] if parent else [],
            'children': children,
            'siblings': siblings
        }
        return Response(FullResponseCategorySerializer(result).data)

