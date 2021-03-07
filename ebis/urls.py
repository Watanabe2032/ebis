from django.urls import path
from . import views

app_name = 'ebis'
urlpatterns = [
    path('', views.ebisHome, name='home'),
    path('search-equipment', views.searchEquipment, name='search-equipment'),
    path('add-equipment', views.addEquipment, name='add-equipment'),
    path('edit-equipment', views.editEquipment, name='edit-equipment'),
    path('edit-category-tag', views.editCategoryTag, name='edit-category-tag'),
    path('edit-equipment-user', views.editEquipmentUser, name='edit-equipment-user'),
    path('show-borrowing-history', views.showBorrowingHistory, name='show-borrowing-history'),
]
