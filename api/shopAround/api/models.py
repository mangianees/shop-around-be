from django.db import models

class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.category_name

class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    brand = models.CharField(max_length=255)
    size = models.CharField(max_length=50)
    category = models.ForeignKey("Categories", on_delete=models.CASCADE)
    product_photo_url = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.product
    
class Stores(models.Model):
    store_id = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=13, decimal_places=10)
    lon = models.DecimalField(max_digits=13, decimal_places=10)
    monday = models.CharField(max_length=300, blank=True)
    tuesday = models.CharField(max_length=300, blank=True)
    wednesday = models.CharField(max_length=300, blank=True)
    thursday = models.CharField(max_length=300, blank=True)
    friday = models.CharField(max_length=300, blank=True)
    saturday = models.CharField(max_length=300, blank=True)
    sunday = models.CharField(max_length=300, blank=True)

    class Meta:
        db_table = 'stores'

    def __str__(self):
        return self.store_name
    
class PriceReport(models.Model):
    price_id = models.AutoField(primary_key=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    store = models.ForeignKey("Stores", on_delete=models.CASCADE)
    product = models.ForeignKey("Products",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'price_reports'

    def __str__(self):
        return self.price_id
    
class Favorite_Products(models.Model):
    fav_product_id = models.AutoField(primary_key=True)
    user = models.ForeignKey("Users", on_delete=models.CASCADE)
    product = models.ForeignKey("Products",on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'favourite_products'

    def __str__(self):
        return self.fav_product_id

class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username