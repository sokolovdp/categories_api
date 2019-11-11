from django.db import models
from rest_framework import serializers


class Category(models.Model):
    name = models.CharField(max_length=128)
    parent = models.ForeignKey(
        'self',
        null=True,
        related_name='children',
        on_delete=models.CASCADE)


class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'parent')


class GetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('parent', )


class FullResponseCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    parents = GetCategorySerializer(many=True)
    children = GetCategorySerializer(many=True)
    siblings = GetCategorySerializer(many=True)
