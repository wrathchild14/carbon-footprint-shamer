from django.conf.urls.static import static
from django.urls import path

from server import settings
from . import views

urlpatterns = [
    path('predict/', views.predict, name='predict'),
    path('process-text/<str:username>/<str:city>/<str:country>/<str:text>/', views.process_text, name='process-text'),
    path('upload/', views.upload_image, name='upload_image'),
    path('image/<int:pk>/', views.get_image_path, name='image_detail'),
    path('save-data/', views.save_data, name='save_data'),
    path('data-list/', views.data_list, name='data_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
