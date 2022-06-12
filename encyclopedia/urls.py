from django.urls import path

from . import views

app_name = 'ency'
urlpatterns = [
    # path("", views.index, name="index"),
    path("",views.IndexView.as_view(),name='index'),
    # path("wiki/<str:name>", views.wiki, name="wiki"),
    path("<int:pk>", views.WikiView.as_view(),name='wiki'),
    path('random_page',views.random_page, name='random_page'),
    path('new_page', views.new_page, name='new_page'),
    path('edit/<int:pk>',views.edit, name='edit'),
    path('logout',views.loggout, name = 'logout'),
]
