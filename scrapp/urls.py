from django.urls import path
from . import views

urlpatterns = [
     path('scrape/', views.index, name='index'),
     path('scrape_product/', views.scrape_product, name='scrape_product'),
]