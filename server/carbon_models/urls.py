from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict, name='predict'),
    path('process-text/<str:username>/<str:city>/<str:country>/<str:text>/', views.process_text, name='process-text'),
]
