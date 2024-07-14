ENDPOINT = "http://127.0.0.1:8000/api/"

import os
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import pytest
import requests
from api.utils.views import *

@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_get_products(api_client):

    """
    Path: products/
         Test: 200 GET all products (displays a singular product for test purposes)
    """

    response = api_client.get(ENDPOINT + "products/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0] == {
		"product_id": 1,
		"product": "Apple",
		"description": "Fresh red apples",
		"brand": "FreshFarms",
		"size": "1kg",
		"product_photo_url": "https://images.unsplash.com/photo-1567306226416-28f0efdc88ce?q=80&w=3870&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
		"category": 1
	}
    assert len(response.json()) == 10

@pytest.mark.django_db
def test_post_product(api_client):

    """
    Path: products/
         Test: 201 POST a singular product
               400 Invalid body data
    """
        
    payload = {
        "product": "test",
        "description": "test",
        "brand": "test",
        "size": "test",
        "product_photo_url": "test",
        "category": 1
    }
    response201 =  api_client.post(ENDPOINT + "products/", data=payload, format='json')
    assert response201.status_code == 201
    assert response201.data == {
        "product_id": 11,
    	"product": "test",
        "description": "test",
        "brand": "test",
        "size": "test",
        "product_photo_url": "test",
        "category": 1
    }

    incorrect_payload = {
        "product": True,
        "description": False,
        "brand": None,
        "size": True,
        "product_photo_url": False,
        "category": None
	}

    response =  api_client.post(ENDPOINT + "products/", data=incorrect_payload, format='json')
    assert response.status_code == 400
    

@pytest.mark.django_db
def test_delete_product(api_client):

    """
    Path: products/product_id/
         Test: 204 DELETE a singular product
               404 Invalid product id
               404 Invalid data type for product id
    """

    response204 =  api_client.delete(ENDPOINT + "products/" +"2/")
    assert response204.status_code == 204

    response404_1 = api_client.delete(ENDPOINT + "products/" +"5234623652456345/")
    response404_2 = api_client.delete(ENDPOINT + "products/" +"qwefqewfwq/")
    assert response404_1.status_code == 404
    assert response404_2.status_code == 404


@pytest.mark.django_db
def test_patch_product(api_client):

    """
    Path: products/product_id/
         Test: 200 PATCH a singular product
               404 Invalid product id
               404 Invalid data type product id
    """

    original_item = api_client.get(ENDPOINT + "products/" + "3/").json()

    patch_body = {
        "product": "Not a carrot",
        "description": "Definitely not a carrot",
        "size": "Not carrot sized",
        "product_photo_url": "https://cdn0.iconfinder.com/data/icons/foods-with-a-mustache/1200/fru-12-512.png"
    }
    response200 = api_client.patch(ENDPOINT + "products/" + "3/", data = patch_body)
    assert response200.status_code == 200
    assert (api_client.get(ENDPOINT + "3/").json()) != original_item

    response404_1 = api_client.patch(ENDPOINT + "products/" + "312341234/", data = patch_body)
    response404_2 = api_client.patch(ENDPOINT + "products/" + "fqwefqwefqew/", data = patch_body)
    assert response404_1.status_code == 404
    assert response404_2.status_code == 404

