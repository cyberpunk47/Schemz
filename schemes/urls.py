from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('schemes/', views.scheme_list, name='scheme_list'),
    path('schemes/create/', views.scheme_create, name='scheme_create'),
    path('schemes/matched/', views.matched_schemes, name='matched_schemes'),
    path('schemes/my-applications/', views.my_applications, name='my_applications'),
    path('schemes/api/list/', views.scheme_api_list, name='scheme_api_list'),
    path('schemes/<int:pk>/', views.scheme_detail, name='scheme_detail'),
    path('schemes/<int:pk>/apply/', views.scheme_apply, name='scheme_apply'),
    path('schemes/<int:pk>/edit/', views.scheme_edit, name='scheme_edit'),
    path('schemes/manage-applications/', views.manage_applications, name='manage_applications'),
    path('schemes/application/<int:pk>/approve/', views.approve_application, name='approve_application'),
    path('schemes/application/<int:pk>/reject/', views.reject_application, name='reject_application'),
    path('schemes/detail/<slug:slug>/', views.scheme_detail_slug, name='scheme_detail_slug'),
    path('schemes/category/<str:category>/', views.scheme_by_category, name='scheme_by_category'),
    re_path(r'^schemes/year/(?P<year>[0-9]{4})/$', views.schemes_by_year, name='schemes_by_year'),
]
