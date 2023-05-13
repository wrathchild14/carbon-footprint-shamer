from django.conf.urls.static import static
from django.urls import path

from server import settings
from . import views

urlpatterns = [
    path('process-text/<str:username>/<str:city>/<str:country>/<str:text>/', views.process_text, name='process-text'),
    path('save-data/', views.save_data, name='save_data'),
    path('list-data/', views.list_data, name='list_data'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
