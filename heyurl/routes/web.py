from django.urls import path

from heyurl import views

urlpatterns = [
    path('', views.index, name='index'),
    path('store', views.store, name='store'),
    path('clicks', views.clicks, name='clicks'),
    path('json-urls', views.json_urls, name='json-urls'),
]
