from django.db import models
from rest_framework import serializers


class Category(models.Model):
    name = models.CharField(max_length=128)
    parent = models.ForeignKey('Category', null=True, on_delete=models.CASCADE)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
