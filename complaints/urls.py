from . import views
from django.urls import path
urlpatterns = [
    path('', views.home, name='home'),   
    path('add_complaint/', views.add_complaint, name='add_complaint'),
    path('view_complaint/', views.view_complaints, name='view_complaint'),
    path('delete/<int:id>/', views.delete_complaint),
    path('edit/<int:id>/', views.edit_complaint),
    path('login/',views.login_view, name='login_view'),
    path('register/',views.register, name='register'),
    path('update_status/<int:id>/', views.update_status, name='update_status'),
    path('logout/',views.logout_view,name='logout')
]
