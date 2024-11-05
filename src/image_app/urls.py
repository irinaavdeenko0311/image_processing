from django.urls import path

from .views import ImageListCreateView, ImageRetrieveUpdateDestroyView

urlpatterns = [
    path("images/", ImageListCreateView.as_view(), name="images"),
    path("images/<int:pk>/", ImageRetrieveUpdateDestroyView.as_view(), name="image"),
]
