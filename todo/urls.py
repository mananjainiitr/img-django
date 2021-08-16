from django.urls import path

from .views import index, detail, create,update,delete,updatetodo,deletetodo,createform,item_create

app_name='todo'
urlpatterns = [
    path('', index, name='index'),
    path('<int:list_id>/', detail, name='list_details'),
    path('createlist/', create, name='list_create'),
    path('update/',update, name='update_list'),
    path('delete/',delete, name='delete_list'),
    path('<int:list_id>/todo/updatetodo/',updatetodo,name="updatetodo"),
    path('<int:list_id>/todo/deletetodo/',deletetodo,name="deletetodo"),
    path('create/',createform,name="createform"),
    path('item_create/',item_create, name='item_create'),


]