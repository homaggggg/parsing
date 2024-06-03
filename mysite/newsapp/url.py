from django.urls import path
from . import views

urlpatterns = [
    path('', views.readDB, name='news'),
    path('news/<str:pk>/', views.readDbOne, name='read_one'),
    path('create/', views.CreateDocDB, name='create'),
    path('update/<str:pk>/', views.UpdateDB, name='update'),
    path('delete/<str:pk>/', views.DeleteDocDB, name='delete'),
    path('delete_all/', views.DeleteAllDocsDB, name='delete_all'),
]
