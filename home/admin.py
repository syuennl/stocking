from django.contrib import admin
from .models import Profile, Material, Product, M_Category, P_Category, Supplier, Colour

# Register your models here.
admin.site.register(Profile)
admin.site.register(Material)
admin.site.register(Supplier)
admin.site.register(M_Category)
admin.site.register(P_Category)
admin.site.register(Colour)
# admin.site.register(Product)
# admin.site.register(ProductMaterial)

class ProductMaterialInline(admin.TabularInline):  # / admin.StackedInline
    model = Product.materials.through
    extra = 3  # Number of extra empty forms you want to display

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin): # when registering products in django admin pg(?)
    inlines = [ProductMaterialInline]