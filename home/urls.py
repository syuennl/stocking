from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('add-product/', views.addProduct, name="add-product"),
    path('add-material/', views.addMaterial, name="add-material"),
    path('increase/<str:obj_type>/<str:pk>', views.increase, name="increase"),
    path('decrease/<str:obj_type>/<str:pk>', views.decrease, name="decrease"),

    path('update-product/<str:pk>/', views.updateProduct, name="update-product"),
    path('update-material/<str:pk>/', views.updateMaterial, name="update-material"),
    path('delete/<str:obj_type>/<str:pk>/', views.delete, name="delete"),

    path('profile/<str:pk>/', views.userProfile, name="profile"),
    path('update-profile/', views.updateProfile, name="update-profile"),

    path('', views.home, name="home"),
    path('<str:acc_type>/', views.home, name="admin-home"),
    # path('', views.UserHomeView.as_view(), name="home"),
    # path('adminn/', views.AdminHomeView.as_view(), name="admin-home"),
    path('product/<str:pk>/', views.product, name="product"),
    path('product/<str:pk>/<str:acc_type>/', views.product, name="admin-product"),
    path('material/<str:pk>/', views.material, name="material"),
    path('material/<str:pk>/<str:acc_type>/', views.material, name="admin-material"),

    
    
]