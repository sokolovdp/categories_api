from django.db import models
from rest_framework import serializers


class Category(models.Model):
    name = models.CharField(max_length=128)
    parent = models.ForeignKey(
        'Category',
        blank=True,
        null=True,
        related_name='children',
        verbose_name='parent',
        on_delete=models.CASCADE)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
