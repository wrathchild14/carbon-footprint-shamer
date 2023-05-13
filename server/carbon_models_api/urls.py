from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict, name='predict'),
    path('process-text/<str:username>/<str:city>/<str:country>/<str:text>/', views.process_text, name='process-text'),
    path('upload/', views.upload_image, name='upload_image'),
    path('image/<int:pk>/', views.image_detail, name='image_detail'),
    path('save-data/', views.save_data, name='save_data'),
    path('data-list/', views.data_list, name='data_list'),
]
