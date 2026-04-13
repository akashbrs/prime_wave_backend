from django.urls import path
from .views import contact_view, debug_view

urlpatterns = [
    path('contact/', contact_view, name='contact'),
    path('debug/', debug_view, name='debug'),
]
