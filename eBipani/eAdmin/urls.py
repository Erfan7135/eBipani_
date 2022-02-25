from django.urls import path
from eAdmin import views

urlpatterns = [
    path('', views.index, name='index'),
    path('customers/', views.customer, name='customer'),
    path('customers/deleteCustomer', views.deleteCustomer, name='deleteCustomer'),
    path('customers/searchCustomer', views.searchCustomer, name='searchCustomer'),
    path('sellers/', views.seller, name='seller'),
    path('sellers/deleteSeller', views.deleteSeller, name='deleteSeller'),
    path('sellers/searchSeller', views.searchSeller, name='searchSeller'),
    path('shippers/', views.shipper, name='shipper'),
    path('shippers/addShipper', views.addShipper, name='addShipper'),
    path('shippers/regShipper', views.regShipper, name='regShipper'),
    path('shippers/editShipper', views.editShipper, name='editShipper'),
    path('shippers/updateShipper', views.updateShipper, name='updateShipper'),
    path('shippers/deleteShipper', views.deleteShipper, name='deleteShipper'),
    path('shippers/searchShipper', views.searchShipper, name='searchShipper'),
    path('newAdmin/', views.newAdmin, name='newAdmin'),
    path('newAdmin/registerAdmin', views.registerAdmin, name='newAdmin'),
]
