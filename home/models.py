from django.db import models
from django.contrib.auth.models import User
# from django.contrib import admin

# null=True : db can b blank
# blank=True : when running save method/submit a form, can b blank

# Create your models here.
class Profile(models.Model):
    picture = models.ImageField(null=True, blank=True, upload_to='profiles/', default='user.png')
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE) #user has 1 profile, each profile associates w/ 1 user
    name = models.CharField(max_length=100, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name or "Unnamed"
    
class M_Category(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name or ""

class Supplier(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.name or ""

class Colour(models.Model):
    name = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.name or ""

class Material(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    picture = models.ImageField(null=True, blank=True, upload_to='materials/', default='material_empty.jpeg')
    name = models.CharField(max_length=200, null=True) 
    size = models.CharField(max_length=200, null=True, blank=True)
    stock = models.IntegerField(null=True)
    colour = models.ForeignKey(Colour, null=True, blank=True, on_delete=models.SET_NULL)
    cost = models.CharField(max_length=50, null=True)
    supplier = models.ForeignKey(Supplier, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(M_Category, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['-updated', 'created']

    def __str__(self):
        return self.name or "Unnamed"
    
class P_Category(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name or ""

class Product(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    picture = models.ImageField(null=True, blank=True, upload_to='products/', default='product_empty.jpeg')
    name = models.CharField(max_length=200, null=True)
    size = models.CharField(max_length=200, null=True, blank=True)
    stock = models.IntegerField(null=True)
    sold = models.CharField(max_length=200, null=True)
    cost = models.CharField(max_length=50, null=True)
    category = models.ForeignKey(P_Category, null=True, on_delete=models.SET_NULL)
    description = models.TextField(null=True, blank=True)
    materials = models.ManyToManyField(Material, related_name='products', blank=True, through="ProductMaterial")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['-updated', 'created']

    def __str__(self):
        return self.name or "Unnamed"
    
class ProductMaterial(models.Model):
    material = models.ForeignKey(Material, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    quantity_used = models.IntegerField(null=True)    

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'material'], name='unique_ProductMaterial')
        ]
    

