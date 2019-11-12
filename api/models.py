from django.db import models, connection
from rest_framework import serializers

# SQLite3 dialect !!!
SQL_REQUEST = """
WITH RECURSIVE
    head (id, name, parent_id, level) AS
        (
            SELECT t.id, t.name, t.parent_id, 'head' AS LEVEL
            FROM api_category AS t
            WHERE t.id = {pk}
        ),
    children (id, name, parent_id, level) AS
        (
            SELECT id, name, parent_id, level
            FROM head
            UNION ALL
            SELECT a.id, a.name, a.parent_id, 'children' AS LEVEL
            FROM api_category AS a
                     JOIN children AS c ON c.id = a.parent_id
        ),
    parents (id, name, parent_id, level) AS
        (
            SELECT id, name, parent_id, 'parents' AS LEVEL
            FROM api_category as a
            WHERE a.id IS (SELECT parent_id FROM head)
            UNION ALL
            SELECT a.id, a.name, a.parent_id, level
            FROM api_category AS a
                     JOIN parents ON parents.parent_id = a.id
        ),
    siblings (id, name, parent_id, level) AS
        (
            SELECT id, name, parent_id, 'siblings' AS LEVEL
            FROM api_category
            WHERE parent_id != (SELECT parent_id FROM api_category
            WHERE id = {pk})
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
                if row[3] == 'head':
                    head_id = category.id
                    head_name = category.name
                elif row[3] == 'parents':
                    parents.append(category)
                elif row[3] == 'children':
                    children.append(category)
                else:
                    siblings.append(category)
        return head_id, head_name, parents, children, siblings


class Category(models.Model):
    name = models.CharField(max_length=128)
    parent = models.ForeignKey(
        'self',
        null=True,
        related_name='children',
        on_delete=models.CASCADE)

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
