from django.urls import include, path

app_name = "gallery"

urlpatterns = [
    path("api/", include("gallery.api.urls", namespace="api_gallery")),
]
