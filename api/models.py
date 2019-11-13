from django.db import models, connection
from rest_framework import serializers
from rest_framework.exceptions import APIException, ValidationError

# SQLite3 dialect !!!
SQL_REQUEST = """
WITH RECURSIVE
    head (id, name, parent_id, level) AS
        (
            SELECT t.id, t.name, t.parent_id, 'head' AS LEVEL FROM api_category AS t WHERE t.id = {pk}
        ),
    children (id, name, parent_id, level) AS
        (
            SELECT id, name, parent_id, level FROM head
            UNION ALL
            SELECT a.id, a.name, a.parent_id, 'children' AS LEVEL
                FROM api_category AS a JOIN children AS c ON c.id = a.parent_id
        ),
    parents (id, name, parent_id, level) AS
        (
            SELECT id, name, parent_id, 'parents' AS LEVEL FROM api_category as a
                WHERE a.id = (SELECT parent_id FROM head)
            UNION ALL
            SELECT a.id, a.name, a.parent_id, level
                FROM api_category AS a JOIN parents ON parents.parent_id = a.id
        ),
    siblings (id, name, parent_id, level) AS
        (
            SELECT id, name, parent_id, 'siblings' AS LEVEL FROM api_category
                WHERE parent_id = (SELECT parent_id FROM api_category WHERE id = {pk}) AND id != {pk}
        )
select * from head
UNION
select * from children
UNION  ALL
select * from parents
UNION ALL
select * from siblings
"""


class Relatives(models.Manager):
    def load(self, pk: int = None) -> tuple:
        head_id = head_name = None
        siblings = []
        parents = []
        children = []
        with connection.cursor() as cursor:
            cursor.execute(SQL_REQUEST.format(pk=pk))
            for row in cursor.fetchall():
                category = self.model(id=row[0], name=row[1], parent_id=row[2])
                subquery = row[3]
                if subquery == 'head':
                    head_id = category.id
                    head_name = category.name
                elif subquery in ('parents', 'children', 'siblings'):
                    locals()[subquery].append(category)
                else:
                    continue
        return head_id, head_name, parents, children, siblings


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    parent = models.ForeignKey('self', null=True, related_name='children', on_delete=models.CASCADE)

    # Managers
    objects = models.Manager()
    relatives = Relatives()


class CreateCategoriesSerializer:
    """
        Emulates functionality of a DRF serializer
    """
    @staticmethod
    def create_record(name, parent_id):
        new_category = Category(name=name, parent_id=parent_id)
        new_category.save()
        return new_category.id

    def save_data(self, data, parent_id):
        parent_id = self.create_record(data['name'], parent_id)
        children = data.get('children', [])
        for data in children:
            self.save_data(data, parent_id)

    def check_data(self, data):
        if data.get('name') is None:
            raise ValidationError('invalid data, key "name" is missing')
        children = data.get('children', [])
        if not isinstance(children, list):
            raise ValidationError('invalid data, field "children" is not list type')
        for data in children:
            self.check_data(data)

    def __init__(self, data: dict):
        self.data = data
        self.validated_data = None

    def is_valid(self, raise_exception=True):
        try:
            self.check_data(self.data)
        except ValidationError:
            if raise_exception:
                raise
        else:
            self.validated_data = self.data.copy()

    def save(self):
        if self.validated_data is None:
            raise APIException('no valid data to save, run is_valid() method first!')
        else:
            self.save_data(self.validated_data, None)


class OutputCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('parent',)


class RetrieveCategoriesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    parents = OutputCategorySerializer(many=True)
    children = OutputCategorySerializer(many=True)
    siblings = OutputCategorySerializer(many=True)
