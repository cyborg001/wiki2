from django.urls import path

from . import views

app_name = 'ency'
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.wiki, name="wiki"),
    path('random_page',views.random_page, name='random_page'),
    path('new_page', views.new_page, name='new_page'),
    path('edit',views.edit, name='edit'),
]
