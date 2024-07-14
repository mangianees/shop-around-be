from django.db import connection
# from .models import PriceReport, Stores

def get_local_prices(product_id, lat, lon, rad):
    query ='''
    WITH latest_price_report AS (
        SELECT price_reports.*, 
            ROW_NUMBER() OVER(PARTITION BY store_id ORDER BY created_at DESC) AS rn
        FROM price_reports 
        WHERE product_id = %s)
    SELECT pr.price_id, pr.price, st.store_id, st.store_name, st.lat, st.lon, ST_Distance(
        ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography,
        ST_SetSRID(ST_MakePoint(st.lon, st.lat), 4326)::geography
    ) AS distance, st.monday, st.tuesday, st.wednesday, st.thursday, st.friday, st.saturday, st.sunday 
    FROM latest_price_report pr
    INNER JOIN stores st ON pr.store_id = st.store_id
    WHERE pr.rn = 1 
    AND ST_DWithin(
    ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography, 
    ST_SetSRID(ST_MakePoint(st.lon, st.lat), 4326)::geography, 
    %s
    )
    ORDER BY pr.price;
    
    '''

    params = [product_id, lon, lat, lon, lat, rad]
    
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        results = cursor.fetchall()

    price_reports = []
    for row in results:
        price_report = {
            'price_id': row[0],
            'price': row[1],
            'store_id': row[2],
            'store_name': row[3],
            'latitude': row[4],
            'longitude': row[5],
            'distance': row[6],
            "monday" : row[7],
            "tuesday" : row[8],
            "wednesday" : row[9],
            "thursday" : row[10],
            "friday" : row[11],
            "saturday" : row[12],
            "sunday" : row[13]
        }
        price_reports.append(price_report)
    
    return price_reports

def get_local_stores(lat, lon, rad):
    query = '''
    SELECT stores.*, ST_Distance(
        ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography,
        ST_SetSRID(ST_MakePoint(stores.lon, stores.lat), 4326)::geography
    ) AS distance 
    FROM stores
    WHERE ST_DWithin(
        ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography, 
        ST_SetSRID(ST_MakePoint(stores.lon, stores.lat), 4326)::geography, 
        %s
    )
    ORDER BY distance;
    '''

    params = [lon, lat, lon, lat, rad]

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        results = cursor.fetchall()

    local_stores = []
    for row in results:
        local_store = {
            "store_id" : row[0],
            "store_name" : row[1],
            "lat" : row[2],
            "lon" : row[3],
            "monday" : row[4],
            "tuesday" : row[5],
            "wednesday" : row[6],
            "thursday" : row[7],
            "friday" : row[8],
            "saturday" : row[9],
            "sunday" : row[10],
            "distance" : row[11],
        }
        local_stores.append(local_store)
        
    return local_stores

def get_favourites_by_user(user_id):
    query = '''
    SELECT fp.fav_product_id, pr.product_id, pr.product, pr.brand, pr.size, pr.product_photo_url
    FROM favourite_products fp
    JOIN products pr ON fp.product_id = pr.product_id 
    WHERE FP.user_id = %s;
    '''

    params = [user_id]

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        results = cursor.fetchall()

    favourite_products = []
    for row in results:
        favourite_product = {
            'fav_product_id': row[0],
            'product_id': row[1],
            'product': row[2],
            'brand': row[3],
            'size': row[4],
            'product_photo_url': row[5]
        }

        favourite_products.append(favourite_product)

    return favourite_products

def get_products_by_category_id(category_id):
    query = '''
    SELECT product_id, product, description, brand, size, product_photo_url
    FROM products 
    WHERE category_id = %s;
    '''
    
    params = [category_id]

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        results = cursor.fetchall()

    products = []
    for row in results:
        product = {
            'product_id': row[0],
            'product': row[1],
            'description': row[2],
            'brand': row[3],
            'size': row[4],
            'product_photo_url': row[5]
        }

        products.append(product)

    return products

def check_category_id(category_id):
    query = '''
    SELECT *
    FROM categories 
    WHERE category_id = %s;
    '''
    
    params = [category_id]

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        results = cursor.fetchall()

    if len(results) == 0:
        return False
    else:
        return True

def check_user_id(user_id):
    query = '''
    SELECT *
    FROM users 
    WHERE user_id = %s;
    '''
    
    params = [user_id]

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        results = cursor.fetchall()

    if len(results) == 0:
        return False
    else:
        return True

def check_product_id(product_id):
    query = '''
    SELECT *
    FROM products 
    WHERE product_id = %s;
    '''
    
    params = [product_id]

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        results = cursor.fetchall()

    if len(results) == 0:
        return False
    else:
        return True