# path('price-report/<int:product_id>/<float:lat>/<float:lon>/<int:rad>/', views.price_report, name='price_report')
@pytest.mark.django_db
def test_get_price_report(api_client):

    """
    Path: price-report/product_id/lat/lon/rad/
         Test: 200 GET all prices of a specific item given a distance
               404 Invalid data type for product id
               404 Invalid product id
               404 Invalid data type for lat/lon
               404 Invalid lat/lon
    """

    response200 = api_client.get(ENDPOINT + "price-report/1/53.8006846000/-1.5506170000/1000/")
    assert response200.status_code == status.HTTP_200_OK
    assert len(response200.json()) == 3
    assert response200.json()[0] == {'price_id': 1, 'price': '10.00', 'store_id': 2, 'store_name': 'Forbidden Planet International', 'latitude': '53.7991821000', 'longitude': '-1.5403808000', 'distance': 694.88400949, 'monday': 'Monday: 9:30\u202fAM\u2009–\u20096:00\u202fPM', 'tuesday': 'Tuesday: 9:30\u202fAM\u2009–\u20096:00\u202fPM', 'wednesday': 'Wednesday: 9:30\u202fAM\u2009–\u20096:00\u202fPM', 'thursday': 'Thursday: 10:00\u202fAM\u2009–\u20096:00\u202fPM', 'friday': 'Friday: 9:30\u202fAM\u2009–\u20096:00\u202fPM', 'saturday': 'Saturday: 9:30\u202fAM\u2009–\u20096:30\u202fPM', 'sunday': 'Sunday: 11:00\u202fAM\u2009–\u20095:00\u202fPM'}

    response404_1 = api_client.get(ENDPOINT + "price-report/gwergwergw/53.7976879000/-1.5439129000/100000000/")
    response404_2 = api_client.get(ENDPOINT + "price-report/1/wergwergwerg/-1.5439129000/100000000/")
    response404_3 = api_client.get(ENDPOINT + "price-report/1/53.7976879000/rwgergwergw/100000000/")
    response404_4 = api_client.get(ENDPOINT + "price-report/1/53.7976879000/-1.5439129000/egwerwergerg/")
    response404_5 = api_client.get(ENDPOINT + "price-report/123512351235/53.7976879000/-1.5439129000/100000000/")
    response404_6 = api_client.get(ENDPOINT + "price-report/1/537976879000123512345123/-1.5439129000/100000000/")
    response404_7 = api_client.get(ENDPOINT + "price-report/1/53.7976879000/-11531235123555439129000/100000000/")
    assert response404_1.status_code == 404
    assert response404_2.status_code == 404
    assert response404_3.status_code == 404
    assert response404_4.status_code == 404
    assert response404_5.status_code == 404
    assert response404_6.status_code == 404
    assert response404_7.status_code == 404
    
# path('stores/<float:lat>/<float:lon>/', views.local_stores, name='local_stores')
@pytest.mark.django_db
def test_get_stores_by_range(api_client):

    """
    Path: stores/lat/lon/?rad=1000
         Test: 200 GET all stores
               404 Invalid data type for lat/lon
               400 Invalid data type for rad query 
    """

    response200 = api_client.get(ENDPOINT + "stores/53.7976879000/-1.5439129000/")
    assert response200.status_code == status.HTTP_200_OK
    assert len(response200.json()) == 62
    assert response200.json()[0] == {'store_id': 44, 'store_name': 'WHSmith', 'lat': '53.7976879000', 'lon': '-1.5439129000', 'monday': 'Monday: 9:00\u202fAM\u2009–\u20096:00\u202fPM', 'tuesday': 'Tuesday: 9:00\u202fAM\u2009–\u20096:00\u202fPM', 'wednesday': 'Wednesday: 9:00\u202fAM\u2009–\u20096:00\u202fPM', 'thursday': 'Thursday: 9:00\u202fAM\u2009–\u20096:00\u202fPM', 'friday': 'Friday: 9:00\u202fAM\u2009–\u20096:00\u202fPM', 'saturday': 'Saturday: 9:00\u202fAM\u2009–\u20096:00\u202fPM', 'sunday': 'Sunday: 11:00\u202fAM\u2009–\u20095:00\u202fPM', 'distance': 0.0}

    response404_1 = api_client.get(ENDPOINT + "stores/wergwergerg/-1.5439129000/?rad=10")
    response404_2 = api_client.get(ENDPOINT + "stores/53.7976879000/wergwergwerg/?rad=10")
    assert response404_1.status_code == 404
    assert response404_2.status_code == 404

    #Test query functionality
    response200_1 = api_client.get(ENDPOINT + "stores/53.7976879000/-1.5439129000/?rad=10")
    response200_2 = api_client.get(ENDPOINT + "stores/53.7976879000/-1.5439129000/?rad=1000000000000000")
    assert response200_1.status_code == 200
    assert len(response200_1.json()) == 3
    assert response200_1.json()[0] == {'store_id': 3, 'store_name': 'WHSmith', 'lat': '53.7976879000', 'lon': '-1.5439129000', 'monday': 'Monday: 9:00\u202fAM\u2009–\u20096:00\u202fPM', 'tuesday': 'Tuesday: 9:00\u202fAM\u2009–\u20096:00\u202fPM', 'wednesday': 'Wednesday: 9:00\u202fAM\u2009–\u20096:00\u202fPM', 'thursday': 'Thursday: 9:00\u202fAM\u2009–\u20096:00\u202fPM', 'friday': 'Friday: 9:00\u202fAM\u2009–\u20096:00\u202fPM', 'saturday': 'Saturday: 9:00\u202fAM\u2009–\u20096:00\u202fPM', 'sunday': 'Sunday: 11:00\u202fAM\u2009–\u20095:00\u202fPM', 'distance': 0.0}
    assert response200_2.status_code == 200
    assert len(response200_2.json()) == 140

    response400 = api_client.get(ENDPOINT + "stores/53.7976879000/-1.5439129000/?rad=wfgwergwerg")
    assert response400.status_code == 400

