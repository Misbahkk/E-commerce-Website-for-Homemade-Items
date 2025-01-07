from django.urls import path
from home.views import index ,category_detail


urlpatterns = [
    path("",index,name='index'),
    path('category/<slug:slug>/', category_detail, name='category_detail'),
    
]