from django.db import models
from rest_framework import serializers


class Relatives(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('parent').prefetch_related('children')


class Category(models.Model):
    name = models.CharField(max_length=128)
    parent = models.ForeignKey(
        'self',
        null=True,
        related_name='children',
        on_delete=models.CASCADE)

    objects = models.Manager()
    relatives = Relatives()


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
