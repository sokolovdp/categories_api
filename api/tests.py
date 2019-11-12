from rest_framework import status
from rest_framework.test import APITestCase
from .models import Category


SOURCE_DATA = {
    "name": "Category 1",
    "children": [
        {
            "name": "Category 1.1",
            "children": [
                {
                    "name": "Category 1.1.1",
                    "children": [
                        {
                            "name": "Category 1.1.1.1"
                        },
                        {
                            "name": "Category 1.1.1.2"
                        },
                        {
                            "name": "Category 1.1.1.3"
                        }
                    ]
                },
                {
                    "name": "Category 1.1.2",
                    "children": [
                        {
                            "name": "Category 1.1.2.1"
                        },
                        {
                            "name": "Category 1.1.2.2"
                        },
                        {
                            "name": "Category 1.1.2.3"
                        }
                    ]
                }
            ]
        },
        {
            "name": "Category 1.2",
            "children": [
                {
                    "name": "Category 1.2.1"
                },
                {
                    "name": "Category 1.2.2",
                    "children": [
                        {
                            "name": "Category 1.2.2.1"
                        },
                        {
                            "name": "Category 1.2.2.2"
                        }
                    ]
                }
            ]
        }
    ]
}


class CategoryTests(APITestCase):

    def test_create_categories_wrong_formats(self):
        """
            Check if validation works
        """
        url = '/categories/'
        data = {'test': 'invalid format'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'name': 'Category', 'children': 'error'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_categories(self):
        """
            Create categories
        """
        url = '/categories/'
        response = self.client.post(url, SOURCE_DATA, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 15)

    def test_get_categories(self):
        """
            Get category data by its ID
        """
        url = '/categories/'
        response = self.client.post(url, SOURCE_DATA, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)