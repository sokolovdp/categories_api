from django.db import models
from rest_framework import serializers


class Category(models.Model):
    name = models.CharField(max_length=128)
    parent = models.ForeignKey(
        'self',
        null=True,
        related_name='children',
        on_delete=models.CASCADE)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'parent')


class ShortCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('parent', )


class CategoryResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    parents = ShortCategorySerializer(many=True)
    children = ShortCategorySerializer(many=True)
    siblings = ShortCategorySerializer(many=True)