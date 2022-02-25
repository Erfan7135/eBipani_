from unicodedata import name
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.searchProducts, name='searchProducts'),
    path('users/csignin/', views.userSignin, name='userSignin'),
    path('users/ssignin/', views.sellerRegistration, name='sellerRegistration'),
    path('users/login/', views.userLogin, name='userLogin'),
    path('users/logout/', views.logout, name='logout'),
    path('products/<category>/', views.productByCategory, name='productByCategory'),
    path('products/<category>/<id>/', views.individualProduct, name='individualProduct'),
    path('users/admin/', include('eAdmin.urls')),
    path('users/seller/', include('eSeller.urls')),
    path('users/customer/', include('eCustomer.urls')),
]
