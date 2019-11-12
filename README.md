# Demo API based on Django's DRF API services to show implementation of the Tree like structure in SQL database table and AI to create and retrieve data from it
## Run application
```text
python manage.py runserver 8000
```
## Model:
```python
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        related_name='children',
        on_delete=models.CASCADE)
    objects = models.Manager()
    relatives = Relatives()
```
## API's points:
```text
​ POST /categories/
```
```text
 GET /categories/<id>/​
```

##  Implementation notes
API using recursive SQL queries returns both all ancestors (parents) and all descendants (children) of an element, plus its siblings (categories with the same parent)

## Tests
```text
python manage.py test

```

## Postman collection to test API
https://www.getpostman.com/collections/ea2dfb57228b08319c7c