from django.urls import path
from api import views


urlpatterns = [
    path('cafe', views.get_cafe),
    path('restaurant', views.get_restaurant),
    path('cafe/keyword', views.get_cafe_kwrds),
    path('restaurant/keyword', views.get_res_kwrds),
    path('stay', views.get_filter_stay),
]
