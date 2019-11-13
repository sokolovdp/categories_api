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

    def init_database(self):
        response = self.client.post('/categories/', SOURCE_DATA, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 15)

    def test_create_categories_wrong_formats(self):
        """
            Check if API properly validate input data
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
            Upload categories into database
        """
        self.init_database()

    def test_get_all_categories(self):
        """
            Get category data by its ID
        """
        self.init_database()

        for category_id in range(1, 16):
            url = f'/categories/{category_id}/'
            response = self.client.get(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get("id"), category_id)

    def test_get_invalid_category_id(self):
        """
            Check if API properly handle invalid category ids
        """
        self.init_database()

        url = f'/categories/0/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        url = f'/categories/16/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        url = f'/categories/err/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_response_data_structure(self):
        """
            Get category data by its ID and check response data structure
            For id = 3 expected data are:
            {
                "id": 3,
                "name": "Category 1.1.1",
                "parents": [
                    {
                        "id": 2,
                        "name": "Category 1.1"
                    },
                    {
                        "id": 1,
                        "name": "Category 1"
                    }
                ],
                "children": [
                    {
                        "id": 4,
                        "name": "Category 1.1.1.1"
                    },
                    {
                        "id": 5,
                        "name": "Category 1.1.1.2"
                    },
                    {
                        "id": 6,
                        "name": "Category 1.1.1.3"
                    }
                ],
                "siblings": [
                    {
                        "id": 7,
                        "name": "Category 1.1.2"
                    }
                ]
            }

        """

        self.init_database()

        category_id = 3
        category_name = "Category 1.1.1"
        url = f'/categories/{category_id}/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data.get("id"), category_id)
        self.assertEqual(response.data.get("name"), category_name)
        self.assertEqual(len(response.data.get("parents")), 2)
        self.assertEqual(len(response.data.get("children")), 3)
        self.assertEqual(len(response.data.get("siblings")), 1)


