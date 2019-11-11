from django.db import models, connection
from rest_framework import serializers


SQL_REQUEST = """
select id, name, parent_id
from api_category
where id = {pk}

union

select id, name, parent_id
from api_category
where id = (select parent_id from api_category where id = {pk})

union

select id, name, parent_id
from api_category
where parent_id = {pk}

union

select id, name, parent_id
from api_category
where parent_id = (select parent_id from api_category where id = {pk})
"""


class Relatives(models.Manager):
    def load(self, pk: int = None) -> tuple:
        with connection.cursor() as cursor:
            cursor.execute(SQL_REQUEST.format(pk=pk))
            result_dict = {}
            for row in cursor.fetchall():
                category = self.model(id=row[0], name=row[1], parent_id=row[2])
                result_dict[row[0]] = category
        if not result_dict:
            return None, None, [], [], []
        head = result_dict.pop(int(pk))
        parent = result_dict.pop(head.parent_id) if head.parent_id else None
        children = siblings = []
        for row in result_dict.values():
            if row.parent_id == head.id:
                children.append(row)
            else:
                siblings.append(row)

        return head.id, head.name, [parent] if parent else [], children, siblings


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