# path('users/<int:user_id>/favourites/', views.favourites, name='favourites')
@pytest.mark.django_db
def test_get_user_favourites(api_client):
    
    """
    Path: users/user_id/favourites/ 
         Test: GET all favourites of a specified user
               404 Invalid user id
               404 Invalid data type for user id
    """

    response200 = api_client.get(ENDPOINT + "users/4/favourites/")
    assert response200.status_code == status.HTTP_200_OK
    assert response200.json() == [{'fav_product_id': 7, 'product_id': 4, 'product': 'Broccoli', 'brand': 'VeggieDelight', 'size': '500g', 'product_photo_url': 'https://cdn.pixabay.com/photo/2016/03/05/19/02/appetite-1238251_1280.jpg'}, {'fav_product_id': 20, 'product_id': 10, 'product': 'Cookies', 'brand': 'Snacky', 'size': '300g', 'product_photo_url': 'https://images.unsplash.com/photo-1558961363-fa8fdf82db35?q=80&w=3286&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'}]

    response404_1 = api_client.get(ENDPOINT + "users/125323452345234/favourites/")
    response404_2 = api_client.get(ENDPOINT + "users/rwgergwerg/favourites/")
    assert response404_1.status_code == 404
    assert response404_2.status_code == 404


# path('categories/<int:category_id>/products/', views.products_by_category, name='products_by_category')
@pytest.mark.django_db
def test_get_products_by_category(api_client):
    
    """
    Path: categories/category_id/products/ 
         Test: GET all products within a specified category
               404 Invalid category id
               404 Invalid data type for category id
    """

    response200 = api_client.get(ENDPOINT + "categories/3/products/")
    assert response200.status_code == status.HTTP_200_OK
    assert len(response200.json()) == 2
    assert response200.json()[0] == {
		"product_id": 5,
		"product": "Milk",
		"description": "Whole milk",
		"brand": "DairyPure",
		"size": "1L",
		"product_photo_url": "https://cdn.pixabay.com/photo/2017/09/11/23/34/milk-bottle-2740848_1280.jpg"
	}

    response404_1 = api_client.get(ENDPOINT + "users/125323452345234/favourites/")
    response404_2 = api_client.get(ENDPOINT + "categories/wergerg/products/")
    assert response404_1.status_code == 404
    assert response404_2.status_code == 404




handler400 = error_400
handler404 = error_404
handler500 = error_500